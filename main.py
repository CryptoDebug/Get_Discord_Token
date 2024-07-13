import requests

email = input("Enter your mail : ")
password = input("Enter your password : ")

login_url = 'https://discord.com/api/v9/auth/login'
mfa_url = 'https://discord.com/api/v9/auth/mfa/totp'

payload = {
    'login': email,
    'password': password
}

response = requests.post(login_url, json=payload)
if response.status_code == 200:
    if 'mfa' in response.json():
        mfa_token = response.json()['ticket']
        two_factor_code = input("Enter your 2FA code : ")
        
        mfa_payload = {
            'code': two_factor_code,
            'ticket': mfa_token
        }
        
        mfa_response = requests.post(mfa_url, json=mfa_payload)
        if mfa_response.status_code == 200:
            token = mfa_response.json()['token']
            print(f'Your discord token is : {token}')
        else:
            print('2FA code verification failed.')
    else:
        token = response.json()['token']
        print(f'Your discord token is : {token}')
else:
    print('Initial authentication failed.')
