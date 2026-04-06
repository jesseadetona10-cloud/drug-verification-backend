with open('config/settings.py', 'r') as f:
    content = f.read()
content = content.replace("SECRET_KEY = 'django-insecure-dev-key-only'", "SECRET_KEY = 'django-insecure-REPLACE_WITH_YOUR_GENERATED_KEY'")
with open('config/settings.py', 'w') as f:
    f.write(content)
print('Done')
