from django.core.mail.backends.smtp import EmailBackend
from django.conf import settings
from .models import GlobalSettings

class DynamicEmailBackend(EmailBackend):
    def __init__(self, host=None, port=None, username=None, password=None,
                 use_tls=None, fail_silently=False, use_ssl=None, timeout=None,
                 ssl_keyfile=None, ssl_certfile=None, **kwargs):
        
        # Try to get credentials from Database (GlobalSettings singleton)
        db_username = username
        db_password = password
        
        try:
            # We use .first() because it's a singleton pattern
            global_settings = GlobalSettings.objects.first()
            if global_settings:
                if global_settings.email_host_user:
                    db_username = global_settings.email_host_user
                if global_settings.email_host_password:
                    db_password = global_settings.email_host_password
        except Exception as e:
            # Fallback to settings.py / env if DB is not ready or migration is pending
            pass

        super().__init__(
            host=host or getattr(settings, 'EMAIL_HOST', 'smtp.gmail.com'),
            port=port or getattr(settings, 'EMAIL_PORT', 587),
            username=db_username or getattr(settings, 'EMAIL_HOST_USER', None),
            password=db_password or getattr(settings, 'EMAIL_HOST_PASSWORD', None),
            use_tls=use_tls or getattr(settings, 'EMAIL_USE_TLS', True),
            fail_silently=fail_silently,
            use_ssl=use_ssl or getattr(settings, 'EMAIL_USE_SSL', False),
            timeout=timeout,
            ssl_keyfile=ssl_keyfile,
            ssl_certfile=ssl_certfile,
            **kwargs
        )
