with open('config/settings.py', 'a') as f:
    f.write('\n# Email Configuration\n')
    f.write('EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"\n')
    f.write('DEFAULT_FROM_EMAIL = "noreply@drugverify.com"\n')
print('Done')
