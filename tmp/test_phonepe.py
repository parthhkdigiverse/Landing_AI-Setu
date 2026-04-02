import requests
import hashlib
import base64
import json

base_urls = [
    "https://api.phonepe.com/apis/pg",
    "https://api.phonepe.com/apis/hermes"
]
endpoints = [
    "/pg/v1/pay",
    "/v1/pay"
]

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

for base in base_urls:
    for ep in endpoints:
        for hash_ep in ["/pg/v1/pay", "/v1/pay"]:
            # Construct URL cleanly
            url = base.rstrip('/')
            if url.endswith('/pg') and ep == '/pg/v1/pay':
                url = url + "/v1/pay" # dedup
            else:
                url = url + ep
            
            # Construct Hash cleanly
            string = payload_base64 + hash_ep + salt_key
            sha256 = hashlib.sha256(string.encode()).hexdigest()
            checksum = sha256 + "###" + salt_index
            
            headers = {
                "Content-Type": "application/json",
                "X-VERIFY": checksum
            }
            
            try:
                resp = requests.post(url, json={"request": payload_base64}, headers=headers, timeout=5)
                print(f"Testing URL: {url} | Hash EP: {hash_ep}")
                print(f"Status Code: {resp.status_code}")
                print(f"Response: {resp.text}\n")
            except Exception as e:
                pass

