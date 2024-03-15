# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# import smtplib
from threading import Thread
import boto3
from botocore.exceptions import ClientError
from sentry_sdk import capture_exception
from config import settings
from .models import User
# import requests
# from django.core.mail import send_mail

def send_otp(user:User,otp):
    SENDER = f"\"Your OTP for Renaissance Verification\" <{settings.Email}>"
    RECIPIENT = user.email
    AWS_REGION = "ap-south-1"
    name= f"{user.first_name} {user.last_name}"
    SUBJECT = f"Your OTP : {otp}"
    BODY_TEXT = (f"Hi {name}, Your one-time password (OTP) for accessing your account is: {otp} This OTP is valid for 10 minutes.Please do not share it with anyone. We hope you have a great time at Renaissance!")
    BODY_HTML = f"""<html>
    <head></head>
    <body>
    <h1></h1>
    <p>Hi {name},<br>
    Your one-time password (OTP) for accessing your account is:<br>
    <b>{otp}</b><br>
    This OTP is valid for 10 minutes.Please do not share it with anyone. <br>
    We hope you have a great time at Renaissance !<br>
    Team JECRC Renaissance
    </p>
    </body>
    </html>
                """
    CHARSET = "UTF-8"
    print(settings.AWS_ACCESS_KEY_ID)
    print(settings.AWS_SECRET_ACCESS_KEY)
    client = boto3.client('ses',
                          region_name=AWS_REGION,
                          aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                          )
    try:
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
        )
    except ClientError as e:
        capture_exception(e)
        print(e.response['Error']['Message'])
    except Exception as e:
        capture_exception(e)
        print(e)
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])


# from azure.communication.email import EmailClient

# def send_otp(user, otp):
#     try:
#         connection_string = settings.ACE_CONNECTION_STRING
#         client = EmailClient.from_connection_string(connection_string)

#         message = {
#             "senderAddress": "DoNotReply@b2e48f1c-4006-459a-bce8-cea2b59d541a.azurecomm.net",
#             "recipients": {
#                 "to": [{"address": f"{user.email}"}],
#             },
#             "content": {
#                 "subject": f"You OTP for Renaissance: {otp}",
#                 "plainText": f"Hi {user.first_name}, Your one-time password (OTP) for accessing your account is: {otp}. This OTP is valid for 10 minutes. Please do not share it with anyone. We hope you have a great time at Renaissance!",
#             },
#         }

#         poller = client.begin_send(message)
#         result = poller.result()

#     except Exception as ex:
#         capture_exception(ex)
#         print(ex)


def send_otp_thread(user: User, otp):
    t = Thread(target=send_otp, args=(user, otp))
    t.start()
