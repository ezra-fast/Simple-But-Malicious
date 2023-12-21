import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import formataddr                      # this is the critical line

# Email configuration
def emailer():
    smtp_server = "smtp-mail.outlook.com"
    smtp_port = 587
    sender_email = "NOTHINGTOSEEHERE"
    sender_name = "Jeff Bezos"  # This is the display name you want to appear

    receiver_email = "NOTHINGTOSEEHERE"
    subject = "Test Subject"
    message = "Test Message"
    replyAddress = "support@apple.com"

    # Create the email message
    msg = MIMEMultipart()
    # msg["From"] = Header(sender_name, "utf-8")  # Setting the display name
    msg["From"] = formataddr((sender_name, sender_email))
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg["Reply-To"] = replyAddress
    msg.attach(MIMEText(message, "plain"))

    # Connect to the SMTP server and send the email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, "NOTHINGTOSEEHERE")
        
        server.sendmail(sender_email, receiver_email, msg.as_string())

emailer()
