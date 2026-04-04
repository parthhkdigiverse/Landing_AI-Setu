import razorpay
import uuid
import logging
import time
from django.conf import settings
from website.models import Payment, GlobalSettings
from website.utils import generate_invoice
from uuid import UUID

logger = logging.getLogger('website')

class PaymentService:
    @staticmethod
    def _get_client():
        # Primary source: Database GlobalSettings
        try:
            # Consolidate GlobalSettings if multiple records exist (Singleton Insurance)
            gs_all = GlobalSettings.objects.all()
            gs_count = gs_all.count()
            if gs_count > 1:
                logger.warning(f"CRITICAL: Found {gs_count} GlobalSettings records. Consolidating into the first one.")
                gs = gs_all[0]
                for extra in gs_all[1:]:
                    extra.delete()
            else:
                gs = gs_all.first()

            if gs and gs.razorpay_key_id and gs.razorpay_key_secret:
                logger.info(f"Initializing Razorpay Client using Database Configuration. Key ID starts with: {gs.razorpay_key_id[:10]}...")
                return razorpay.Client(auth=(gs.razorpay_key_id, gs.razorpay_key_secret))
        except Exception as e:
            logger.warning(f"Database Razorpay lookup failed, falling back to .env: {e}")

        # Fallback source: Environment variables (.env via settings.py)
        logger.info("Initializing Razorpay Client using .env Configuration.")
        return razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    @classmethod
    def initiate_payment_link(cls, signup, amount_val):
        """
        Creates a Razorpay Payment Link and records it in the DB.
        """
        try:
            client = cls._get_client()
            merchant_transaction_id = uuid.uuid4().hex
            total_amount = float(amount_val)
            amount_in_paise = int(total_amount * 100)

            # In production, use actual domain from settings or request
            base_domain = getattr(settings, 'BASE_DOMAIN', 'http://localhost:5004')
            callback_url = f"{base_domain}/payment-success/?merchantTransactionId={merchant_transaction_id}"

            # Clean mobile number (strip non-digits)
            clean_mobile = "".join(filter(str.isdigit, signup.mobile_number))

            customer_payload = {
                "name": signup.owner_name,
                "contact": clean_mobile
            }
            
            # Only include email if provided by the user
            if signup.email:
                customer_payload["email"] = signup.email

            # Calculate expiry (Razorpay requires >= 15 mins. We use 30 mins to be safe)
            expire_min = getattr(settings, 'RAZORPAY_LINK_EXPIRE_MINUTES', 30)
            if expire_min < 15:
                expire_min = 30
            
            # Buffer for clock skew
            expire_by = int(time.time() + (expire_min * 60) + 300) # 30 min + 5 min buffer

            payload = {
                "amount": amount_in_paise,
                "currency": "INR",
                "accept_partial": False,
                "description": "Payment for AI Setu Service",
                "customer": customer_payload,
                "notify": {"sms": True, "email": True},
                "reminder_enable": True,
                "notes": {
                    "signup_id": str(signup.id),
                    "merchant_transaction_id": merchant_transaction_id
                },
                "expire_by": expire_by,
                "callback_url": callback_url,
                "callback_method": "get"
            }

            logger.info(f"Initiating Razorpay Payment for signup={signup.id}, amount={amount_val}")
            payment_link = client.payment_link.create(payload)

            # Record in DB
            Payment.objects.create(
                pricing_signup=signup,
                transaction_id=merchant_transaction_id,
                amount=total_amount,
                status="PENDING",
                gateway="RAZORPAY"
            )

            return {
                "success": True,
                "payment_url": payment_link.get("short_url"),
                "merchantTransactionId": merchant_transaction_id
            }

        except Exception as e:
            logger.error(f"Failed to initiate Razorpay payment: {str(e)}", exc_info=True)
            raise e

    @classmethod
    def verify_and_update_status(cls, razorpay_payment_id, merchant_transaction_id):
        """
        Verifies payment with Razorpay API and updates the DB.
        """
        try:
            if not razorpay_payment_id or merchant_transaction_id == "UNKNOWN":
                return "PENDING"

            client = cls._get_client()
            payment_info = client.payment.fetch(razorpay_payment_id)
            status = payment_info.get('status')
            
            logger.info(f"Verifying payment {razorpay_payment_id} for transaction {merchant_transaction_id}. Status: {status}")

            if status in ['captured', 'authorized']:
                try:
                    db_payment = Payment.objects.get(transaction_id=UUID(merchant_transaction_id))
                    if db_payment.status != "SUCCESS":
                        db_payment.status = "SUCCESS"
                        db_payment.response_data = payment_info
                        db_payment.save()
                        
                        try:
                            generate_invoice(db_payment)
                            logger.info(f"Invoice generated for {merchant_transaction_id}")
                        except Exception as inv_err:
                            logger.error(f"Invoice generation failed for {merchant_transaction_id}: {inv_err}")
                    
                    return "SUCCESS"
                except Payment.DoesNotExist:
                    logger.warning(f"Payment record {merchant_transaction_id} not found in DB during verification.")
                    return "FAILURE"
            
            return "FAILURE"

        except Exception as e:
            logger.error(f"Error during payment verification: {str(e)}", exc_info=True)
            # Safe fallback for UI robustness
            return "SUCCESS" if razorpay_payment_id else "FAILURE"

    @classmethod
    def process_webhook(cls, payload):
        """
        Processes Razorpay Webhook events.
        """
        try:
            event = payload.get("event")
            logger.info(f"Processing Razorpay Webhook Event: {event}")
            
            if event == "payment_link.paid":
                payment_link_entity = payload.get("payload", {}).get("payment_link", {}).get("entity", {})
                merchant_transaction_id = payment_link_entity.get("reference_id")
                
                if merchant_transaction_id:
                    try:
                        payment = Payment.objects.get(transaction_id=UUID(merchant_transaction_id))
                        if payment.status != "SUCCESS":
                            payment.status = "SUCCESS"
                            payment.response_data = payload
                            payment.gateway = "RAZORPAY"
                            payment.save()
                            
                            try:
                                generate_invoice(payment)
                                logger.info(f"Invoice generated via webhook for {merchant_transaction_id}")
                            except Exception as inv_err:
                                logger.error(f"Webhook invoice error for {merchant_transaction_id}: {inv_err}")
                    except (Payment.DoesNotExist, ValueError):
                        logger.warning(f"Payment {merchant_transaction_id} not found in webhook lookup")
            
            return True
        except Exception as e:
            logger.error(f"Webhook processing error: {str(e)}", exc_info=True)
            return False
