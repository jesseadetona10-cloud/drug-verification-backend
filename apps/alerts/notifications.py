from django.core.mail import send_mail
from django.conf import settings
from apps.accounts.models import User

def send_counterfeit_alert_email(alert):
    regulators = User.objects.filter(role="regulator", is_active=True)
    emails = list(regulators.values_list("email", flat=True))
    if not emails:
        return
    subject = f"[URGENT] {alert.severity.upper()} Alert: {alert.title}"
    message = f"Alert Type: {alert.alert_type}\nSeverity: {alert.severity}\nMessage: {alert.message}\n"
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, emails, fail_silently=True)

def send_recall_alert_email(alert):
    pharmacists = User.objects.filter(role="pharmacist", is_active=True)
    wholesalers = User.objects.filter(role="wholesaler", is_active=True)
    emails = list(pharmacists.values_list("email", flat=True)) + list(wholesalers.values_list("email", flat=True))
    if not emails:
        return
    subject = f"[RECALL NOTICE] {alert.title}"
    message = f"A drug recall has been issued.\nMessage: {alert.message}\n"
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, emails, fail_silently=True)
