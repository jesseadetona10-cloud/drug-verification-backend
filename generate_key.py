with open('fix_secret_key.py', 'w') as f:
    f.write('import secrets\n')
    f.write('key = secrets.token_hex(32)\n')
    f.write('print(key)\n')
print('Done')
