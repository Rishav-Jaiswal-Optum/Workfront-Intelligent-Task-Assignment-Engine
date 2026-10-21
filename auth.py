import time
import jwt
import requests
import urllib3

from config import *

urllib3.disable_warnings()

def get_access_token():

    try:
        with open("private.key", "r") as file:
            private_key = file.read()

        jwt_token = jwt.encode(
            {
                "iss": CUSTOMER_ID,
                "sub": USER_ID,
                "exp": int(time.time()) + 300
            },
            private_key,
            algorithm="RS256",
            headers={
                "kid": PUBLIC_KEY_ID
            }
        )

        response = requests.post(
            f"{WORKFRONT_URL}/integrations/oauth2/api/v1/jwt/exchange",
            headers={
                "Content-Type": "application/x-www-form-urlencoded"
            },
            data={
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "jwt_token": jwt_token
            },
            verify=False
        )

        response.raise_for_status()

        token_data = response.json()

        return token_data["access_token"]
    
    except Exception as e:
        print(f"error: {str(e)}")