import requests
import json
import base64

# Add IDs here to test them all
TRANSACTION_IDS = [
    "1f60d5ca-7c35-48e7-b293-5d5940ea6e54",
    "19d73c7f-d63f-40c7-941d-716536a3cab0"
]
CALLBACK_URL = "http://127.0.0.1:8000/payment-callback/"

def test_callback(tid, use_form_data=False):
    print(f"Testing ID: {tid} | Format: {'Form Data' if use_form_data else 'JSON Body'}...")
    # Prepare the payload PhonePe usually sends
    payload_data = {
        "success": True,
        "code": "PAYMENT_SUCCESS",
        "message": "Payment successful",
        "data": {
            "merchantId": "PGTESTPAYUAT",
            "merchantTransactionId": tid,
            "transactionId": f"T{tid[:8].upper()}",
            "amount": 1416000,
            "state": "COMPLETED",
            "responseCode": "SUCCESS"
        }
    }
    
    # Base64 encode the payload as PhonePe does
    payload_json = json.dumps(payload_data)
    payload_base64 = base64.b64encode(payload_json.encode()).decode()
    
    if use_form_data:
        response = requests.post(CALLBACK_URL, data={"response": payload_base64})
    else:
        response = requests.post(CALLBACK_URL, json={"response": payload_base64})
    
    print(f"Status: {response.status_code} | Response: {response.json().get('message')}")

if __name__ == "__main__":
    for tid in TRANSACTION_IDS:
        test_callback(tid, use_form_data=False)
        print("-" * 20)
        # test_callback(tid, use_form_data=True) # Optional form data check
