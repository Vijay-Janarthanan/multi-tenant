from __future__ import print_function
import random, string, jwt, sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from pprint import pprint
from django.conf import settings

configuration = sib_api_v3_sdk.Configuration()
configuration.api_key['api-key'] = settings.MAIL_API_KEY

# Send Email via Brevo API
def sendEmail(to, html, subject):
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
    subject = subject
    html_content = html
    sender = {"name":"Vijay","email":"mageshjack6@gmail.com"}
    to = [{"email":to,"name":to.split("@")[0]}]
    headers = {"Some-Custom-Name":"unique-id-1234"}
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, headers=headers, html_content=html_content, sender=sender, subject=subject)

    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)

# Creating Temporary Password for Invited Members
def createTempassword():
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(10))

# Encrypt the Payload with JWT which gives Refresh Token with 1 Month expiry
def encodeJWTRefreshToken(payload, exp):
    payload['exp'] = exp+2629743
    encoded_jwt = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    print("encodeJWTRefreshToken",encoded_jwt)
    return encoded_jwt

# Encrypt the Payload with JWT which gives Access Token with 1 Day expiry
def encodeJWTaccessToken(payload, exp):
    payload['exp'] = exp+86400
    encoded_jwt = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    print("encodeJWTaccessToken",encoded_jwt)
    return encoded_jwt

# Decrypt JWT Token
def decodeJWT(token):
    return jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

