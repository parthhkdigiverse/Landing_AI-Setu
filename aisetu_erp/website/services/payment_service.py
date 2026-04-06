import razorpay
import uuid
import logging
import time
import requests
import json
from django.conf import settings
from website.models import Payment, GlobalSettings
from website.utils import generate_invoice
from uuid import UUID

logger = logging.getLogger('website')

class PaymentService:
    @staticmethod
    def _get_settings():
        """Helper to get GlobalSettings singleton."""
        gs = GlobalSettings.objects.first()
        if not gs:
            # Create a default one if it doesn't exist
            gs = GlobalSettings.objects.create()
        return gs

    @staticmethod
    def _get_razorpay_client(gs=None):
        if not gs:
            gs = PaymentService._get_settings()
            
        if gs.razorpay_key_id and gs.razorpay_key_secret:
            return razorpay.Client(auth=(gs.razorpay_key_id, gs.razorpay_key_secret))
        
        # Fallback to .env
        return razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    @classmethod
    def initiate_payment_link(cls, signup, amount_val):
        """
        Unified entry point for payment initiation.
        Delegates to the active gateway.
        """
        gs = cls._get_settings()
        gateway = gs.active_gateway or "RAZORPAY"
        
        if gateway == "CASHFREE":
            return cls.initiate_cashfree_payment(signup, amount_val, gs)
        else:
            return cls.initiate_razorpay_payment(signup, amount_val, gs)

    @classmethod
    def initiate_razorpay_payment(cls, signup, amount_val, gs):
        """
        Creates a Razorpay Payment Link.
        """
        try:
            client = cls._get_razorpay_client(gs)
            merchant_transaction_id = uuid.uuid4().hex
            total_amount = float(amount_val)
            amount_in_paise = int(total_amount * 100)

            base_domain = getattr(settings, 'BASE_DOMAIN', 'http://localhost:5004')
            
            display_id = merchant_transaction_id
            
            callback_url = f"{base_domain}/payment-success/?merchantTransactionId={merchant_transaction_id}"

            clean_mobile = "".join(filter(str.isdigit, signup.mobile_number))
            customer_payload = {"name": signup.owner_name, "contact": clean_mobile}
            if signup.email:
                customer_payload["email"] = signup.email

            expire_min = getattr(settings, 'RAZORPAY_LINK_EXPIRE_MINUTES', 30)
            expire_by = int(time.time() + (expire_min * 60) + 300)
            payload = {
                "amount": amount_in_paise,
                "currency": "INR",
                "accept_partial": False,
                "description": f"AI Setu Service - {signup.shop_name}",
                "customer": customer_payload,
                "notify": {"sms": True, "email": True},
                "reminder_enable": True,
                "notes": {
                    "signup_id": str(signup.id), 
                    "merchant_transaction_id": merchant_transaction_id,
                    "display_id": display_id
                },
                "expire_by": expire_by,
                "callback_url": callback_url,
                "callback_method": "get"
            }

            logger.info(f"Initiating Razorpay Payment for signup={signup.id}, amount={amount_val}")
            payment_link = client.payment_link.create(payload)

            Payment.objects.create(
                pricing_signup=signup,
                transaction_id=UUID(merchant_transaction_id),
                amount=total_amount,
                status="PENDING",
                gateway="RAZORPAY"
            )

            return {
                "success": True,
                "payment_url": payment_link.get("short_url"),
                "merchantTransactionId": merchant_transaction_id,
                "gateway": "RAZORPAY"
            }
        except Exception as e:
            logger.error(f"Razorpay Initiation error: {e}", exc_info=True)
            raise e

    @classmethod
    def initiate_cashfree_payment(cls, signup, amount_val, gs):
        """
        Creates a Cashfree Order and returns the payment session/url.
        """
        try:
            merchant_transaction_id = uuid.uuid4().hex
            total_amount = float(amount_val)
            
            # Cashfree credentials
            app_id = gs.cashfree_app_id
            secret_key = gs.cashfree_secret_key
            env = gs.cashfree_environment # SANDBOX or PRODUCTION
            
            url = "https://sandbox.cashfree.com/pg/orders" if env == "SANDBOX" else "https://api.cashfree.com/pg/orders"
            
            base_domain = getattr(settings, 'BASE_DOMAIN', 'http://localhost:5004')
            
            display_id = merchant_transaction_id
            
            return_url = f"{base_domain}/payment-success/?merchantTransactionId={merchant_transaction_id}&gateway=CASHFREE"

            clean_mobile = "".join(filter(str.isdigit, signup.mobile_number))
            
            payload = {
                "order_id": display_id,
                "order_amount": total_amount,
                "order_currency": "INR",
                "customer_details": {
                    "customer_id": str(signup.id),
                    "customer_name": signup.owner_name,
                    "customer_email": signup.email or "customer@aisetu.com",
                    "customer_phone": clean_mobile
                },
                "order_meta": {
                    "return_url": return_url,
                    "notify_url": f"{base_domain}/cashfree-webhook/"
                },
                "order_note": f"AI Setu Service - {signup.shop_name}"
            }

            headers = {
                "accept": "application/json",
                "content-type": "application/json",
                "x-api-version": "2023-08-01",
                "x-client-id": app_id,
                "x-client-secret": secret_key
            }

            logger.info(f"Initiating Cashfree Payment for signup={signup.id}, amount={amount_val}")
            response = requests.post(url, json=payload, headers=headers)
            
            if response.status_code != 200:
                logger.error(f"Cashfree API Error: {response.text}")
                raise Exception(f"Cashfree API Error: {response.text}")

            order_data = response.json()
            payment_session_id = order_data.get("payment_session_id")
            cf_mode = "sandbox" if env == "SANDBOX" else "production"
            
            Payment.objects.create(
                pricing_signup=signup,
                transaction_id=UUID(merchant_transaction_id),
                amount=total_amount,
                status="PENDING",
                gateway="CASHFREE"
            )

            return {
                "success": True,
                "payment_url": payment_session_id, 
                "cf_mode": cf_mode,
                "merchantTransactionId": merchant_transaction_id,
                "gateway": "CASHFREE",
                "cf_order_id": order_data.get("cf_order_id")
            }
        except Exception as e:
            logger.error(f"Cashfree Initiation error: {e}", exc_info=True)
            raise e

    @classmethod
    def verify_and_update_status(cls, payment_id, merchant_transaction_id, gateway="RAZORPAY"):
        """
        Unified verification.
        """
        if gateway == "CASHFREE":
            return cls.verify_cashfree_status(merchant_transaction_id)
        else:
            return cls.verify_razorpay_status(payment_id, merchant_transaction_id)

    @classmethod
    def verify_razorpay_status(cls, razorpay_payment_id, merchant_transaction_id):
        try:
            if not razorpay_payment_id or merchant_transaction_id == "UNKNOWN":
                return "PENDING"

            client = cls._get_razorpay_client()
            payment_info = client.payment.fetch(razorpay_payment_id)
            status = payment_info.get('status')
            
            if status in ['captured', 'authorized']:
                return cls._mark_payment_success(merchant_transaction_id, payment_info)
            return "FAILURE"
        except Exception as e:
            logger.error(f"Razorpay verification error: {e}")
            return "FAILURE"

    @classmethod
    def verify_cashfree_status(cls, display_id):
        try:
            gs = cls._get_settings()
            env = gs.cashfree_environment
            url = f"https://sandbox.cashfree.com/pg/orders/{display_id}" if env == "SANDBOX" else f"https://api.cashfree.com/pg/orders/{display_id}"
            
            headers = {
                "x-api-version": "2023-08-01",
                "x-client-id": gs.cashfree_app_id,
                "x-client-secret": gs.cashfree_secret_key
            }
            
            logger.info(f"Verifying Cashfree Order: {display_id} via {url}")
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                order_status = data.get("order_status")
                logger.info(f"CASHFREE VERIFY RESPONSE for {display_id}: status={order_status}")
                
                merchant_transaction_id = display_id

                # Support multiple success indicators (PAID is v3 standard, SUCCESS is sometimes returned)
                if order_status in ["PAID", "SUCCESS"]:
                    return cls._mark_payment_success(merchant_transaction_id, data)
                return "FAILURE"
            else:
                logger.warning(f"Cashfree Verify Failed! Status: {response.status_code}, Body: {response.text}")
                return "PENDING"
        except Exception as e:
            logger.error(f"Cashfree verification error: {e}", exc_info=True)
            return "FAILURE"

    @classmethod
    def _mark_payment_success(cls, merchant_transaction_id, response_data):
        try:
            db_payment = Payment.objects.get(transaction_id=UUID(merchant_transaction_id))
            if db_payment.status != "SUCCESS":
                db_payment.status = "SUCCESS"
                db_payment.response_data = response_data
                db_payment.save()
                
                try:
                    generate_invoice(db_payment)
                except Exception as inv_err:
                    logger.error(f"Invoice error: {inv_err}")
            return "SUCCESS"
        except Payment.DoesNotExist:
            logger.warning(f"Payment {merchant_transaction_id} not found")
            return "FAILURE"

    @classmethod
    def process_webhook(cls, payload, gateway="RAZORPAY"):
        """
        Unified webhook processing.
        """
        if gateway == "CASHFREE":
            return cls.process_cashfree_webhook(payload)
        
        # Razorpay Logic
        try:
            event = payload.get("event")
            if event == "payment_link.paid":
                payment_link_entity = payload.get("payload", {}).get("payment_link", {}).get("entity", {})
                merchant_transaction_id = payment_link_entity.get("reference_id")
                if merchant_transaction_id:
                    cls._mark_payment_success(merchant_transaction_id, payload)
            return True
        except Exception as e:
            logger.error(f"Razorpay webhook error: {e}")
            return False

    @classmethod
    def process_cashfree_webhook(cls, payload):
        try:
            data = payload.get("data", {})
            order = data.get("order", {})
            order_id = order.get("order_id")
            payment_status = data.get("order", {}).get("order_status") or data.get("payment", {}).get("payment_status")
            
            if order_id and (payment_status == "SUCCESS" or payment_status == "PAID"):
                cls._mark_payment_success(order_id, payload)
            return True
        except Exception as e:
            logger.error(f"Cashfree webhook error: {e}")
            return False
