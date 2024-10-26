# utils.py

import base64
import requests
from django.conf import settings
from datetime import datetime

def generate_token():
    api_url = settings.M_PESA['BASE_URL'] + settings.M_PESA['TOKEN_URL']
    api_key = settings.M_PESA['CONSUMER_KEY']
    api_secret = settings.M_PESA['CONSUMER_SECRET']
    headers = {
        'Authorization': 'Basic ' + base64.b64encode(f'{api_key}:{api_secret}'.encode()).decode('utf-8'),
        'Content-Type': 'application/json'
    }
    response = requests.get(api_url, headers=headers)
    json_response = response.json()
    return json_response['access_token']

def lipa_na_mpesa_online(phone_number, amount):
    api_url = settings.M_PESA['BASE_URL'] + settings.M_PESA['LIPA_URL']
    access_token = generate_token()
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    payload = {
        "BusinessShortCode": settings.M_PESA['LIPA_NG'],
        "Password": settings.M_PESA['LIPA_PASS'],
        "Timestamp": datetime.now().strftime('%Y%m%d%H%M%S'),
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone_number,
        "PartyB": settings.M_PESA['LIPA_NG'],
        "PhoneNumber": phone_number,
        "CallBackURL": 'https://yourdomain.com/callback/',
        "AccountReference": "Test123",
        "TransactionDesc": "Payment for testing"
    }
    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()
