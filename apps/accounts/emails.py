from django.core.mail import send_mail
from django.conf import settings
import threading

def _send_async(subject, message, recipient):
    try:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient, fail_silently=True)
    except Exception:
        pass

def send_welcome_email(user):
    msg = f"Hi {user.company_name or user.email},\n\nWelcome to DrugVerify!\n\nRole: {user.role.capitalize()}\nEmail: {user.email}\n\nStay safe,\nDrugVerify Team"
    t = threading.Thread(target=_send_async, args=("Welcome to DrugVerify!", msg, [user.email]))
    t.daemon = True
    t.start()

def send_counterfeit_alert_email(alert):
    msg = f"ALERT: {alert.title}\n\nSeverity: {alert.severity.upper()}\nMessage: {alert.message}\n\nDrugVerify Team"
    t = threading.Thread(target=_send_async, args=(f"CRITICAL ALERT: {alert.title}", msg, [settings.DEFAULT_FROM_EMAIL]))
    t.daemon = True
    t.start()
