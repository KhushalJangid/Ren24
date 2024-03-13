from email.message import EmailMessage
import boto3
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from threading import Thread
# from account.models import User
from config import settings

# def send_email_with_attachment(user,pdf_buffer):
#     # Initialize SES client
#     ses_client = boto3.client('ses', 
#                               region_name='ap-south-1', 
#                               aws_access_key_id=settings.AWS_ACCESS_KEY_ID, 
#                               aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
#                               )  # Replace with your desired region and credentials
    
#     name=f"{user.first_name} {user.last_name}"
#     # Create a multipart message
#     message = MIMEMultipart()
#     message['Subject'] = f'Renaissance Master Pass'
#     message['From'] = f"\"Your Pass for Renaissance 2024 !\" <{settings.Email}>"
#     message['To'] = user.email

#     # Add HTML content (optional)
#     html_content = MIMEText(f'''<p>Hi {name}, <br>
#                             Thank you for registering for Renaissance 2024,<br>
#                             Your Master Pass is attached to this email.<br>
#                             Please present this ticket at the event entrance for scanning.<br><br>
#                             <b>Note:</b>
#                             <ul>
#                                 <li>This pass will grant you entry to the JECRC campus for 3 days (19 to 21 March)</li>
#                                 <li>This pass can be scanned only once per day, no re-entry will be permitted</li>
#                                 <li>This pass is non-transferable and non-refundable </li>
#                             </ul>
#                             We look forward to seeing you at Ren 2024 ! <br><br>
#                             Best regards,<br>
#                             Team JECRC Renaissance
#                             </p>''', 'html')
#     message.attach(html_content)

#     # Attach the image
#     attachment = MIMEApplication(pdf_buffer.getvalue())
#     attachment.add_header('Content-Disposition', 'attachment', filename='Ticket.pdf')
#     message.attach(attachment)

#     # Send the email
#     try:
#         response = ses_client.send_raw_email(
#             Source=message['From'],
#             Destinations=[message['To']],
#             RawMessage={'Data': message.as_string()}
#         )
#         print(f"Email sent! Message ID: {response['MessageId']}")
#     except Exception as e:
#         print(f"Error sending email: {str(e)}")

# def send_email_thread(user,pdf_buffer):
#     t = Thread(target=send_email_with_attachment, args=(user, pdf_buffer))
#     t.start()

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

# def send_email_with_attachment(user, pdf_buffer):
#     # Define your SMTP server settings
#     smtp_server = "smtp-relay.brevo.com"
#     smtp_port = 587
#     smtp_username = "ticket.renaissance@gmail.com"
#     smtp_password = "yfKJ7YwzOLRs6D9t"

#     # Create a multipart message
#     message = MIMEMultipart()
#     message["Subject"] = "Renaissance Master Pass"
#     message["From"] = f"\"Your Pass for Renaissance 2024!\" <noreply@renaissance.com>"
#     message["To"] = user.email

#     # Add HTML content (optional)
#     name = f"{user.first_name} {user.last_name}"
#     html_content = MIMEText(f"""<p>Hi {name},<br>
#                             Thank you for registering for Renaissance 2024!<br>
#                             Your Master Pass is attached to this email.<br>
#                             Please present this ticket at the event entrance for scanning.<br><br>
#                             <b>Note:</b>
#                             <ul>
#                                 <li>This pass will grant you entry to the JECRC campus for 3 days (19 to 21 March).</li>
#                                 <li>This pass can be scanned only once per day; no re-entry will be permitted.</li>
#                                 <li>This pass is non-transferable and non-refundable.</li>
#                             </ul>
#                             We look forward to seeing you at Ren 2024!<br><br>
#                             Best regards,<br>
#                             Team JECRC Renaissance
#                             </p>""", "html")
#     message.attach(html_content)

#     # Attach the PDF
#     attachment = MIMEApplication(pdf_buffer.getvalue())
#     attachment.add_header("Content-Disposition", "attachment", filename="Ticket.pdf")
#     message.attach(attachment)

#     try:
#         # Connect to the SMTP server and send the email
#         with smtplib.SMTP(smtp_server, smtp_port) as server:
#             server.starttls()
#             server.login(smtp_username, smtp_password)
#             server.sendmail(message["From"], message["To"], message.as_string())
#         print(f"Email with attachment sent successfully to {user.email}")
#     except smtplib.SMTPException as e:
#         print(f"Error sending email with attachment: {e}")


# def send_email_thread(user,pdf_buffer):
#     t = Thread(target=send_email_with_attachment, args=(user, pdf_buffer))
#     t.start()

# from django.core.mail import EmailMessage

# def send_email_with_attachment(user, pdf_buffer):
#   """
#   Sends an email with a PDF attachment to the user.
#   """
#   subject = "Renaissance Master Pass"
#   from_email = f'"Your Pass for Renaissance 2024!" <noreply@renaissance.com>'
#   recipient_list = [user.email]

#   # Build the email content
#   name = f"{user.first_name} {user.last_name}"
#   html_content = f"""<p>Hi {name},<br>
#                       Thank you for registering for Renaissance 2024!<br>
#                       Your Master Pass is attached to this email.<br>
#                       Please present this ticket at the event entrance for scanning.<br><br>
#                       <b>Note:</b>
#                       <ul>
#                         <li>This pass will grant you entry to the JECRC campus for 3 days (19 to 21 March).</li>
#                         <li>This pass can be scanned only once per day; no re-entry will be permitted.</li>
#                         <li>This pass is non-transferable and non-refundable.</li>
#                       </ul>
#                       We look forward to seeing you at Ren 2024!<br><br>
#                       Best regards,<br>
#                       Team JECRC Renaissance
#                     </p>"""

#   # Create the email message
#   message = EmailMessage(subject, html_content, from_email, recipient_list)
#   message.content_subtype = 'html'  # Set HTML content type

#   # Attach the PDF
#   attachment = pdf_buffer.getvalue()
#   message.attach(filename="Ticket.pdf", content=attachment, mimetype="application/pdf")

#   # Send the email
#   try:
#     message.send()
#     print(f"Email with attachment sent successfully to {user.email}")
#   except Exception as e:
#     print(f"Error sending email with attachment: {e}")

# def send_email_thread(user, pdf_buffer):
#   """
#   Sends the email with attachment in a separate thread.
#   """
#   t = Thread(target=send_email_with_attachment, args=(user, pdf_buffer))
#   t.start()

import base64
from azure.communication.chat import ChatClient
from azure.identity import DefaultAzureCredential
from azure.core.exceptions import ResourceNotFoundError
from email.message import EmailMessage
from io import BytesIO
from azure.communication.email import EmailClient

from azure.communication.email import EmailClient

from azure.communication.email import EmailClient

def send_email_with_attachment(user, pdf_buffer):
    """
    Sends an email with a PDF attachment to the user.
    """
    # Initialize Azure Communication Services
    connection_string = ""
    client = EmailClient.from_connection_string(connection_string)

    # Build the email content
    name = f"{user.first_name} {user.last_name}"
    # Send the message with attachment
    message = {
            "senderAddress": "",
            "recipients":  {
                "to": [{"address": f"{user.email}" }],
            },
            "content": {
                "subject": "Your Renaissance 2024 Master Pass",
                "html": f"""<html>
                      <body>
                      <p>Hi {name},<br>
                      Thank you for registering for Renaissance 2024!<br>
                      Your Master Pass is attached to this email.<br>
                      Please present this ticket at the event entrance for scanning.<br><br>
                      <b>Note:</b>
                      <ul>
                        <li>This pass will grant you entry to the JECRC campus for 3 days (19 to 21 March).</li>
                        <li>This pass can be scanned only once per day; no re-entry will be permitted.</li>
                        <li>This pass is non-transferable and non-refundable.</li>
                      </ul>
                      We look forward to seeing you at Ren 2024!<br><br>
                      Best regards,<br>
                      Team JECRC Renaissance
                      </p>
                      </body>
                      </html>"""
            },
            "attachments":[
              {"name":"Ticket.pdf",
              "attachmentType": "application/pdf",
              "contentType":"application/pdf",
              "contentInBase64":base64.b64encode(pdf_buffer.getvalue()).decode("utf-8"),}
              
            ]
        }
        
    
    client.begin_send(message)

    print(f"Email with attachment sent successfully to {user.email}")



def send_email_thread(user, pdf_buffer):
  """
  Sends the email with attachment in a separate thread.
  """
  t = Thread(target=send_email_with_attachment, args=(user, pdf_buffer))
  t.start()
