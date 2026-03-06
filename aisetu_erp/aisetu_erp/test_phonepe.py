import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000"

def test_initiate_payment():
    print("Testing /api/phonepe/initiate/")
    url = f"{BASE_URL}/api/phonepe/initiate/"
    payload = {
        "amount": 100,  # 100 Rupees
        "phone": "9999999999"
    }
    headers = {
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    return response.json()

if __name__ == "__main__":
    result = test_initiate_payment()
    if 'payment_url' in result:
        print("\nSuccess! Payment URL received.")
        print(f"URL: {result['payment_url']}")
        print(f"Merchant Transaction ID: {result['merchant_transaction_id']}")
    else:
        print("\nFailed to get payment URL.")
