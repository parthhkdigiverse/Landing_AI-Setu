import os
import django
import sys

# Setup Django environment
sys.path.append('f:/Projects/Landing_AI-Setu/aisetu_erp')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aisetu_erp.settings')
django.setup()

from website.models import Payment
from uuid import UUID

def check_payment(tid_str):
    print(f"Checking payment for ID: {tid_str}")
    try:
        tid_uuid = UUID(tid_str)
        payment = Payment.objects.get(transaction_id=tid_uuid)
        print(f"Found Payment: ID={payment.id}, Status={payment.status}")
        print(f"Response Data: {payment.response_data}")
        return True
    except Payment.DoesNotExist:
        print(f"Payment with transaction_id {tid_str} NOT FOUND.")
    except Exception as e:
        print(f"Error: {e}")
    return False

if __name__ == "__main__":
    # Test with one of the PENDING IDs from the user's screenshot
    check_payment("1f60d5ca-7c35-48e7-b293-5d5940ea6e54")
    # Test with the SUCCESS ID
    check_payment("19d73c7f-d63f-40c7-941d-716536a3cab0")
