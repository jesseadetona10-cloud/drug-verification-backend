with open('config/settings.py', 'a') as f:
    f.write('\nfrom datetime import timedelta\n')
    f.write('SIMPLE_JWT = {\n')
    f.write('    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),\n')
    f.write('    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),\n')
    f.write('}\n')
print('Done')
