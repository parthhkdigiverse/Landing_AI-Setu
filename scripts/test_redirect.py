import requests
import base64
import json

# Use a PENDING ID from the user's screenshot
TRANSACTION_ID = "1f60d5ca-7c35-48e7-b293-5d5940ea6e54"
REDIRECT_URL = "http://127.0.0.1:8000/payment-success/"

def test_redirect():
    print(f"Testing redirect for ID: {TRANSACTION_ID}...")
    
    # Mock PhonePe response payload
    payload_data = {
        "success": True,
        "code": "PAYMENT_SUCCESS",
        "message": "Payment successful",
        "data": {
            "merchantId": "PGTESTPAYUAT86",
            "merchantTransactionId": TRANSACTION_ID,
            "transactionId": "T2403180950000001",
            "amount": 1416000,
            "state": "COMPLETED",
            "responseCode": "SUCCESS"
        }
    }
    
    # Base64 encode
    payload_json = json.dumps(payload_data)
    payload_base64 = base64.b64encode(payload_json.encode()).decode()
    
    # Send POST request (as PhonePe would with redirectMode: POST)
    print("Sending POST request to redirect URL...")
    response = requests.post(
        REDIRECT_URL,
        data={"response": payload_base64},
        allow_redirects=False # We want to see the 302
    )
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 302:
        print(f"Redirect Location: {response.headers.get('Location')}")
    else:
        print(f"Response: {response.text[:500]}")

if __name__ == "__main__":
    test_redirect()
