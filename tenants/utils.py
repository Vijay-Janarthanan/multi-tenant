from __future__ import print_function
import time, random, string
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from pprint import pprint

configuration = sib_api_v3_sdk.Configuration()
configuration.api_key['api-key'] = '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'

def sendEmail(to, html):
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
    subject = "You are Invited!!!"
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

def createTempassword():
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(10))