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
from .models import FAQ, AllStoreType, CareerPage, ChildJobPosition, ComparisonFeature, ContactPageContent, ContactSubmission, DemoVideo, Feature, Footer, GlobalSettings, HowItWorksStep, JobPosition, LoginLink, Page, Policy, PricingSignup, LandingPageContent, Payment, AdminUser, Problem, ReferralPerk, StoreType, Testimonial, USPFeature, BlogCategory, BlogPost
import razorpay
from django.conf import settings
import requests
import uuid
import base64
from .serializers import AllStoreTypeSerializer, CareerPageSerializer, ChildJobPositionSerializer, ComparisonFeatureSerializer, FAQSerializer, JobPositionSerializer, LandingPageContentSerializer,JobApplicationSerializer, LoginLinkSerializer, PageSerializer, PolicySerializer,ReferralUserSerializer, ContactPageContentSerializer, BlogCategorySerializer, BlogPostSerializer, FooterSerializer
import logging
from .services.payment_service import PaymentService

logger = logging.getLogger('website')

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


@api_view(["POST"])
@permission_classes([AllowAny])
def book_demo_api(request):
    try:
        data = request.data

        name = data.get("name")
        contact_number = data.get("contact_number")     
        store_type = data.get("store_type")      
        city = data.get("city")

        if not all([name, contact_number, store_type, city]):
            return Response({"error": "All fields required"}, status=400)

        DemoRequest.objects.create(
            name=name,
            contact_number=contact_number,
            store_type=store_type,
            city=city,
        )

        return Response({"message": "Demo request saved successfully"}, status=201)

    except Exception as e:
        return Response({"error": str(e)}, status=400)

@csrf_exempt
def user_login(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')

            if not all([email, password]):
                return JsonResponse({"error": "All fields required"}, status=400)

            # Store the login attempt in the UserLogin model, not DemoRequest
            UserLogin.objects.create(
                email=email,
                password=password,
            )

            return JsonResponse({"message": "Login successfully"}, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Only POST allowed"}, status=405)

def serve_frontend_with_seo(request, slug=None):
    logger.info(f"FALLBACK HIT: path={request.path}, method={request.method}")
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
@permission_classes([AllowAny])
def pricing_signup(request):
    shop_name = request.data.get('shop_name')
    owner_name = request.data.get('owner_name')
    mobile_number = request.data.get('mobile_number')
    email = request.data.get('email')
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
        email=email,
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
@permission_classes([AllowAny])
def apply_job(request):

    serializer = JobApplicationSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Application submitted successfully"}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def check_referral(request):

    logger.info(f"Incoming check_referral data: {request.data}")

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

@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
@authentication_classes([])
def initiate_payment(request):
    """
    Unified Payment Initiation (Razorpay Only)
    """
    logger.info(f"PAYMENT INITIATION HIT: data={request.data}")
    try:
        signup_id = request.data.get("signup_id")
        amount_val = request.data.get("amount")

        if not signup_id or not amount_val:
            return Response({"error": "signup_id or amount is missing"}, status=400)

        signup = PricingSignup.objects.filter(id=signup_id).first()
        if not signup:
            return Response({"error": f"Signup with ID {signup_id} not found"}, status=400)

        payment_data = PaymentService.initiate_payment_link(signup, amount_val)
        return Response(payment_data)

    except Exception as e:
        logger.error(f"General Initiation Error: {e}", exc_info=True)
        return Response({"error": str(e)}, status=500)

@csrf_exempt
def razorpay_callback(request):
    """
    Razorpay Webhook/Callback
    """
    import json
    
    if request.method == "POST":
        # Handle Webhook from Razorpay
        try:
            payload = json.loads(request.body)
            PaymentService.process_webhook(payload)
            return JsonResponse({"status": "ok"})
        except Exception as e:
            logger.error(f"Razorpay Webhook Error: {e}", exc_info=True)
            return JsonResponse({"error": str(e)}, status=400)

    # 1. Check for GET params from redirect (though payment_success handles this)
    razorpay_payment_id = request.GET.get('razorpay_payment_id')
    logger.info(f"Razorpay GET Callback received for payment_id={razorpay_payment_id}")
    
    return JsonResponse({"status": "received"})

@csrf_exempt
def payment_success(request):
    """
    Handle the redirect from Payment Gateway. Extract status and redirect/render.
    """
    from django.shortcuts import redirect, render

    logger.info(f"--- PAYMENT REDIRECT FROM PG --- Params: {request.GET.dict()}")

    # 1. Check if this is an internal redirect (we've already processed it)
    if request.GET.get('status'):
        return render(request, "index.html")
    
    # Razorpay Success Parameters
    razorpay_payment_id = request.GET.get('razorpay_payment_id')
    merchant_transaction_id = request.GET.get('merchantTransactionId') or request.GET.get('tid')
    gateway = request.GET.get('gateway', 'RAZORPAY')

    tid = merchant_transaction_id or "UNKNOWN"

    frontend_status = PaymentService.verify_and_update_status(razorpay_payment_id, tid, gateway=gateway)

    return redirect(f"/payment-success/?status={frontend_status}&tid={tid}&gateway={gateway}")

@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
def cashfree_webhook(request):
    """
    Cashfree Webhook for asynchronous status updates.
    """
    try:
        # Cashfree sends payload in the body
        payload = request.data
        logger.info(f"CASHFREE WEBHOOK RECEIVED: {payload}")
        
        PaymentService.process_webhook(payload, gateway="CASHFREE")
        return Response({"status": "OK"}, status=200)
    except Exception as e:
        logger.error(f"Cashfree Webhook Error: {e}", exc_info=True)
        return Response({"error": str(e)}, status=400)

@api_view(["GET"])
@permission_classes([AllowAny])
def check_payment_status_api(request, tid):
    """
    API for frontend to poll payment status.
    """
    try:
        from uuid import UUID
        payment = Payment.objects.get(transaction_id=UUID(tid))
        
        return Response({
            "status": payment.status,
            "transaction_id": str(payment.transaction_id),
            "amount": payment.amount,
            "invoice_url": request.build_absolute_uri(payment.invoice.url) if payment.invoice else None
        })
    except (Payment.DoesNotExist, ValueError):
        return Response({"status": "NOT_FOUND", "error": "Payment not found"}, status=404)
    
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
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
def all_store_type(request):

    stores = AllStoreType.objects.filter(is_active=True).order_by("name")

    serializer = AllStoreTypeSerializer(stores, many=True)

    return Response(serializer.data)

@api_view(["GET"])
@permission_classes([AllowAny])
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