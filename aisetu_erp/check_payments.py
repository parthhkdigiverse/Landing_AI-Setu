import os
import django
import sys

# Add the project directory to sys.path
sys.path.append(r'f:\Projects\Landing_AI-Setu\aisetu_erp')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aisetu_erp.settings')
django.setup()

from website.models import Payment

payments = Payment.objects.order_by('-created_at')[:5]
for p in payments:
    print(f"ID: {p.id}")
    print(f"TID: {p.transaction_id}")
    print(f"Status: {p.status}")
    print(f"Response Data: {p.response_data}")
    print("-" * 20)
