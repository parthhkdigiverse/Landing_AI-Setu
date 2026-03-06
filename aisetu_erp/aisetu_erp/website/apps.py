from django.apps import AppConfig


class WebsiteConfig(AppConfig):
    default_auto_field = 'django_mongodb_backend.fields.ObjectIdAutoField'
    name = 'website'
