import requests
import base64
import json

email = input("Enter your mail: ")
password = input("Enter your password: ")

login_url = 'https://discord.com/api/v10/auth/login'
mfa_url = 'https://discord.com/api/v10/auth/mfa/totp'  # Utilisez /codes-verification pour un code de secours
experiments_url = 'https://discord.com/api/v10/experiments'

# Générer X-Super-Properties
super_properties = base64.b64encode(
    json.dumps({
        "os": "Windows",
        "browser": "Chrome",
        "device": "",
        "browser_user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "browser_version": "91.0.4472.124",
        "os_version": "10",
        "referrer": "",
        "referring_domain": "",
        "referrer_current": "",
        "referring_domain_current": "",
        "release_channel": "stable",
        "client_build_number": 123456,  # À mettre à jour si possible
        "client_event_source": None
    }).encode()
).decode()

headers = {
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'X-Super-Properties': super_properties
}

# Obtenir le X-Fingerprint
fingerprint_response = requests.get(experiments_url, headers=headers)
if fingerprint_response.status_code == 200:
    headers['X-Fingerprint'] = fingerprint_response.json().get('fingerprint', '')
    print(f"X-Fingerprint: {headers['X-Fingerprint']}")

payload = {
    'login': email,
    'password': password
}

response = requests.post(login_url, json=payload, headers=headers)
if response.status_code == 200:
    print(f"Login response: {response.json()}")
    if 'mfa' in response.json():
        mfa_token = response.json()['ticket']
        print(f"MFA ticket: {mfa_token}")
        two_factor_code = input("Enter your 2FA code (or backup code if using /codes-verification): ")

        # Si vous utilisez un code de secours, changez l'URL en /codes-verification
        # mfa_url = 'https://discord.com/api/v10/auth/mfa/codes-verification'  # Décommentez pour utiliser un code de secours
        mfa_payload = {
            'code': two_factor_code,
            'ticket': mfa_token,
            'gift_code_sku_id': None,
            'login_source': None,
            'allow_ticket': True
        }

        mfa_response = requests.post(mfa_url, json=mfa_payload, headers=headers)
        if mfa_response.status_code == 200:
            token = mfa_response.json()['token']
            print(f'Your Discord token is: {token}')
        else:
            print(f'2FA code verification failed: {mfa_response.status_code} - {mfa_response.text}')
    else:
        token = response.json()['token']
        print(f'Your Discord token is: {token}')
else:
    print(f'Initial authentication failed: {response.status_code} - {response.text}')
