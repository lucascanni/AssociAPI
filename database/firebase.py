import firebase_admin, pyrebase
from firebase_admin import credentials
# from configs.firebase_config import firebaseConfig
from dotenv import dotenv_values
import json

# config = dotenv_values("/etc/secrets/.env")
config = dotenv_values(".env")

# cred = credentials.Certificate('configs/associapi_private_key.json')
cred = firebase_admin.credentials.Certificate(json.loads(config['FIREBASE_SERVICE_ACCOUNT_KEY']))
firebase_admin.initialize_app(cred)

# firebase=pyrebase.initialize_app(firebaseConfig)
firebase = pyrebase.initialize_app(json.loads(config['FIREBASE_CONFIG']))
db=firebase.database()

#authentication
authMember = firebase.auth()
