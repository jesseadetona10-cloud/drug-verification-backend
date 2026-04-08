from django.core.mail import send_mail
from django.conf import settings

def send_welcome_email(user):
    try:
        send_mail(
            subject="Welcome to DrugVerify!",
            message=f"""
Hi {user.company_name or user.email},

Welcome to DrugVerify - Nigeria's Drug Verification Platform!

Your account has been created successfully.
Role: {user.role.capitalize()}
Email: {user.email}

You can now log in at: http://localhost:5173

Stay safe,
DrugVerify Team
            """,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=True,
        )
    except Exception:
        pass

def send_counterfeit_alert_email(alert):
    try:
        send_mail(
            subject=f"CRITICAL ALERT: {alert.title}",
            message=f"""
DRUG VERIFICATION ALERT

Type: {alert.alert_type.upper()}
Severity: {alert.severity.upper()}
Drug: {alert.drug.name if alert.drug else "Unknown"}
Message: {alert.message}

Please take immediate action.

DrugVerify Team
            """,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.DEFAULT_FROM_EMAIL],
            fail_silently=True,
        )
    except Exception:
        pass
