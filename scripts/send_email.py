import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv # type: ignore

load_dotenv()  # Load credentials securely from .env

# Get email credentials from environment variables
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")  # Use an App Password (NOT real password)
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))  # Default SMTP port for TLS

def send_email_notification(data):
    """
    Send an email notification when meeting data is saved.
    """
    subject = "🚀 New Meeting Insights Ready!"
    body = f"""
    Hello Team,

    Your AI-Powered Meeting Assistant has just processed a new meeting transcript. Here are the key insights:

    🔹 **Name:** {data.get('name', 'N/A')}
    🔹 **Start Time:** {data.get('start_time', 'N/A')}
    🔹 **End Time:** {data.get('end_time', 'N/A')}
    🔹 **Total Hours:** {data.get('total_hours', 'N/A')}
    🔹 **Meeting Date:** {data.get('meeting_date', 'N/A')}
    🔹 **Notes:** {data.get('note', 'N/A')}

    ---
    **Full Transcript:**
    {data.get('transcript', 'N/A')}

    
    Best regards,
    Your AI-Powered Meeting Assistant
    """

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER

    try:
        # Establish SMTP connection
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.ehlo()  # Identify with the server
        server.starttls()  # Secure the connection
        server.ehlo()  # Re-identify after securing the connection
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)  # Authenticate

        # Send the email
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())

        # Close the connection
        server.quit()

        print(" Email notification sent successfully!")
    except Exception as e:
        print(f" Email sending failed: {e}")
