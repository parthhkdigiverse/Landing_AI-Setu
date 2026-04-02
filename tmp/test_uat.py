import requests
import hashlib
import json
import base64

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

hash_ep = "/pg/v1/pay"
string = payload_base64 + hash_ep + salt_key
sha256 = hashlib.sha256(string.encode()).hexdigest()
checksum = sha256 + "###" + salt_index

headers = {
    "Content-Type": "application/json",
    "X-VERIFY": checksum
}

url = "https://api-preprod.phonepe.com/apis/pg-sandbox/pg/v1/pay"

resp = requests.post(url, json={"request": payload_base64}, headers=headers, timeout=5)
print(f"UAT Status: {resp.status_code}")
print(f"Response: {resp.text}")

