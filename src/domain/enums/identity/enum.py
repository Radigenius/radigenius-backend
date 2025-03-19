from django.db.models import TextChoices


class BanReasons(TextChoices):
    ABUSIVE = "Abusive"
    RACISM = "Racism"
    SPAM = "Spam"
    SUSPICIOUS_ACTIVITY = "Suspicious_Activity"
    HONEYPOT = "Honeypot"
    OTHER = "Other"
