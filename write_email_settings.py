with open('config/settings.py', 'r') as f:
    content = f.read()
content += '''
# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
DEFAULT_FROM_EMAIL = 'noreply@drugverification.com'
'''
with open('config/settings.py', 'w') as f:
    f.write(content)
print('Done')
