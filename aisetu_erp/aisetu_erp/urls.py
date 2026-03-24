"""
URL configuration for aisetu_erp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import re_path,path, include
from website.views import serve_frontend_with_seo
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('custom-admin/', include('custom_admin.urls')),
    path('', include('website.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Catch-all route for frontend routing (React) - MUST BE LAST
# We use serve_frontend_with_seo to inject dynamic meta tags for blog posts and other pages
urlpatterns.append(re_path(r'^blog/(?P<slug>[\w-]+)/?$', serve_frontend_with_seo))
urlpatterns.append(re_path(r'^.*$', serve_frontend_with_seo))