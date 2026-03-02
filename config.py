import os
from dotenv import load_dotenv

load_dotenv()

EBAY_CLIENT_ID = os.getenv("EBAY_CLIENT_ID")
EBAY_CLIENT_SECRET = os.getenv("EBAY_CLIENT_SECRET")
EBAY_IDENTITY_URL = "https://api.sandbox.ebay.com/identity/v1/oauth2/token"
EBAY_BASE_URL = "https://api.sandbox.ebay.com"
YOUR_TOKEN_HERE = os.getenv("YOUR_TOKEN_HERE")