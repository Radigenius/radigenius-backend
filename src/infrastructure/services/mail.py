import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging
from typing import Dict

from django.conf import settings

from infrastructure.exceptions.exceptions import SendEmailException

logger = logging.getLogger(__name__)

class MailService:
    def __init__(self):
        self.transporter = None
        self.initialize_transporter()

    def initialize_transporter(self):
        email_config = settings.EMAIL
        if not email_config:
            logger.warning("Email configuration not found")
            return

        try:
            # SMTP server connection is established per email in smtplib, so just storing config
            self.transporter = {
                'host': email_config.get('HOST'),
                'port': email_config.get('PORT'),
                'user': email_config.get('USER'),
                'password': email_config.get('PASSWORD'),
                'from': email_config.get('FROM'),
                'secure': email_config.get('PORT') == 465
            }
            # Test connection
            with smtplib.SMTP_SSL(self.transporter['host'], self.transporter['port']) if self.transporter['secure'] else smtplib.SMTP(self.transporter['host'], self.transporter['port']) as server:
                server.login(self.transporter['user'], self.transporter['password'])
            logger.info("SMTP connection configured successfully")
        except Exception as error:
            logger.error(f"SMTP connection error: {str(error)}")

    def send_email(self, options: Dict[str, str]):
        if not self.transporter:
            raise NotImplementedError("Email configuration not found or transporter not initialized")

        try:
            msg = MIMEMultipart()
            msg['From'] = self.transporter['from']
            msg['To'] = options['to']
            msg['Subject'] = options['subject']

            msg.attach(MIMEText(options['html'], 'html'))

            with smtplib.SMTP_SSL(self.transporter['host'], self.transporter['port']) if self.transporter['secure'] else smtplib.SMTP(self.transporter['host'], self.transporter['port']) as server:
                server.login(self.transporter['user'], self.transporter['password'])
                server.send_message(msg)

            logger.info(f"Email sent to {options['to']}")
        except Exception as error:
            logger.error(f"Failed to send email: {str(error)}")
            raise SendEmailException(f"Failed to send email: {str(error)}")

    def send_otp_email(self, to: str, otp: int):
        subject = "Your One-Time Password (OTP)"
        html = f"""
        <h1>Your Verification Code</h1>
        <p>Thank you for registering! Please use the code below to verify your account:</p>
        <div style="margin: 20px 0; padding: 15px; background-color: #f5f5f5; border-radius: 4px; text-align: center;">
            <span style="font-size: 24px; font-weight: bold; letter-spacing: 5px;">{otp}</span>
        </div>
        <p>This OTP will expire in 4 minutes.</p>
        <p>If you didn't request this code, please ignore this email.</p>
        """
        self.send_email({'to': to, 'subject': subject, 'html': html})