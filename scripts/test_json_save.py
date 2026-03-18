import os
import django
import sys
import json

# Setup Django environment
sys.path.append('f:/Projects/Landing_AI-Setu/aisetu_erp')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aisetu_erp.settings')
django.setup()

from website.models import Payment
from uuid import UUID

def test_json_save(tid_str):
    print(f"Testing JSON save for ID: {tid_str}")
    try:
        tid_uuid = UUID(tid_str)
        payment = Payment.objects.get(transaction_id=tid_uuid)
        test_data = {"test": "data", "status": "success", "val": 123}
        payment.response_data = test_data
        payment.save()
        
        # Refetch
        payment.refresh_from_db()
        print(f"Refetched Response Data: {payment.response_data}")
        if payment.response_data == test_data:
            print("SUCCESS: JSON stored correctly.")
        else:
            print("FAILURE: JSON not stored correctly.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Test with the SUCCESS ID
    test_json_save("19d73c7f-d63f-40c7-941d-716536a3cab0")
