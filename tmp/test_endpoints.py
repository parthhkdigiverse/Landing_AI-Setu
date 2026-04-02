import requests
import hashlib
import base64
import json

merchant_id = "SU2502131201315075436273"
salt_key = "e3ae70f4-eb93-445a-a35a-d074e9060435"
salt_index = "1"

payload = {
  "merchantId": merchant_id,
  "merchantTransactionId": "TEST-12345",
  "merchantUserId": "MUID123",
  "amount": 100,
  "redirectUrl": "https://webhook.site/redirect",
  "redirectMode": "REDIRECT",
  "callbackUrl": "https://webhook.site/callback",
  "paymentInstrument": {
    "type": "PAY_PAGE"
  }
}

payload_json = json.dumps(payload, separators=(',', ':'))
payload_base64 = base64.b64encode(payload_json.encode()).decode()

endpoints = [
    # Variations of apis/pg
    ("https://api.phonepe.com/apis/pg/v1/pay", "/v1/pay"),
    ("https://api.phonepe.com/apis/pg/v1/pay", "/pg/v1/pay"),
    ("https://api.phonepe.com/apis/pg/pg/v1/pay", "/pg/v1/pay"),
    ("https://api.phonepe.com/apis/pg/pg/v1/pay", "/pg/pg/v1/pay"),
    
    # Variations of apis/hermes
    ("https://api.phonepe.com/apis/hermes/v1/pay", "/v1/pay"),
    ("https://api.phonepe.com/apis/hermes/v1/pay", "/pg/v1/pay"),
    ("https://api.phonepe.com/apis/hermes/pg/v1/pay", "/v1/pay"),
    ("https://api.phonepe.com/apis/hermes/pg/v1/pay", "/pg/v1/pay"),
    
    # Root level?
    ("https://api.phonepe.com/pg/v1/pay", "/pg/v1/pay"),
    ("https://api.phonepe.com/v1/pay", "/v1/pay")
]

for url, hash_ep in endpoints:
    string = payload_base64 + hash_ep + salt_key
    sha256 = hashlib.sha256(string.encode()).hexdigest()
    checksum = sha256 + "###" + salt_index
    
    headers = {
        "Content-Type": "application/json",
        "X-VERIFY": checksum
    }
    
    try:
        resp = requests.post(url, json={"request": payload_base64}, headers=headers, timeout=5)
        print(f"URL: {url} | Hash EP: {hash_ep} -> Code: {resp.status_code}")
        # print(f"  {resp.text.strip()}")
    except Exception as e:
        pass
