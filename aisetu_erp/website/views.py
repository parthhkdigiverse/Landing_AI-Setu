from django.shortcuts import get_object_or_404, render

from website.models import DemoRequest,UserLogin, ReferralUser
from django.http import JsonResponse, HttpResponse
import json
import re
import os
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import APIView, api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.response import Response
from rest_framework import status
from dotenv import dotenv_values, set_key, unset_key
import datetime
from .models import FAQ, AllStoreType, CareerPage, ChildJobPosition, ComparisonFeature, ContactPageContent, ContactSubmission, DemoVideo, Feature, Footer, HowItWorksStep, JobPosition, LoginLink, Page, Policy, PricingSignup, LandingPageContent, Payment, PricingSignup, AdminUser, Problem, ReferralPerk, StoreType, Testimonial, USPFeature, BlogCategory, BlogPost
from .serializers import AllStoreTypeSerializer, CareerPageSerializer, ChildJobPositionSerializer, ComparisonFeatureSerializer, FAQSerializer, JobPositionSerializer, LandingPageContentSerializer,JobApplicationSerializer, LoginLinkSerializer, PageSerializer, PolicySerializer,ReferralUserSerializer, ContactPageContentSerializer, BlogCategorySerializer, BlogPostSerializer, FooterSerializer

# ... rest of file until the end ...

@api_view(['GET'])
@permission_classes([AllowAny])
def get_blog_posts(request):
    posts = BlogPost.objects.filter(is_published=True)
    category_slug = request.GET.get('category')
    if category_slug:
        posts = posts.filter(category__slug=category_slug)
        
    serializer = BlogPostSerializer(posts, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_blog_post_detail(request, slug):
    try:
        post = BlogPost.objects.get(slug=slug, is_published=True)
        serializer = BlogPostSerializer(post, context={'request': request})
        return Response(serializer.data)
    except BlogPost.DoesNotExist:
        return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_blog_categories(request):
    categories = BlogCategory.objects.all()
    serializer = BlogCategorySerializer(categories, many=True)
    return Response(serializer.data)
from .utils import generate_invoice, admin_required
import random
import string
from bson import ObjectId
import base64
import hashlib
import requests
import jwt
import uuid
from django.conf import settings


@csrf_exempt
def book_demo_api(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            name = data.get("name")
            contact_number = data.get("contact_number")     
            store_type = data.get("store_type")      
            city = data.get("city")

            if not all([name, contact_number, store_type, city]):
                return JsonResponse({"error": "All fields required"}, status=400)

            DemoRequest.objects.create(
                name=name,
                contact_number=contact_number,
                store_type=store_type,
                city=city,
            )

            return JsonResponse({"message": "Demo request saved successfully"}, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Only POST allowed"}, status=405)

@csrf_exempt
def user_login(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            email = data.POST.get('email')
            password = data.POST.get('password')

            if not all([email, password]):
                return JsonResponse({"error": "All fields required"}, status=400)

            DemoRequest.objects.create(
                email=email,
                password=password,
            )

            return JsonResponse({"message": "Login successfully"}, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Only POST allowed"}, status=405)

def serve_frontend_with_seo(request, slug=None):
    from django.conf import settings
    index_path = settings.REACT_BUILD_DIR / 'index.html'
    
    if not index_path.exists():
        return HttpResponse("Frontend build not found.", status=404)
        
    with open(index_path, 'r', encoding='utf-8') as f:
        html = f.read()
        
    if slug:
        try:
            post = BlogPost.objects.get(slug=slug, is_published=True)
            
            from django.utils.html import escape
            import re
            
            def clean_seo(text):
                if not text: return ""
                # Replace newlines with spaces and condense multiple spaces
                text = re.sub(r'\s+', ' ', text).strip()
                return escape(text)

            # Prepare SEO values
            title = clean_seo(post.seo_title or post.title)
            description = clean_seo(post.seo_description or (post.excerpt if post.excerpt else ""))
            keywords = clean_seo(post.seo_keywords)
            
            # Extract Image URL safely
            image_url = "https://lovable.dev/opengraph-image-p98pqg.png"
            if post.featured_image:
                try:
                    image_url = request.build_absolute_uri(post.featured_image.url)
                except:
                    pass
            
            # Replace Title
            html = re.sub(r'<title>[^<]+</title>', f'<title>{title} | AI-Setu ERP</title>', html)
            
            # Replace Meta Description
            html = re.sub(r'<meta name="description" content="[^"]*" />', f'<meta name="description" content="{description}" />', html)
            
            # Inject/Replace Keywords
            if keywords:
                if '<meta name="keywords"' in html:
                    html = re.sub(r'<meta name="keywords" content="[^"]*" />', f'<meta name="keywords" content="{keywords}" />', html)
                else:
                    # Insert after description
                    html = re.sub(r'(<meta name="description" content="[^"]*" />)', rf'\1\n    <meta name="keywords" content="{keywords}" />', html)

            # Replace OG Tags
            html = re.sub(r'<meta property="og:title" content="[^"]*" />', f'<meta property="og:title" content="{title} | AI-Setu ERP" />', html)
            html = re.sub(r'<meta property="og:description" content="[^"]*" />', f'<meta property="og:description" content="{description}" />', html)
            html = re.sub(r'<meta property="og:image" content="[^"]*" />', f'<meta property="og:image" content="{image_url}" />', html)
            
            # Replace Twitter Tags
            html = re.sub(r'<meta name="twitter:image" content="[^"]*" />', f'<meta name="twitter:image" content="{image_url}" />', html)
            
        except BlogPost.DoesNotExist:
            pass # Fallback to default
            
    return HttpResponse(html)

FIXED_PASSWORD = "1234"
@csrf_exempt
def login_view(request):

    if request.method == "POST":

        data = json.loads(request.body)

        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return JsonResponse({"error": "All fields required"}, status=400)

        # ✅ Check Admin
        try:
            admin = AdminUser.objects.get(email=email)

            if admin.password == password:
                return JsonResponse({
                    "message": "Admin login successful",
                    "role": "admin"
                })

        except AdminUser.DoesNotExist:
            pass

        # ✅ Check User
        if password == FIXED_PASSWORD:

            UserLogin.objects.create(email=email, password=password)

            return JsonResponse({
                "message": "User login successful",
                "role": "user"
            })

        return JsonResponse({"error": "Invalid credentials"}, status=401)

    return JsonResponse({"error": "Only POST allowed"}, status=405)
        
@csrf_exempt
@api_view(['POST'])
def pricing_signup(request):
    shop_name = request.data.get('shop_name')
    owner_name = request.data.get('owner_name')
    mobile_number = request.data.get('mobile_number')
    referral_code_input = request.data.get('referral_code')
    check_referral = request.data.get('check_referral')

    price = 14160  # default price

    # --- 1. REFERRAL VALIDATION ONLY (Apply Button) ---
    if check_referral:
        if referral_code_input:
            # Check if input code exists in PricingSignup OR ReferralUser
            exists_in_pricing = PricingSignup.objects.filter(referral_code=referral_code_input).exists()
            exists_in_referral = ReferralUser.objects.filter(referral_code=referral_code_input).exists()

            if exists_in_pricing or exists_in_referral:
                return Response({
                    "valid": True,
                    "price": 12980
                })

        return Response({
            "valid": False,
            "price": 14160
        })

    # --- 2. NORMAL SIGNUP FLOW ---

    # Check if this mobile is already registered in PricingSignup
    # if PricingSignup.objects.filter(mobile_number=mobile_number).exists():
    #     return Response({
    #         "error": "This mobile number is already registered"
    #     }, status=400)

    # --- CHANGE START: Check for existing code from ReferralUser ---
    existing_referral_user = ReferralUser.objects.filter(mobile_number=mobile_number).first()
    
    if existing_referral_user and existing_referral_user.referral_code:
        # Use the code they already have
        final_referral_code = existing_referral_user.referral_code
    else:
        # Generate a new code ONLY if they don't have one
        final_referral_code = ''.join(random.choices(
            string.ascii_uppercase + string.digits, k=6
        ))
    # --- CHANGE END ---

    # Referral discount logic (Applying the input code from the friend)
    if referral_code_input:
        # Check PricingSignup
        ref_pricing = PricingSignup.objects.filter(referral_code=referral_code_input).first()
        if ref_pricing:
            ref_pricing.total_referrals += 1
            ref_pricing.save()
            price = 12980
        else:
            # Also check ReferralUser table for the discount
            ref_user = ReferralUser.objects.filter(referral_code=referral_code_input).first()
            if ref_user:
                # If your ReferralUser model has a total_referrals field, increment it here
                # ref_user.total_referrals += 1 
                # ref_user.save()
                price = 12980

    # Create the new entry with the final_referral_code (either existing or new)
    signup = PricingSignup.objects.create(
        shop_name=shop_name,
        owner_name=owner_name,
        mobile_number=mobile_number,
        state=request.data.get('state', 'Gujarat'),
        referral_code=final_referral_code
    )

    return Response({
        "message": "Signup successful",
        "referral_code": final_referral_code, # Returns the existing code to the user
        "signup_id": str(signup.id),
        "price": price
    })

@api_view(['GET'])
def landing_page_content_api(request):
    try:
        content = LandingPageContent.objects.first()
        if not content:
            # Create default content if not exists
            content = LandingPageContent.objects.create()
        serializer = LandingPageContentSerializer(content)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

from django.http import HttpResponse

@csrf_exempt
def submit_contact(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            # Save contact form
            contact = ContactSubmission.objects.create(
                name=data.get("name"),
                phone=data.get("phone"),
                email=data.get("email"),
                officeAddress=data.get("officeAddress"),
                message=data.get("message"),
            )

            # Prepare response
            response = {
                "id": str(contact.id),  # Convert ObjectId to string
                "message": "Form submitted successfully!"
            }

            # Return JSON as HttpResponse
            return HttpResponse(
                json.dumps(response),
                content_type="application/json",
                status=201
            )

        except Exception as e:
            response = {"error": str(e)}
            return HttpResponse(
                json.dumps(response),
                content_type="application/json",
                status=500
            )

    response = {"error": "Invalid request"}
    return HttpResponse(
        json.dumps(response),
        content_type="application/json",
        status=400
    )


@api_view(["POST"])
def apply_job(request):

    serializer = JobApplicationSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Application submitted successfully"}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def check_referral(request):

    print("Incoming Data:", request.data)

    mobile = request.data.get("mobile_number")

    if not mobile:
        return Response({"error": "Mobile number required"}, status=400)

    # Check PricingSignup
    user = PricingSignup.objects.filter(mobile_number=mobile).first()

    if user and user.referral_code:
        return Response({
            "referral_code": user.referral_code,
            "status": "existing_pricing_user"
        })

    # Check referral user
    referral_user, created = ReferralUser.objects.get_or_create(
        mobile_number=mobile
    )

    return Response({
        "referral_code": referral_user.referral_code,
        "status": "new_user" if created else "existing_referral_user"
    })

def get_phonepe_access_token():
    """Helper to fetch a V2 OAuth token from PhonePe."""
    url = "https://api.phonepe.com/apis/identity-manager/v1/oauth/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "client_id": settings.PHONEPE_MERCHANT_ID,
        "client_secret": settings.PHONEPE_SALT_KEY, # In V2, Salt Key acts as Client Secret
        "client_version": str(settings.PHONEPE_SALT_INDEX), # Salt Index acts as Client Version
        "grant_type": "client_credentials"
    }
    
    try:
        response = requests.post(url, data=data, headers=headers, timeout=10)
        response.raise_for_status()
        token_data = response.json()
        return token_data.get("access_token")
    except Exception as e:
        print(f"Error fetching PhonePe OAuth token: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"Token Error Response: {e.response.text}")
        return None

@csrf_exempt
@api_view(["POST"])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([AllowAny])
def initiate_payment(request):
    """
    PhonePe PG V2 Payment Initiation (OAuth Based)
    """
    try:
        signup_id = request.data.get("signup_id")
        amount_val = request.data.get("amount") # This is in Rupees from frontend

        if not signup_id or not amount_val:
            return Response({"error": "signup_id or amount is missing"}, status=400)

        signup = PricingSignup.objects.filter(id=signup_id).first()
        if not signup:
            return Response({"error": f"Signup with ID {signup_id} not found"}, status=400)

        # 1. Fetch OAuth Token
        access_token = get_phonepe_access_token()
        if not access_token:
            return Response({"error": "Failed to authenticate with PhonePe (V2)"}, status=500)
        
        # Generate a hex UUID (no dashes) for better compatibility with QR generators
        merchant_transaction_id = uuid.uuid4().hex
        
        # The frontend already includes 18% GST in the provided amount
        total_amount = float(amount_val)
        amount_in_paise = int(total_amount * 100)
        
        # 2. Prepare V2 Payload
        # Auto-detect Sandbox vs Production
        is_sandbox = settings.PHONEPE_MERCHANT_ID.startswith("PGTEST")
        if is_sandbox:
            pay_url = "https://api-preprod.phonepe.com/apis/pg-sandbox/checkout/v2/pay"
        else:
            pay_url = "https://api.phonepe.com/apis/pg/checkout/v2/pay"

        # Detect host dynamically (localhost or ai-setu.com)
        base_domain = request.build_absolute_uri('/').rstrip('/')
        redirect_url = f"{base_domain}/payment-success/?merchantTransactionId={merchant_transaction_id}"
        callback_url = f"{base_domain}/payment-callback/"

        # Sanitize Mobile Number (Ensure exactly 10 digits for PhonePe)
        raw_mobile = str(signup.mobile_number)
        clean_mobile = re.sub(r'\D', '', raw_mobile) # Only digits
        if len(clean_mobile) > 10:
            clean_mobile = clean_mobile[-10:] # Take last 10
            
        payload = {
            "merchantId": settings.PHONEPE_MERCHANT_ID,
            "merchantTransactionId": merchant_transaction_id.upper(), # PhonePe V2 often uses this key
            "merchantUserId": f"USER_{signup.id}",
            "amount": amount_in_paise,
            "mobileNumber": clean_mobile,
            "expireAfter": 1200, 
            "paymentFlow": {
                "type": "PG_CHECKOUT",
                "message": "Payment for AI Setu Service",
                "merchantUrls": {
                    "redirectUrl": redirect_url,
                    "callbackUrl": callback_url
                }
            },
            "redirectMode": "REDIRECT"
        }

        # Log initiation attempt
        log_file = os.path.join(settings.BASE_DIR, 'payment_init_debug.log')
        with open(log_file, 'a') as f:
            f.write(f"\n--- INITIATION {datetime.datetime.now()} ---\n")
            f.write(f"merchantTransactionId: {merchant_transaction_id}\n")
            f.write(f"Payload: {json.dumps(payload, indent=2)}\n")

        # 3. Request Pay Page via V2 API
        # Auto-detect Sandbox vs Production
        is_sandbox = settings.PHONEPE_MERCHANT_ID.startswith("PGTEST")
        if is_sandbox:
            pay_url = "https://api-preprod.phonepe.com/apis/pg-sandbox/checkout/v2/pay"
        else:
            pay_url = "https://api.phonepe.com/apis/pg/checkout/v2/pay"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"O-Bearer {access_token}"
        }

        print(f"--- PHONEPE V2 INITIATION ---")
        print(f"Environment: {'SANDBOX' if is_sandbox else 'PRODUCTION'}")
        print(f"Transaction ID: {merchant_transaction_id}")
        print(f"Total Amount: ₹{total_amount}")
        
        response = requests.post(pay_url, json=payload, headers=headers, timeout=15)
        data = response.json()
        print("PhonePe V2 Response:", data)
        with open(log_file, 'a') as f:
            f.write(f"Response Status: {response.status_code}\n")
            f.write(f"Response Body: {json.dumps(data, indent=2)}\n")

        if response.status_code == 200 and data.get("redirectUrl"):
            # Create payment record with the final amount
            Payment.objects.create(
                pricing_signup=signup,
                transaction_id=merchant_transaction_id,
                amount=total_amount,
                status="PENDING"
            )

            return Response({
                "success": True,
                "payment_url": data.get("redirectUrl"), # Sync with frontend key
                "merchantTransactionId": merchant_transaction_id
            })
        else:
            return Response({
                "error": data.get("message", "Payment initiation failed"),
                "details": data.get("code", "ERROR")
            }, status=400)

    except Exception as e:
        print(f"General Initiation Error: {e}")
        return Response({"error": str(e)}, status=500)

# -------------------------------
# PhonePe Status Check Utility (Synchronous)
# -------------------------------
def check_phonepe_status_sync(merchant_transaction_id):
    """
    Check status using V2 API
    """
    try:
        # 1. Get Token
        access_token = get_phonepe_access_token()
        if not access_token:
            return {"success": False, "message": "Auth failed"}

        # 2. Hit V2 Status Endpoint
        url = f"https://api.phonepe.com/apis/pg/checkout/v2/order/{merchant_transaction_id}/status"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"O-Bearer {access_token}"
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        
        if response.status_code == 200:
            # V2 Success check
            if data.get("state") == "COMPLETED":
                return {"success": True, "data": data}
            return {"success": False, "status": data.get("state"), "data": data}
        
        return {"success": False, "message": data.get("message", "Status check failed")}
    except Exception as e:
        return {"success": False, "message": str(e)}

# -------------------------------
# PhonePe Callback
# -------------------------------
@csrf_exempt
def payment_callback(request):
    try:
        log_file = os.path.join(settings.BASE_DIR, 'payment_debug.log')
        with open(log_file, 'a') as f:
            f.write(f"\n--- CALLBACK {uuid.uuid4()} ---\n")
            f.write(f"Method: {request.method}\n")
            f.write(f"GET: {json.dumps(request.GET.dict())}\n")
            f.write(f"POST: {json.dumps(request.POST.dict())}\n")
            f.write(f"Body: {request.body.decode('utf-8', errors='ignore')[:1000]}\n")

        print("--- PHONEPE CALLBACK RECEIVED ---")
        
        # PhonePe can send data as JSON body OR as Form-Encoded data in POST
        data = {}
        
        # 1. Try JSON Body
        try:
            body_data = json.loads(request.body)
            data = body_data
            print("Parsed JSON body")
        except (ValueError, json.JSONDecodeError):
            print("Not a JSON body or empty")

        # 2. Try POST Form Data if body didn't have what we need
        if not data or "response" not in data:
            if request.POST:
                data = request.POST.dict()
                print("Using POST form data")

        # PhonePe usually sends a base64 encoded 'response'
        if "response" in data:
            response_payload = data["response"]
            decoded_response = base64.b64decode(response_payload).decode()
            data = json.loads(decoded_response)
            print("Successfully decoded base64 response")
        
        # Log the final data for debugging
        print(f"Callback Data: {json.dumps(data, indent=2)}")

        # Extract transaction ID and code
        # Structure is usually: {"success": true, "code": "PAYMENT_SUCCESS", "data": {"merchantTransactionId": "..."}}
        transaction_id = data.get("data", {}).get("merchantTransactionId")
        code = data.get("code")
        
        if not transaction_id:
            print("Error: No transaction_id found in callback data")
            return JsonResponse({"error": "No transaction ID found"}, status=400)

        print(f"Processing callback for Transaction ID: {transaction_id}, Code: {code}")

        from uuid import UUID
        try:
            # Explicitly convert to UUID if it's a string
            if isinstance(transaction_id, str):
                payment_lookup_id = UUID(transaction_id)
            else:
                payment_lookup_id = transaction_id
                
            payment = Payment.objects.get(transaction_id=payment_lookup_id)
            # Store the full response data
            payment.response_data = data
        except (ValueError, Payment.DoesNotExist):
            print(f"Payment not found for ID: {transaction_id}")
            return JsonResponse({"error": f"Payment record {transaction_id} not found"}, status=404)
        
        # Update status
        if code == "PAYMENT_SUCCESS":
            payment.status = "SUCCESS"
            # Optional: Generate invoice here
            try:
                from .utils import generate_invoice
                generate_invoice(payment)
                print(f"Invoice generated for {transaction_id}")
            except Exception as invoice_error:
                print(f"Invoice generation failed for {transaction_id}: {invoice_error}")
        else:
            payment.status = code if code else "FAILED"
            print(f"Status updated to: {payment.status}")
            
        # Final log before saving
        print(f"Saving payment {payment.transaction_id} with status {payment.status} and response_data present: {payment.response_data is not None}")
        payment.save()
        return JsonResponse({"message": "Payment processed", "status": payment.status})

    except Exception as e:
        import traceback
        print(f"Callback Critical Error: {str(e)}")
        traceback.print_exc()
        return JsonResponse({"error": "Failed to process callback", "details": str(e)}, status=500)

@csrf_exempt
def payment_success(request):
    """
    Handle the redirect from PhonePe. Extract status and redirect/render.
    """
    from django.shortcuts import redirect, render
    import base64
    import json
    import os
    from django.conf import settings

    log_file = os.path.join(settings.BASE_DIR, 'payment_debug.log')
    with open(log_file, 'a') as f:
        f.write(f"\n--- SUCCESS REDIRECT {uuid.uuid4()} ---\n")
        f.write(f"Method: {request.method}\n")
        f.write(f"GET: {json.dumps(request.GET.dict())}\n")
        f.write(f"POST: {json.dumps(request.POST.dict())}\n")

    print("--- PAYMENT REDIRECT FROM PG ---")

    # 1. Check if this is an internal redirect (we've already processed it)
    # We check for tid and status but NO response/code/encoded fields
    if request.GET.get('status') and not (request.GET.get('response') or request.POST.get('response')):
        print("Internal redirect detected, serving frontend")
        return render(request, "index.html")
    
    status_code = "UNKNOWN"
    transaction_id = "UNKNOWN"

    # PhonePe redirects back with 'response' (encoded) or 'code' (raw status)
    # Check POST first, then GET
    encoded_response = request.POST.get('response') or request.GET.get('response')
    response_code = request.POST.get('code') or request.GET.get('code')
    # Sometimes transactionId is sent directly in query params or we can get it from 'mt' or similar if custom
    transaction_id_param = request.GET.get('transactionId') or request.GET.get('mt') or \
                          request.POST.get('transactionId') or request.GET.get('merchantTransactionId') or \
                          request.POST.get('merchantTransactionId') or request.GET.get('transaction_id')
    
    if encoded_response:
        try:
            decoded_response = base64.b64decode(encoded_response).decode()
            data = json.loads(decoded_response)
            print(f"Decoded redirect response: {json.dumps(data, indent=2)}")
            status_code = data.get('code', 'UNKNOWN')
            transaction_id = data.get('data', {}).get('merchantTransactionId', 'UNKNOWN')
        except Exception as e:
            print(f"Error parsing redirect response: {e}")
    
    # Fallback for status and ID if base64 failed or was missing
    if status_code == "UNKNOWN" and response_code:
        status_code = response_code
    
    if transaction_id == "UNKNOWN" and transaction_id_param:
        transaction_id = transaction_id_param    # Map to simplified frontend statuses
    if status_code == "PAYMENT_SUCCESS":
        frontend_status = "SUCCESS"
    elif status_code in ["PAYMENT_ERROR", "PAYMENT_DECLINED", "TIMED_OUT"]:
        frontend_status = "FAILURE"
    elif status_code == "PAYMENT_PENDING":
        frontend_status = "PENDING"
    else:
        # -------------------------------
        # DB Lookup Fallback
        # -------------------------------
        # If redirect parameters are missing/unclear, check the database status
        # which might have been updated by the callback already
        if transaction_id != "UNKNOWN":
            try:
                from uuid import UUID
                payment = Payment.objects.get(transaction_id=UUID(transaction_id))
                if payment.status in ["SUCCESS", "FAILURE", "PENDING"]:
                    frontend_status = payment.status
                    print(f"Status resolved from DB for {transaction_id}: {frontend_status}")
                else:
                    frontend_status = status_code
            except Exception as db_err:
                print(f"Fallback DB lookup failed: {db_err}")
                frontend_status = status_code
        else:
            frontend_status = status_code # Still likely "UNKNOWN"

    # Final check: if we are redirecting to index.html anyway, 
    # make sure we have the most accurate status
    if (frontend_status == "UNKNOWN" or frontend_status == "PENDING") and transaction_id != "UNKNOWN":
        print(f"Status still {frontend_status}, attempting synchronous Status API check...")
        status_data = check_phonepe_status_sync(transaction_id)
        if status_data and status_data.get("success"):
            status_code = status_data.get("code")
            if status_code == "PAYMENT_SUCCESS":
                frontend_status = "SUCCESS"
                # Update DB
                try:
                    payment = Payment.objects.get(transaction_id=UUID(transaction_id))
                    if payment.status != "SUCCESS":
                        payment.status = "SUCCESS"
                        payment.response_data = status_data
                        payment.save()
                        print(f"DB updated to SUCCESS via sync check for {transaction_id}")
                except:
                    pass
            elif status_code in ["PAYMENT_ERROR", "PAYMENT_DECLINED", "TIMED_OUT"]:
                frontend_status = "FAILURE"
            elif status_code == "PAYMENT_PENDING":
                frontend_status = "PENDING"

    print(f"Redirecting to frontend with status={frontend_status}, tid={transaction_id}")
    # Redirect to same URL but with our simplified parameters
    return redirect(f"/payment-success/?status={frontend_status}&tid={transaction_id}")

@api_view(["GET"])
@permission_classes([AllowAny])
def check_payment_status_api(request, tid):
    """
    API for frontend to poll payment status.
    """
    try:
        from uuid import UUID
        payment = Payment.objects.get(transaction_id=UUID(tid))
        
        # If still pending in DB, try a sync check once
        if payment.status == "PENDING":
             status_data = check_phonepe_status_sync(tid)
             if status_data and status_data.get("success"):
                 status_code = status_data.get("code")
                 if status_code == "PAYMENT_SUCCESS":
                     payment.status = "SUCCESS"
                     payment.response_data = status_data
                     payment.save()
                 elif status_code == "PAYMENT_FAILED": # Simplified
                     payment.status = "FAILURE"
                     payment.save()
        
        return Response({
            "status": payment.status,
            "tid": str(payment.transaction_id),
            "amount": payment.amount,
            "invoice_url": request.build_absolute_uri(payment.invoice.url) if payment.invoice else None
        })
    except (Payment.DoesNotExist, ValueError):
        return Response({"error": "Payment not found"}, status=404)
    
@api_view(['GET', 'POST', 'DELETE'])
@admin_required
def manage_env_api(request):
    """
    CRUD for .env file.
    GET: List all variables.
    POST: Set a variable (Create/Update).
    DELETE: Unset a variable.
    """
    env_path = settings.BASE_DIR / 'aisetu_erp' / '.env'
    
    if request.method == 'GET':
        # Read all variables
        env_vars = dotenv_values(env_path)
        return Response(env_vars)
    
    elif request.method == 'POST':
        # Create or Update
        key = request.data.get('key')
        value = request.data.get('value')
        
        if not key or value is None:
            return Response({"error": "Key and value are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        # PERSIST to file
        set_key(str(env_path), key, str(value))
        
        # Also update os.environ for immediate effect in CURRENT process
        os.environ[key] = str(value)
        
        return Response({"message": f"Variable {key} set successfully"})
    
    elif request.method == 'DELETE':
        # Delete variable
        key = request.data.get('key')
        
        if not key:
            return Response({"error": "Key is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Try to unset
        result = unset_key(str(env_path), key)
        
        if result[0]: # If something was removed
            if key in os.environ:
                del os.environ[key]
            return Response({"message": f"Variable {key} removed successfully"})
        else:
            return Response({"error": f"Variable {key} not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(["GET"])
def contactus_page_content(request):
    # Fetch the ONLY record
    content = ContactPageContent.objects.first()

    if not content:
        # Only happens the very first time
        content = ContactPageContent.objects.create()
    
    serializer = ContactPageContentSerializer(content)
    return Response(serializer.data)


@api_view(["GET"])
def get_problems(request):
    problems = Problem.objects.filter(is_active=True).order_by('order')
    data = []
    for p in problems:
        data.append({
            "id": str(p.id),
            "title": p.title,
            "description": p.description,
            "icon": p.icon
        })
    return Response(data)


@api_view(["GET"])
def get_features(request):
    features = Feature.objects.filter(is_active=True).order_by('order')
    data = []
    for f in features:
        data.append({
            "id": str(f.id),
            "title": f.title,
            "description": f.description,
            "icon": f.icon
        })
    return Response(data)

@api_view(["GET"])
def get_usp_features(request):
    features = USPFeature.objects.filter(is_active=True).order_by('order')
    data = []
    for f in features:
        data.append({
            "id": str(f.id),
            "title": f.title,
            "description": f.description,
            "icon": f.icon
        })
    return Response(data)

@api_view(["GET"])
def get_how_it_works_steps(request):
    try:
        content = LandingPageContent.objects.first()
        if not content:
            return Response([])
        
        steps = HowItWorksStep.objects.filter(is_active=True).order_by('step_number')
        data = []
        for s in steps:
            data.append({
                "id": str(s.id),
                "title": s.title,
                "description": s.description,
                "icon": s.icon,
                "step_number": s.step_number
            })
        return Response(data)
    except Exception as e:
        return Response({"error": str(e)}, status=500)

@api_view(["GET"])
def get_store_types(request):
    stores = StoreType.objects.filter(is_active=True).order_by('order')
    data = []
    for s in stores:
        data.append({
            "id": str(s.id),
            "title": s.title,
            "icon": s.icon
        })
    return Response(data)

@api_view(["GET"])
def get_referral_perks(request):
    perks = ReferralPerk.objects.filter(is_active=True).order_by('order')
    data = []
    for p in perks:
        data.append({
            "id": str(p.id),
            "value": p.value,
            "text": p.text,
            "icon": p.icon
        })
    return Response(data)

@api_view(["GET"])
@permission_classes([AllowAny])
def get_home_testimonials(request):
    testimonials = Testimonial.objects.filter(is_active=True).order_by('order')[:3]
    data = []
    for t in testimonials:
        data.append({
            "id": str(t.id),
            "name": t.name,
            "role": t.role,
                "review": t.review,
                "rating": t.rating,
                "image": request.build_absolute_uri(t.image.url) if t.image else None
        })
    return Response(data)

@api_view(["GET"])
@permission_classes([AllowAny])
def get_all_testimonials(request):
    testimonials = Testimonial.objects.filter(is_active=True).order_by('order')
    data = []
    for t in testimonials:
        data.append({
            "id": str(t.id),
            "name": t.name,
            "role": t.role,
                "review": t.review,
                "rating": t.rating,
                "image": request.build_absolute_uri(t.image.url) if t.image else None
        })
    return Response(data)

@api_view(["GET"])
def get_comparison_features(request):
    features = ComparisonFeature.objects.filter(is_active=True).order_by('order')
    data = []
    for f in features:
        data.append({
            "id": str(f.id),  # convert ObjectId to string
            "feature_name": f.feature_name,
            "has_ai_setu": f.has_ai_setu,
            "has_traditional": f.has_traditional,
        })
    return Response(data)

@api_view(["GET"])
def get_faqs(request):
    faqs = FAQ.objects.filter(is_active=True).order_by('order')
    data = []
    for f in faqs:
        data.append({
            "id": str(f.id),  # convert ObjectId to string
            "question": f.question,
            "answer": f.answer,
        })
    return Response(data)

@api_view(["GET"])
def get_login_link(request):

    login = LoginLink.objects.filter(is_active=True).first()

    if not login:
        return Response({})

    data = {
        "id": str(login.id),   # convert ObjectId to string
        "label": login.label,
        "url": login.url,
        "is_active": login.is_active,
    }

    return Response(data)

@api_view(["GET"])
def get_demo_video(request):

    video = DemoVideo.objects.filter(is_active=True).first()

    if not video:
        return Response({})

    data = {
        "id": str(video.id),
        "title": video.title,
        "video_url": video.video_url
    }

    return Response(data)
    

@api_view(["GET"])
def all_store_type(request):

    stores = AllStoreType.objects.filter(is_active=True).order_by("name")

    serializer = AllStoreTypeSerializer(stores, many=True)

    return Response(serializer.data)

@api_view(["GET"])
def get_footer(request):
    footer = Footer.objects.first()

    if not footer:
        return Response({"error": "No footer found"})

    serializer = FooterSerializer(footer, context={'request': request})
    return Response(serializer.data)



def convert_objectid(data):
    """
    Recursively convert ObjectId to string
    """
    if isinstance(data, list):
        return [convert_objectid(item) for item in data]

    if isinstance(data, dict):
        new_data = {}
        for key, value in data.items():
            if isinstance(value, ObjectId):
                new_data[key] = str(value)
            else:
                new_data[key] = convert_objectid(value)
        return new_data

    return data


class CareerPageAPIView(APIView):

    def get(self, request):
        career = CareerPage.objects.first()

        serializer = CareerPageSerializer(career)

        data = convert_objectid(serializer.data)

        return Response(data)
    
class JobDetailAPIView(APIView):

    def get(self, request, slug):

        job = ChildJobPosition.objects.prefetch_related(
            "descriptions",
            "skills"
        ).get(slug=slug)

        serializer = ChildJobPositionSerializer(job)

        return Response(serializer.data)
    
@api_view(['GET'])
def about_page_api(request):
    from website.models import AboutPageContent, AboutUsServeItem
    content = AboutPageContent.objects.first()

    if not content:
        content = AboutPageContent.objects.create()

    # Build response format expected by frontend
    data = {"sections": []}

    # Helper for image URL
    def get_img_url(img_field):
        return request.build_absolute_uri(img_field.url) if img_field else None

    # Hero
    data["sections"].append({
        "name": "hero",
        "title": content.hero_title,
        "subtitle": content.hero_description,
        "items": []
    })

    # About
    about_items = []
    for i, desc in enumerate([content.about_description_1, content.about_description_2, content.about_description_3]):
        if desc: about_items.append({"id": i, "description": desc})
        
    data["sections"].append({
        "name": "about",
        "title": content.about_heading,
        "subtitle": "", # not used
        "image": get_img_url(content.about_image),
        "items": about_items
    })

    # Mission
    data["sections"].append({
        "name": "mission",
        "title": content.mission_title,
        "subtitle": content.mission_description,
        "items": []
    })

    # Why Choose (Only Dynamic CRUD)
    why_items = []
    
    # Dynamic points
    from website.models import AboutUsWhyChooseItem
    for w_item in AboutUsWhyChooseItem.objects.filter(about_page=content, is_active=True).order_by('order'):
        why_items.append({
            "id": str(w_item.id),
            "title": w_item.title
        })

    data["sections"].append({
        "name": "why_choose",
        "title": content.why_choose_title,
        "items": why_items
    })

    # Serve
    serve_items = []
    for s_item in AboutUsServeItem.objects.filter(is_active=True).order_by('order'):
        serve_items.append({
            "id": str(s_item.id),
            "title": s_item.title,
            "image": get_img_url(s_item.image)
        })

    data["sections"].append({
        "name": "serve",
        "title": content.serve_title,
        "subtitle": content.serve_subtitle,
        "items": serve_items
    })

    # CTA
    data["sections"].append({
        "name": "cta",
        "title": content.cta_title,
        "subtitle": content.cta_description,
        "items": [{"id": 1, "title": content.cta_button_text}]
    })

    return Response(data)

class PolicyListAPIView(APIView):
    def get(self, request):
        policies = Policy.objects.all()
        serializer = PolicySerializer(policies, many=True)

        data = convert_objectid(serializer.data)

        return Response(data)


class PolicyDetailAPIView(APIView):
    def get(self, request, slug):
        try:
            policy = Policy.objects.get(slug=slug)
        except Policy.DoesNotExist:
            return Response({"error": "Not found"}, status=404)

        serializer = PolicySerializer(policy)

        # ✅ FIX HERE
        data = convert_objectid(serializer.data)

        return Response(data)