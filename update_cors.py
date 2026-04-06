with open('config/settings.py', 'r') as f:
    content = f.read()

content = content.replace(
    "'rest_framework',",
    "'rest_framework',\n    'corsheaders',"
)
content = content.replace(
    "'django.middleware.security.SecurityMiddleware',",
    "'django.middleware.security.SecurityMiddleware',\n    'corsheaders.middleware.CorsMiddleware',"
)
if 'CORS_ALLOWED_ORIGINS' not in content:
    content += "\nCORS_ALLOWED_ORIGINS = [\n    'http://localhost:5173',\n]\n"

with open('config/settings.py', 'w') as f:
    f.write(content)
print('Done')
