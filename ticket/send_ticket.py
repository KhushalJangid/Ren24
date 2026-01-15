# from email.message import EmailMessage
import boto3
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from threading import Thread

from config import settings

def send_email_with_attachment(user,pdf_buffer):
    # Initialize SES client
    ses_client = boto3.client('ses',
                              region_name='ap-south-1',
                              aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                              aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
                              )  # Replace with your desired region and credentials

    name=f"{user.first_name} {user.last_name}"
    # Create a multipart message
    message = MIMEMultipart()
    message['Subject'] = f'Renaissance Master Pass'
    message['From'] = f"\"Your Pass for Renaissance 2024 !\" <{settings.Email}>"
    message['To'] = user.email

    # Add HTML content (optional)
    html_content = MIMEText(f'''<p>Hi {name}, <br>
                            Thank you for registering for Renaissance 2024,<br>
                            Your Master Pass is attached to this email.<br>
                            Please present this ticket at the event entrance for scanning.<br><br>
                            <b>Note:</b>
                            <ul>
                                <li>This pass will grant you entry to the JECRC campus for 3 days (19 to 21 March)</li>
                                <li>This pass can be scanned only once per day, no re-entry will be permitted</li>
                                <li>This pass is non-transferable and non-refundable </li>
                            </ul>
                            We look forward to seeing you at Ren 2024 ! <br><br>
                            Best regards,<br>
                            Team JECRC Renaissance
                            </p>''', 'html')
    message.attach(html_content)

    # Attach the image
    attachment = MIMEApplication(pdf_buffer.getvalue())
    attachment.add_header('Content-Disposition', 'attachment', filename='Ticket.pdf')
    message.attach(attachment)

    # Send the email
    try:
        response = ses_client.send_raw_email(
            Source=message['From'],
            Destinations=[message['To']],
            RawMessage={'Data': message.as_string()}
        )
        print(f"Email sent! Message ID: {response['MessageId']}")
    except Exception as e:
        print(f"Error sending email: {str(e)}")

def send_email_thread(user, pdf_buffer):
    """
    Sends the email with attachment in a separate thread.
    """
    t = Thread(target=send_email_with_attachment, args=(user, pdf_buffer))
    t.start()
