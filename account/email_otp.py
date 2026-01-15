from threading import Thread
import boto3
from botocore.exceptions import ClientError
from config import settings
from .models import User

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
        print(e.response['Error']['Message'])
    except Exception as e:
        print(e)
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])


def send_otp_thread(user: User, otp):
    t = Thread(target=send_otp, args=(user, otp))
    t.start()
