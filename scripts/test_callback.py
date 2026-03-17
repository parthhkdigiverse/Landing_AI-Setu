import requests
import json
import base64

# Use the transaction ID found in the database
TRANSACTION_ID = "20169fe6-74df-4869-9d61-7928678952ff"
CALLBACK_URL = "http://localhost:8000/payment-callback/"

def test_callback():
    # Prepare the payload PhonePe usually sends
    payload_data = {
        "success": True,
        "code": "PAYMENT_SUCCESS",
        "message": "Payment successful",
        "data": {
            "merchantId": "PGTESTPAYUAT",
            "merchantTransactionId": TRANSACTION_ID,
            "transactionId": "T2403161525000001",
            "amount": 1416000,
            "state": "COMPLETED",
            "responseCode": "SUCCESS"
        }
    }
    
    # Base64 encode the payload as PhonePe does
    payload_json = json.dumps(payload_data)
    payload_base64 = base64.b64encode(payload_json.encode()).decode()
    
    # Send the POST request
    response = requests.post(
        CALLBACK_URL,
        json={"response": payload_base64}
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.json()}")

if __name__ == "__main__":
    test_callback()
