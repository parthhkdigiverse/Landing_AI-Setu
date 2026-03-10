from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import random
import string
import uuid
import datetime
import os
from database import demo_requests, user_logins, pricing_signups, contact_submissions, job_applications, landing_page_content, referral_users

app = Flask(__name__, static_folder=None) # Disable default static folder
CORS(app)

# React build directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REACT_BUILD_DIR = os.path.join(BASE_DIR, "Frontend", "landing-page-launchpad-main", "dist")

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react(path):
    # Strip 'static/' prefix if present (React build might include it)
    normalized_path = path
    if path.startswith('static/'):
        normalized_path = path[7:]

    if normalized_path != "" and os.path.exists(os.path.join(REACT_BUILD_DIR, normalized_path)):
        return send_from_directory(REACT_BUILD_DIR, normalized_path)
    else:
        return send_from_directory(REACT_BUILD_DIR, 'index.html')

FIXED_PASSWORD = "1234"

def generate_referral_code():
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choices(characters, k=6))

@app.route('/book-demo/', methods=['POST'])
def book_demo_api():
    try:
        data = request.get_json()
        name = data.get("name")
        contact_number = data.get("contact_number")
        store_type = data.get("store_type")
        city = data.get("city")

        if not all([name, contact_number, store_type, city]):
            return jsonify({"error": "All fields required"}), 400

        demo_requests.insert_one({
            "name": name,
            "contact_number": contact_number,
            "store_type": store_type,
            "city": city,
            "created_at": datetime.datetime.now(datetime.UTC)
        })

        return jsonify({"message": "Demo request saved successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/login/', methods=['POST'])
def login_view():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({"error": "All fields are required"}), 400

        if password == FIXED_PASSWORD:
            user_logins.insert_one({
                "email": email,
                "password": password,
                "login_time": datetime.datetime.now(datetime.UTC)
            })
            return jsonify({"message": "Login successful!"}), 200
        else:
            return jsonify({"error": "Incorrect password. Please contact admin."}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/pricing-signup/', methods=['POST'])
def pricing_signup():
    try:
        data = request.get_json()
        shop_name = data.get('shop_name')
        owner_name = data.get('owner_name')
        mobile_number = data.get('mobile_number')
        referral_code_entered = data.get('referral_code')

        generated_code = generate_referral_code()

        if referral_code_entered:
            pricing_signups.update_one(
                {"referral_code": referral_code_entered},
                {"$inc": {"total_referrals": 1}}
            )

        pricing_signups.insert_one({
            "shop_name": shop_name,
            "owner_name": owner_name,
            "mobile_number": mobile_number,
            "referral_code": generated_code,
            "total_referrals": 0,
            "created_at": datetime.datetime.now(datetime.UTC)
        })

        return jsonify({
            "message": "Signup successful",
            "referral_code": generated_code
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/landing-content/', methods=['GET'])
def landing_page_content_api():
    try:
        content = landing_page_content.find_one()
        if not content:
            # Create default content if not exists
            default_content = {
                "hero_eyebrow": "India's Smartest Retail ERP",
                "hero_title": "Smart ERP for",
                "hero_highlighted_title": "Indian Retailers",
                "hero_subtitle": "AI-powered billing, inventory & store management — built specifically for Indian retail businesses. Save time, reduce errors, grow faster.",
                "hero_highlights": "GST-Ready Billing,Real-time Inventory,AI-Powered Insights",
                "primary_cta_text": "Book Free Demo",
                "secondary_cta_text": "Watch Demo",
                "trusted_retailers_count": "500+",
                "hero_stats_label": "Today's Sales",
                "hero_stats_value": "₹1,24,500"
            }
            landing_page_content.insert_one(default_content)
            content = default_content

        content['_id'] = str(content['_id'])
        return jsonify(content), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/contact/submit/', methods=['POST'])
def submit_contact():
    try:
        data = request.get_json()
        contact = {
            "name": data.get("name"),
            "phone": data.get("phone"),
            "email": data.get("email"),
            "officeAddress": data.get("officeAddress"),
            "message": data.get("message"),
            "created_at": datetime.datetime.now(datetime.UTC)
        }
        result = contact_submissions.insert_one(contact)
        return jsonify({
            "id": str(result.inserted_id),
            "message": "Form submitted successfully!"
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/apply-job/', methods=['POST'])
def apply_job():
    try:
        # Note: Django model had FileField for resume.
        # For simplicity in this initial port, we expect a filename or handle it via multipart
        data = request.form.to_dict()
        resume_file = request.files.get('resume')
        
        # Save resume file logic if needed
        resume_path = ""
        if resume_file:
            resume_path = os.path.join("uploads/resumes", resume_file.filename)
            resume_file.save(resume_path)

        job_application = {
            "job_position": data.get("job_position"),
            "first_name": data.get("first_name"),
            "last_name": data.get("last_name"),
            "email": data.get("email"),
            "phone": data.get("phone"),
            "experience": int(data.get("experience", 0)) if data.get("experience") else None,
            "available_to_join": int(data.get("available_to_join", 0)) if data.get("available_to_join") else None,
            "current_salary": data.get("current_salary"),
            "expected_salary": data.get("expected_salary"),
            "location": data.get("location"),
            "resume": resume_path,
            "applied_at": datetime.datetime.now(datetime.UTC)
        }
        job_applications.insert_one(job_application)
        return jsonify({"message": "Application submitted successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/referral-check/', methods=['POST'])
def check_referral():
    try:
        data = request.get_json()
        mobile = data.get("mobile_number")
        if not mobile:
            return jsonify({"error": "Mobile number required"}), 400

        # Check pricing_signups
        user = pricing_signups.find_one({"mobile_number": mobile})
        if user and user.get("referral_code"):
            return jsonify({
                "referral_code": user["referral_code"],
                "status": "existing_pricing_user"
            }), 200

        # Check referral_users
        referral_user = referral_users.find_one({"mobile_number": mobile})
        created = False
        if not referral_user:
            referral_user = {
                "mobile_number": mobile,
                "referral_code": generate_referral_code(),
                "created_at": datetime.datetime.utcnow()
            }
            referral_users.insert_one(referral_user)
            created = True

        return jsonify({
            "referral_code": referral_user["referral_code"],
            "status": "new_user" if created else "existing_referral_user"
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=8000)
