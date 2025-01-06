# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client
from dotenv import dotenv_values

env = dotenv_values('.env')

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = env["TWILLIO_ACCOUNT_SID_LIVE"]
auth_token = env["TWILLIO_AUTH_TOKEN_LIVE"]
client = Client(account_sid, auth_token)

call = client.calls.create(
    url="http://demo.twilio.com/docs/voice.xml",
    to="+18585856575",
    from_=f"+1{env['TWILLIO_PHONE_NUMBER_LIVE']}",
)

print(call.sid)