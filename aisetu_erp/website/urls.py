from django.urls import path
from .views import book_demo_api,login_view,pricing_signup, landing_page_content_api, submit_contact, apply_job, check_referral
from . import views 
urlpatterns = [    
    path("book-demo/", book_demo_api, name="book_demo_api"),
    path('api/login/', login_view, name='login_view'),
    path('pricing-signup/', pricing_signup, name='pricing_signup'),
    path('api/landing-content/', landing_page_content_api, name='landing_page_content_api'),
    path("api/contact/submit/", submit_contact, name="submit_contact"),
    path("apply-job/", apply_job, name="apply_job"),
    path('referral-check/', check_referral, name='check_referral'),
    path("phonepe/initiate/", initiate_payment, name="initiate_payment"),
    path("payment-callback/", payment_callback, name="payment_callback"),
]