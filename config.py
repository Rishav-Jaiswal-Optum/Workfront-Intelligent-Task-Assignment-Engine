from dotenv import load_dotenv
import os

load_dotenv()

WORKFRONT_URL = os.getenv("WORKFRONT_URL")

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

CUSTOMER_ID = os.getenv("CUSTOMER_ID")
USER_ID = os.getenv("USER_ID")
PUBLIC_KEY_ID = os.getenv("PUBLIC_KEY_ID")
WORKING_DAYS = 10
HOURS_PER_DAY = 8
MAX_CAPACITY = WORKING_DAYS * HOURS_PER_DAY