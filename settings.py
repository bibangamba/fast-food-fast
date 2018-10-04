import os
from dotenv import load_dotenv, find_dotenv
load_dotenv()

db_uri = os.getenv('DATABASE_URI')
print("################ ", db_uri)