with open('apps/drugs/views.py', 'r') as f:
    content = f.read()

email_import = '''from django.core.mail import send_mail
from django.conf import settings
from apps.accounts.models import User
'''

notify_code = '''
def notify_regulators(drug):
    try:
        regulators = User.objects.filter(role="regulator", is_active=True)
        emails = list(regulators.values_list("email", flat=True))
        if emails:
            send_mail(
                subject=f"New Drug Registration: {drug.name}",
                message=f"A new drug has been submitted for approval.\n\nDrug: {drug.name}\nNAFDAC No: {drug.nafdac_number}\nManufacturer: {drug.manufacturer.company_name}\n\nPlease login to review and approve/reject this drug.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=emails,
                fail_silently=True,
            )
    except Exception as e:
        print(f"Email error: {e}")
'''

content = email_import + content + notify_code

with open('apps/drugs/views.py', 'w') as f:
    f.write(content)
print('Done')
