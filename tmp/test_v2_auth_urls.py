import requests

client_id = "SU2502131201315075436273"
client_secret = "e3ae70f4-eb93-445a-a35a-d074e9060435"
client_version = "1"

urls = [
    "https://api.phonepe.com/apis/pg/v3/auth/token",
    "https://api.phonepe.com/apis/hermes/v3/auth/token",
    "https://api.phonepe.com/apis/pg/oauth/token",
    "https://api.phonepe.com/apis/hermes/oauth/token",
    "https://api.phonepe.com/auth/v2/oauth/token",
    "https://api.phonepe.com/apis/merchant-simulator/v1/oauth/token"
]

data = {
    "client_id": client_id,
    "client_version": client_version,
    "client_secret": client_secret,
    "grant_type": "client_credentials"
}

headers = {"Content-Type": "application/x-www-form-urlencoded"}

for url in urls:
    try:
        resp = requests.post(url, data=data, headers=headers, timeout=2)
        print(f"URL: {url} -> {resp.status_code}")
    except:
        pass
