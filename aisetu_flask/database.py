import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://HK_Digiverse:HK%40Digiverse%40123@cluster0.lcbyqbq.mongodb.net/aisetu_db?retryWrites=true&w=majority&appName=Cluster0")
client = MongoClient(MONGO_URI)
db = client.get_database("aisetu_db")

# Collections
demo_requests = db.demo_requests
user_logins = db.user_logins
pricing_signups = db.pricing_signups
contact_submissions = db.contact_submissions
job_applications = db.job_applications
landing_page_content = db.landing_page_content
referral_users = db.referral_users
