from website.models import DemoRequest,UserLogin, ReferralUser
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import APIView, api_view
from rest_framework.response import Response
from rest_framework import status
from .models import FAQ, ComparisonFeature, ContactPageContent, ContactSubmission, Feature, HowItWorksStep, PricingSignup, LandingPageContent, Payment, PricingSignup, AdminUser, AboutPageContent, CareerPageContent, Problem, ReferralPerk, StoreType, Testimonial, USPFeature
from .serializers import AboutPageSerializer, CareerPageSerializer, ComparisonFeatureSerializer, FAQSerializer, LandingPageContentSerializer,JobApplicationSerializer,ReferralUserSerializer, ContactPageContentSerializer
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

    # ❌ Prevent duplicate signup
    if PricingSignup.objects.filter(mobile_number=mobile_number).exists():
        return Response({
            "error": "This mobile number already registered"
        }, status=400)

    generated_code = None

    # ✔ Check if user came from referral popup
    referral_user = ReferralUser.objects.filter(
        mobile_number=mobile_number
    ).first()

    if referral_user:
        generated_code = referral_user.referral_code
    else:
        generated_code = ''.join(random.choices(
            string.ascii_uppercase + string.digits, k=6
        ))

    # ✔ Increase referral count
    if referral_code_input:
        try:
            ref_user = PricingSignup.objects.get(referral_code=referral_code_input)
            ref_user.total_referrals += 1
            ref_user.save()
        except PricingSignup.DoesNotExist:
            pass

    signup = PricingSignup.objects.create(
        shop_name=shop_name,
        owner_name=owner_name,
        mobile_number=mobile_number,
        referral_code=generated_code
    )

    return Response({
        "message": "Signup successful",
        "referral_code": generated_code,
        "signup_id": str(signup.id)
    }, status=status.HTTP_201_CREATED)  

from rest_framework import status
from .models import ContactSubmission, PricingSignup, LandingPageContent
from django.views.decorators.csrf import csrf_exempt

from .models import PricingSignup


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
        return Response({"message": "Application submitted successfully"})

    return Response(serializer.errors)

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

# MERCHANT_ID = "PGTESTPAYUAT"
# SALT_KEY = "099eb0cd-02cf-4e2a-8aca-3e6c6aff0399"
# SALT_INDEX = "1"

@csrf_exempt
@api_view(["POST"])
def initiate_payment(request):
    try:
        signup_id = request.data.get("signup_id")
        amount = request.data.get("amount")

        if not signup_id:
            return Response({"error": "signup_id is missing"}, status=400)
        if not amount:
            return Response({"error": "amount is missing"}, status=400)

        signup = PricingSignup.objects.filter(id=signup_id).first()
        if not signup:
            # This is a common cause for 400/404 errors
            return Response({"error": f"Signup with ID {signup_id} not found"}, status=400)

        # -------------------------------
        # Validate Merchant Keys
        # -------------------------------
        if not getattr(settings, "PHONEPE_MERCHANT_ID", None) or \
           not getattr(settings, "PHONEPE_SALT_KEY", None) or \
           not getattr(settings, "PHONEPE_SALT_INDEX", None) or \
           not getattr(settings, "PHONEPE_BASE_URL", None):
            return Response({"error": "PhonePe merchant keys not configured"}, status=500)

        print("Merchant ID:", settings.PHONEPE_MERCHANT_ID)
        print("Salt Index:", settings.PHONEPE_SALT_INDEX)

        payment = Payment.objects.create(
            pricing_signup=signup,
            amount=amount
        )

        # -------------------------------
        # Prepare Payload
        # -------------------------------
        payload = {
            "merchantId": settings.PHONEPE_MERCHANT_ID,
            "merchantTransactionId": str(payment.transaction_id),
            "merchantUserId": str(signup.id),
            "amount": int(amount) * 100,  # in paise
            "redirectUrl": "http://localhost:8000/payment-success/",
            "redirectMode": "POST",
            "callbackUrl": "http://localhost:8000/payment-callback/",
            "paymentInstrument": {
                "type": "PAY_PAGE"
            }
        }
        print("Payment Payload:", payload)
        payload_base64 = base64.b64encode(json.dumps(payload).encode()).decode()

        # -------------------------------
        # Generate Checksum
        # -------------------------------
        string = payload_base64 + "/pg/v1/pay" + settings.PHONEPE_SALT_KEY
        sha256 = hashlib.sha256(string.encode()).hexdigest()
        checksum = sha256 + "###" + str(settings.PHONEPE_SALT_INDEX)

        headers = {
            "Content-Type": "application/json",
            "X-VERIFY": checksum
        }

        url = settings.PHONEPE_BASE_URL + "/pg/v1/pay"

        print("Request URL:", url)
        # -------------------------------
        # Make Request to PhonePe
        # -------------------------------
        phonepe_response = requests.post(
            url,
            json={"request": payload_base64},
            headers=headers,
            timeout=15
        )

        phonepe_data = phonepe_response.json()
        print("PhonePe Response:", phonepe_data)

        if not phonepe_data.get("success"):
            return Response({
                "error": phonepe_data.get("message", "Payment failed")
            }, status=400)

        payment_url = phonepe_data["data"]["instrumentResponse"]["redirectInfo"]["url"]

        print("Payment URL:", payment_url)

        return Response({
            "payment_url": payment_url
        })

    except Exception as e:
        print("Payment Error:", str(e))
        return Response({
            "error": "Internal server error",
            "details": str(e)
        }, status=500)

# -------------------------------
# PhonePe Callback
# -------------------------------
@csrf_exempt
def payment_callback(request):
    try:
        data = json.loads(request.body)
        transaction_id = data["data"]["merchantTransactionId"]

        payment = Payment.objects.get(transaction_id=transaction_id)
        payment.status = "SUCCESS"
        payment.save()

        return JsonResponse({"message": "Payment verified"})

    except Payment.DoesNotExist:
        return JsonResponse({"error": "Payment not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": "Internal server error", "details": str(e)}, status=500)
    
@api_view(["GET"])
def about_page_content(request):
    # Use .first() to get the object, not a queryset
    content = AboutPageContent.objects.first()

    if not content:
        # Create default if it doesn't exist
        content = AboutPageContent.objects.create()

    serializer = AboutPageSerializer(content)
    return Response(serializer.data)

@api_view(["GET"])
def career_page_content(request):
    # Fetch the ONLY record
    content = CareerPageContent.objects.first()

    if not content:
        # Only happens the very first time
        content = CareerPageContent.objects.create()
    
    serializer = CareerPageSerializer(content)
    return Response(serializer.data)



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

    problems = Problem.objects.filter(is_active=True)

    data = []

    for p in problems:
        data.append({
            "title": p.title,
            "description": p.description,
            "icon": p.icon
        })

    return Response(data)


@api_view(["GET"])
def get_features(request):

    features = Feature.objects.filter(is_active=True)

    data = []

    for f in features:
        data.append({
            "title": f.title,
            "description": f.description,
            "icon": f.icon
        })

    return Response(data)

@api_view(["GET"])
def get_usp_features(request):

    features = USPFeature.objects.filter(is_active=True)

    data = []

    for f in features:
        data.append({
            "title": f.title,
            "description": f.description,
            "icon": f.icon
        })

    return Response(data)

@api_view(["GET"])
def get_how_it_works_steps(request):

    steps = HowItWorksStep.objects.filter(is_active=True)

    data = []

    for s in steps:

        data.append({
            "title": s.title,
            "description": s.description,
            "icon": s.icon,
            "step_number": s.step_number
        })

    return Response(data)

@api_view(["GET"])
def get_store_types(request):

    stores = StoreType.objects.filter(is_active=True)

    data = []

    for s in stores:
        data.append({
            "title": s.title,
            "icon": s.icon
        })

    return Response(data)

@api_view(["GET"])
def get_referral_perks(request):

    perks = ReferralPerk.objects.filter(is_active=True)

    data = []

    for p in perks:
        data.append({
            "value": p.value,
            "text": p.text,
            "icon": p.icon
        })

    return Response(data)

@api_view(["GET"])
def get_home_testimonials(request):

    testimonials = Testimonial.objects.filter(is_active=True)[:3]

    data = []

    for t in testimonials:

        data.append({
            "name": t.name,
            "role": t.role,
            "text": t.review,
            "rating": t.rating,
            "image": request.build_absolute_uri(t.image.url) if t.image else None
        })

    return Response(data)

@api_view(["GET"])
def get_all_testimonials(request):

    testimonials = Testimonial.objects.filter(is_active=True)

    data = []

    for t in testimonials:

        data.append({
            "name": t.name,
            "role": t.role,
            "text": t.review,
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