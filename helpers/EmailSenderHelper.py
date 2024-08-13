import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailSender:
    EMAIL_CONFIGS = {
        "gmail.com": {"smtp_server": "smtp.gmail.com", "smtp_port": 587},
        "outlook.com": {"smtp_server": "smtp-mail.outlook.com", "smtp_port": 587},
        "yahoo.com": {"smtp_server": "smtp.mail.yahoo.com", "smtp_port": 587},
        # Add more email providers as needed
    }

    def __init__(self, sender_email, sender_password):
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.sender_config = self._get_email_config(sender_email)

    def _get_email_config(self, email):
        domain = email.split("@")[1]
        return self.EMAIL_CONFIGS.get(domain, {"smtp_server": "smtp.default.com", "smtp_port": 587})

    def send_email(self, recipient_email, subject, body):
        # Determine recipient's email configuration
        recipient_config = self._get_email_config(recipient_email)

        # Create the email message
        message = MIMEMultipart()
        message['From'] = self.sender_email
        message['To'] = recipient_email
        message['Subject'] = subject

        # Add body to email
        message.attach(MIMEText(body, 'plain'))

        try:
            # Create SMTP session using sender's configuration
            with smtplib.SMTP(self.sender_config["smtp_server"], self.sender_config["smtp_port"]) as server:
                server.starttls()  # Enable TLS
                server.login(self.sender_email, self.sender_password)
                
                # Send email
                server.send_message(message)
            
            print(f"Email sent successfully to {recipient_email}!")
            print(f"Sender SMTP: {self.sender_config['smtp_server']}")
            print(f"Recipient's email provider: {recipient_config['smtp_server']}")
        except Exception as e:
            print(f"An error occurred: {e}")

# Example usage
if __name__ == "__main__":
    # Create an EmailSender instance
    email_sender = EmailSender("your.email@gmail.com", "your_app_password_for_gmail")

    # Send emails to different providers
    email_sender.send_email("recipient@gmail.com", "Test Email to Gmail", "This is a test email sent to a Gmail account.")
    email_sender.send_email("recipient@outlook.com", "Test Email to Outlook", "This is a test email sent to an Outlook account.")
    email_sender.send_email("recipient@yahoo.com", "Test Email to Yahoo", "This is a test email sent to a Yahoo account.")
    email_sender.send_email("recipient@example.com", "Test Email to Unknown Provider", "This is a test email sent to an unknown provider.")