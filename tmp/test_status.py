import requests
import hashlib
import json

merchant_id = "SU2502131201315075436273"
salt_key = "e3ae70f4-eb93-445a-a35a-d074e9060435"
salt_index = "1"
merchant_transaction_id = "TEST-12345"

urls = [
    "https://api.phonepe.com/apis/pg/v1/status",
    "https://api.phonepe.com/apis/pg/pg/v1/status",
    "https://api.phonepe.com/apis/hermes/pg/v1/status"
]

for base_url in urls:
    ep = f"/{merchant_id}/{merchant_transaction_id}"
    url = base_url + ep
    
    hash_ep1 = f"/pg/v1/status/{merchant_id}/{merchant_transaction_id}"
    hash_ep2 = f"/v1/status/{merchant_id}/{merchant_transaction_id}"
    
    for hash_ep in [hash_ep1, hash_ep2]:
        string = hash_ep + salt_key
        sha256 = hashlib.sha256(string.encode()).hexdigest()
        checksum = sha256 + "###" + salt_index
        
        headers = {
            "Content-Type": "application/json",
            "X-VERIFY": checksum,
            "X-MERCHANT-ID": merchant_id
        }
        
        try:
            resp = requests.get(url, headers=headers, timeout=5)
            print(f"Status URL: {url} | Hash EP: {hash_ep} -> Code: {resp.status_code}")
        except Exception as e:
            pass
