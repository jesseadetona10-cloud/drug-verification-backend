from django.core.mail import send_mail
from django.conf import settings

def send_alert_email(to_email, subject, message):
    \"\"\"Send alert email to user.\"\"\"
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[to_email],
        fail_silently=True,
    )

def send_counterfeit_alert(drug_name, batch_number, location):
    \"\"\"Send counterfeit alert to regulators.\"\"\"
    subject = f'COUNTERFEIT ALERT: {drug_name}'
    message = f'''COUNTERFEIT DRUG DETECTED!

Drug: {drug_name}
Batch: {batch_number}
Location: {location}
Time: {datetime.now()}

Immediate action required. Please investigate.'''
    # In production, send to all regulators
    send_alert_email('regulator@drugverify.com', subject, message)

def send_recall_notification(batch_number, drug_name, reason):
    \"\"\"Send recall notification.\"\"\"
    subject = f'BATCH RECALL: {drug_name}'
    message = f'''BATCH RECALL NOTICE

Drug: {drug_name}
Batch: {batch_number}
Reason: {reason}

This batch has been recalled. Please stop distribution immediately and return remaining stock.

Contact your supplier for more information.'''
    # Would loop through all affected parties in production
    send_alert_email('pharmacist@drugverify.com', subject, message)

from datetime import datetime
