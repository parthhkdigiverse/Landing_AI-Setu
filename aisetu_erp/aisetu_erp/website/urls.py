from django.urls import path
from .views import book_demo_api,login_view,pricing_signup, phonepe_initiate_payment, phonepe_callback

urlpatterns = [    
    path("book-demo/", book_demo_api, name="book_demo_api"),
    path('api/login/', login_view, name='login_view'),
    path('pricing-signup/', pricing_signup, name='pricing_signup'),
    path('api/phonepe/initiate/', phonepe_initiate_payment, name='phonepe_initiate_payment'),
    path('api/phonepe/callback/', phonepe_callback, name='phonepe_callback'),
]