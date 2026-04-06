import re
with open("config/settings.py", "r") as f:
    content = f.read()
content = content.replace(
    "SECRET_KEY = 'django-insecure-dev-key-only'",
    "SECRET_KEY = 'django-insecure-dev-key-only-for-development-use-only-change-in-prod'"
)
with open("config/settings.py", "w") as f:
    f.write(content)
print("Done")
