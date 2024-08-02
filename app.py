import json
import jwt
import requests
import subprocess
from flask import Flask, request

app = Flask(__name__)

# Your configurations
JWKS_URL = "https://[kindedomain].kinde.com/.well-known/jwks.json"
SOUND_FILE = "/Users/danielrivers/development/play/webhooksound/new-signup.mp3"

# Function to fetch and process JWKS data
def get_jwks():
    response = requests.get(JWKS_URL)
    return response.json()["keys"]

# Function to validate JWT
def validate_jwt(token, jwks):
    try:
        unverified_header = jwt.get_unverified_header(token)
        kid = unverified_header["kid"]
        for jwk in jwks:
            if jwk["kid"] == kid:
                public_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk))
                return jwt.decode(token, key=public_key, algorithms=["RS256"])
        return None
    except jwt.ExpiredSignatureError:
        return None  # Or handle the error as needed

# Flask route to handle webhooks
@app.route('/webhook', methods=['POST'])
def handle_webhook():
    token = request.get_data(as_text=True)  

    jwks = get_jwks()
    decoded_data = validate_jwt(token, jwks)
    print(decoded_data.get("type"))
    if decoded_data and decoded_data.get("type") == "user.created":
        subprocess.Popen(["mpg123", SOUND_FILE])  
        return "User created, sound played!", 200
    else:
        return "Invalid or irrelevant webhook", 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)  