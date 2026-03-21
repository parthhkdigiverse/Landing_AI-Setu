from django.urls import path
from . import views

app_name = 'custom_admin'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('<str:app_label>/<str:model_name>/', views.CustomAdminListView.as_view(), name='model_list'),
    path('<str:app_label>/<str:model_name>/add/', views.CustomAdminCreateView.as_view(), name='model_create'),
    path('<str:app_label>/<str:model_name>/<slug:pk>/change/', views.CustomAdminUpdateView.as_view(), name='model_update'),
    path('<str:app_label>/<str:model_name>/<slug:pk>/delete/', views.CustomAdminDeleteView.as_view(), name='model_delete'),
]
