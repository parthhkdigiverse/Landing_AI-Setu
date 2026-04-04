import hashlib, binascii, os
from pymongo import MongoClient
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / 'aisetu_erp' / '.env')

# Generate hash for 'admin'
salt = b'salt1234'
dk = hashlib.pbkdf2_hmac('sha256', b'admin', salt, 390000)
password_hash = f'pbkdf2_sha256$390000${binascii.hexlify(salt).decode()}${binascii.hexlify(dk).decode()}'

# Connect to MongoDB
uri = os.getenv('DB_URL', os.getenv('DB_HOST'))
db_name = os.getenv('DB_NAME', 'aisetu_db_razorpay')
client = MongoClient(uri)
db = client[db_name]
collection = db['auth_user']

# Update password for user 'hp'
result = collection.update_one({'username': 'hp'}, {'$set': {'password': password_hash}})

if result.matched_count > 0:
    print('Password for user hp reset successfully via direct Mongo update')
else:
    print('User hp not found in auth_user collection')
client.close()
