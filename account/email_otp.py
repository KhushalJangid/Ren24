from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from threading import Thread
import boto3
from botocore.exceptions import ClientError
from config import settings
from .models import User
import requests
from django.core.mail import send_mail

# def send_otp(user:User,otp):
#     SENDER = f"\"Your OTP for Renaissance Verification\" <{settings.Email}>"
#     RECIPIENT = user.email
#     AWS_REGION = "ap-south-1"
#     name= f"{user.first_name} {user.last_name}"
#     SUBJECT = f"Your OTP : {otp}"
#     BODY_TEXT = (f"Hi {name}, Your one-time password (OTP) for accessing your account is: {otp} This OTP is valid for 10 minutes.Please do not share it with anyone. We hope you have a great time at Renaissance!")
#     BODY_HTML = f"""<html>
#     <head></head>
#     <body>
#     <h1></h1>
#     <p>Hi {name},<br> 
#     Your one-time password (OTP) for accessing your account is:<br>
#     <b>{otp}</b><br> 
#     This OTP is valid for 10 minutes.Please do not share it with anyone. <br>
#     We hope you have a great time at Renaissance !<br>
#     Team JECRC Renaissance
#     </p>
#     </body>
#     </html>
#                 """            
#     CHARSET = "UTF-8"
#     print(settings.AWS_ACCESS_KEY_ID)
#     print(settings.AWS_SECRET_ACCESS_KEY)
#     client = boto3.client('ses',
#                           region_name=AWS_REGION,
#                           aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
#                           aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
#                           )
#     try:
#         response = client.send_email(
#             Destination={
#                 'ToAddresses': [
#                     RECIPIENT,
#                 ],
#             },
#             Message={
#                 'Body': {
#                     'Html': {
#                         'Charset': CHARSET,
#                         'Data': BODY_HTML,
#                     },
#                     'Text': {
#                         'Charset': CHARSET,
#                         'Data': BODY_TEXT,
#                     },
#                 },
#                 'Subject': {
#                     'Charset': CHARSET,
#                     'Data': SUBJECT,
#                 },
#             },
#             Source=SENDER,
#         )	
#     except ClientError as e:
#         print(e.response['Error']['Message'])
#     except Exception as e:
#         print(e)
#     else:
#         print("Email sent! Message ID:"),
#         print(response['MessageId'])
        
# def send_otp_thread(user:User, otp):
#     t = Thread(target=send_otp, args=(user, otp))
#     t.start()

# def send_otp_thread(user:User, otp):
#     # Define your Brevo API endpoint
#     brevo_api_url = "https://api.brevo.com/v3/send_email"

#     # Define your Brevo API credentials (replace with actual values)
#     brevo_api_key = "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"
#     # brevo_api_secret = "your_api_secret"

#     # Define the email parameters
#     sender = f"\"Your OTP for Renaissance Verification\" <noreply@renaissance.com>"
#     recipient = "email"
#     name = f"{'first_name'} {'last_name'}"
#     subject = f"Your OTP: {otp}"
#     body_text = (f"Hi {name}, Your one-time password (OTP) for accessing your account is: {otp}. "
#                  f"This OTP is valid for 10 minutes. Please do not share it with anyone. "
#                  f"We hope you have a great time at Renaissance!")
#     body_html = f"""<html>
#     <head></head>
#     <body>
#     <h1></h1>
#     <p>Hi {name},<br> 
#     Your one-time password (OTP) for accessing your account is:<br>
#     <b>{otp}</b><br> 
#     This OTP is valid for 10 minutes. Please do not share it with anyone. <br>
#     We hope you have a great time at Renaissance!<br>
#     Team JECRC Renaissance
#     </p>
#     </body>
#     </html>
#     """

#     # Prepare the payload
#     payload = {
#         "api_key": brevo_api_key,
#         # "api_secret": brevo_api_secret,
#         "sender": sender,
#         "recipient": recipient,
#         "subject": subject,
#         "body_text": body_text,
#         "body_html": body_html
#     }

#     try:
#         # Send the email using Brevo API
#         response = requests.post(brevo_api_url, json=payload)
#         if response.status_code == 200:
#             print(f"OTP email sent successfully to {recipient}")
#         else:
#             print(f"Failed to send OTP email. Status code: {response.status_code}")
#     except requests.RequestException as e:
#         print(f"Error sending OTP email: {e}")

# def send_otp(user:User, otp):
#     # Define your SMTP server settings
#     smtp_server = "smtp-relay.brevo.com"
#     smtp_port = 587
#     smtp_username = "ticket.renaissance@gmail.com"
#     smtp_password = "yfKJ7YwzOLRs6D9t"

#     # Define email parameters
#     sender = "OTP for Renaissance <ticket.renaissance@gmail.com"
#     recipient = user.email
#     name = f"{user.first_name} {user.last_name}"  # Replace with the user's name
#     subject = f"Your OTP: {otp}"
#     body_text = (f"Hi {name}, Your one-time password (OTP) for accessing your account is: {otp}. "
#                  f"This OTP is valid for 10 minutes. Please do not share it with anyone. "
#                  f"We hope you have a great time at Renaissance!")
#     body_html = f"""<html>
#     <head>Yor OTP for Renaissance Login</head>
#     <body>
#     <h1></h1>
#     <p>Hi {name},<br> 
#     Your one-time password (OTP) for accessing your account is:<br>
#     <b>{otp}</b><br> 
#     This OTP is valid for 10 minutes. Please do not share it with anyone. <br>
#     We hope you have a great time at Renaissance!<br>
#     Team JECRC Renaissance
#     </p>
#     </body>
#     </html>
#     """

#     # Create the email message
#     msg = MIMEMultipart("alternative")
#     msg["From"] = sender
#     msg["To"] = recipient
#     msg["Subject"] = subject
#     msg.attach(MIMEText(body_text, "plain"))
#     msg.attach(MIMEText(body_html, "html"))

#     try:
#         # Connect to the SMTP server and send the email
#         with smtplib.SMTP(smtp_server, smtp_port) as server:
#             server.starttls()
#             server.login(smtp_username, smtp_password)
#             server.sendmail(sender, recipient, msg.as_string())  # Encode the message
#         print(f"OTP email sent successfully to {recipient}")
#     except smtplib.SMTPException as e:
#         print(f"Error sending OTP email: {e}")
        
# def send_otp_thread(user:User, otp):
#     t = Thread(target=send_otp, args=(user, otp))
#     t.start()

def send_email_otp(recipient,OTP):
    name= f"{recipient.first_name} {recipient.last_name}"
    otp=OTP
    subject="OTP for your Registration"
    message=f"Hi {name}, \n Your one-time password (OTP) for accessing your account is: {otp}. \n This OTP is valid for 10 minutes. Please do not share it with anyone. \n \n We hope you have a great time at Renaissance!"
    from_email=settings.EMAIL_HOST_USER
    recipient_list=[recipient]
    send_mail(subject,message,from_email,recipient_list,fail_silently=True)
    
def send_otp_thread(user:User, otp):
    t = Thread(target=send_email_otp, args=(user, otp))
    t.start()