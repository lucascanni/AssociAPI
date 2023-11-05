import firebase_admin, pyrebase
from firebase_admin import credentials
from configs.firebase_config import firebaseConfig

cred = credentials.Certificate('configs/associapi_private_key.json')
firebase_admin.initialize_app(cred)

firebase=pyrebase.initialize_app(firebaseConfig)
db=firebase.database()