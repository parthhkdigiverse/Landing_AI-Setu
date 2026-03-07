from django.urls import path
from .views import book_demo_api,login_view,pricing_signup, phonepe_initiate_payment, phonepe_callback, landing_page_content_api, submit_contact, apply_job
from . import views 
urlpatterns = [    
    path("book-demo/", book_demo_api, name="book_demo_api"),
    path('api/login/', login_view, name='login_view'),
    path('pricing-signup/', pricing_signup, name='pricing_signup'),
    path('api/phonepe/initiate/', phonepe_initiate_payment, name='phonepe_initiate_payment'),
    path('api/phonepe/callback/', phonepe_callback, name='phonepe_callback'),
    path('api/landing-content/', landing_page_content_api, name='landing_page_content_api'),
    path("api/contact/submit/", submit_contact, name="submit_contact"),
    path("apply-job/", apply_job, name="apply_job"),
]