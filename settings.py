import os
from dotenv import load_dotenv
load_dotenv()

db_uri = os.getenv('TEST_DATABASE_URI')
print("################ ", db_uri)