import os
from dotenv import load_dotenv

# load .env
load_dotenv(dotenv_path="config/.env", verbose=True)

host = os.environ.get('host')
port = os.environ.get('port')
user = os.environ.get('user')
password = os.environ.get('password')
db = os.environ.get('db')
dbtype = os.environ.get('dbtype')

SQLALCHEMY_DATABASE_URL = f"{dbtype}://{user}:{password}@{host}:{port}/{db}"