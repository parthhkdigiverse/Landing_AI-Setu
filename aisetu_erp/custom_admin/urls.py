from django.urls import path
from . import views

app_name = 'custom_admin'

urlpatterns = [
    path('', views.dashboard, name='admin_root'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('singleton/<str:model_name>/', views.edit_singleton, name='edit_singleton'),
    path('page-sections/<str:page_type>/', views.page_sections, name='page_sections'),
    path('toggle-section-visibility/', views.toggle_section_visibility, name='toggle_section_visibility'),
    
    # Generic CRUD paths
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('<str:app_label>/<str:model_name>/', views.CustomAdminListView.as_view(), name='model_list'),
    path('<str:app_label>/<str:model_name>/add/', views.CustomAdminCreateView.as_view(), name='model_create'),
    path('<str:app_label>/<str:model_name>/<slug:pk>/change/', views.CustomAdminUpdateView.as_view(), name='model_update'),
    path('<str:app_label>/<str:model_name>/<slug:pk>/delete/', views.CustomAdminDeleteView.as_view(), name='model_delete'),
]
