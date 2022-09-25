# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client

# Find your Account SID and Auth Token in Account Info
# and set the environment variables. See http://twil.io/secure

auth_token = '6248c64f482825d90cc19eff058f2e58'        #When publishing, remove these.
account_sid  = 'ACe2df4ce7d5dd6c91c98ac5f4db2b4399'   #When publishing, remove these.
client = Client(account_sid, auth_token)

def full_Send(message_content, phone_num):
  message = client.messages.create(
    body='\n' + message_content,
    from_='+12053045893',
    to='+1' + phone_num
  )


                    