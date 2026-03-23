import os
import django
from rest_framework.test import APIRequestFactory

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aisetu_erp.settings')
django.setup()

from website.views import get_how_it_works_steps, landing_page_content_api

factory = APIRequestFactory()

try:
    # Test how-it-works API
    request = factory.get('/api/how-it-works/')
    response = get_how_it_works_steps(request)
    print("How-It-Works API Response Status:", response.status_code)
    print("How-It-Works API Data:", response.data)
    
    # Test landing-content API
    request = factory.get('/api/landing-content/')
    response = landing_page_content_api(request)
    print("Landing-Content API Response Status:", response.status_code)
    if 'howitworks_steps' in response.data:
        print("Landing-Content contains howitworks_steps:", len(response.data['howitworks_steps']))
except Exception as e:
    print("ERROR:", e)
    import traceback
    traceback.print_exc()
