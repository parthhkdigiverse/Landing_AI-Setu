import requests

client_id = "SU2502131201315075436273"
client_secret = "e3ae70f4-eb93-445a-a35a-d074e9060435"
client_version = "1"

# The standard V2 OAuth token endpoints
urls = [
    "https://api.phonepe.com/apis/hermes/v1/oauth/token",
    "https://api.phonepe.com/apis/pg/v1/oauth/token",
    "https://api.phonepe.com/v1/oauth/token"
]

for url in urls:
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    data = {
        "client_id": client_id,
        "client_version": client_version,
        "client_secret": client_secret,
        "grant_type": "client_credentials"
    }
    
    print(f"Testing Oauth at: {url}")
    try:
        resp = requests.post(url, data=data, headers=headers, timeout=5)
        print(f"Status: {resp.status_code}")
        print(f"Response: {resp.text}\n")
    except Exception as e:
        pass
