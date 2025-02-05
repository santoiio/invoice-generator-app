import smtplib, ssl
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def send_email(subject, receivers, message, attachment_path):
    host = "smtp.gmail.com"
    port = 465
    username = "brandon.proworks@gmail.com"
    password = os.getenv("PASSWORD")
    context = ssl.create_default_context()

    # Ensure the attachment file exists
    if not os.path.exists(attachment_path):
        print(f"Error: The file {attachment_path} was not found!")
        return

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = username
    msg['To'] = ", ".join(receivers) #Join multiple recipients with a comma
    msg['Subject'] = subject

    # Add body text to the email
    msg.attach(MIMEText(message, 'plain'))

    # Attach the PDF file
    with open(attachment_path, "rb") as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(attachment_path)}')
        msg.attach(part)


    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        server.sendmail(username, receivers, msg.as_string())