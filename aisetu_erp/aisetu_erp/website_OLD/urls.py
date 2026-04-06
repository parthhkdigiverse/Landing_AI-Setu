from django.urls import path
from .views import book_demo_api,login_view,pricing_signup, submit_contact
from . import views
urlpatterns = [    
    path("book-demo/", book_demo_api, name="book_demo_api"),
    path('api/login/', login_view, name='login_view'),
    path('pricing-signup/', pricing_signup, name='pricing_signup'),
    # path("api/contact/submit/", submit_contact, name="contact_submit"),
    # path("contact/submit/", views.submit_contact, name="submit_contact"),
]