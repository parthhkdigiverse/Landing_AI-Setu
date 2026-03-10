import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_route(method, endpoint, data=None, files=None):
    url = f"{BASE_URL}{endpoint}"
    print(f"Testing {method} {endpoint}...")
    try:
        if method == "POST":
            if files:
                response = requests.post(url, data=data, files=files)
            else:
                response = requests.post(url, json=data)
        else:
            response = requests.get(url)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json() if response.headers.get('Content-Type') == 'application/json' else response.text[:100]}")
    except Exception as e:
        print(f"Error: {e}")
    print("-" * 20)

if __name__ == "__main__":
    # Test book-demo
    test_route("POST", "/book-demo/", {
        "name": "Test User",
        "contact_number": "1234567890",
        "store_type": "Retail",
        "city": "Test City"
    })

    # Test login
    test_route("POST", "/api/login/", {
        "email": "test@example.com",
        "password": "1234"
    })

    # Test landing-content
    test_route("GET", "/api/landing-content/")

    # Test contact-submit
    test_route("POST", "/api/contact/submit/", {
        "name": "Contact User",
        "phone": "9876543210",
        "email": "contact@example.com",
        "officeAddress": "123 Street",
        "message": "Hello!"
    })

    # Test referral-check
    test_route("POST", "/referral-check/", {
        "mobile_number": "9999999999"
    })
