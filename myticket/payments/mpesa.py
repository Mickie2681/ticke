import requests
import base64
import datetime
import os
import logging
from dotenv import load_dotenv

load_dotenv()

# Load secrets from environment only — do NOT hard-code secrets here.
CONSUMER_KEY = os.getenv('MPESA_CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('MPESA_CONSUMER_SECRET')
SHORTCODE = os.getenv('MPESA_SHORTCODE')
PASSKEY = os.getenv('MPESA_PASSKEY')
CALLBACK_URL = os.getenv('MPESA_CALLBACK_URL')

logger = logging.getLogger(__name__)


def _require_env_vars(*names):
    missing = [n for n in names if not os.getenv(n)]
    if missing:
        raise EnvironmentError(f"Missing required environment variables: {', '.join(missing)}")


def get_access_token(timeout=10):
    _require_env_vars('MPESA_CONSUMER_KEY', 'MPESA_CONSUMER_SECRET')
    api_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    creds = f"{CONSUMER_KEY}:{CONSUMER_SECRET}"
    headers = {
        "Authorization": "Basic " + base64.b64encode(creds.encode()).decode()
    }
    resp = requests.get(api_url, headers=headers, timeout=timeout)
    resp.raise_for_status()
    data = resp.json()
    token = data.get('access_token')
    if not token:
        logger.error('No access_token in response from MPESA auth')
        raise RuntimeError('Failed to retrieve access token from MPESA')
    logger.debug('Retrieved access token from MPESA')
    return token


def _validate_phone(phone_number: str):
    if not isinstance(phone_number, str):
        raise ValueError('phone_number must be a string')
    digits = ''.join(ch for ch in phone_number if ch.isdigit())
    if len(digits) < 9 or len(digits) > 15:
        raise ValueError('phone_number looks invalid')
    return digits


def _validate_amount(amount):
    try:
        amt = int(amount)
    except Exception:
        raise ValueError('amount must be an integer')
    if amt <= 0:
        raise ValueError('amount must be positive')
    return amt


def stk_push(phone_number, amount, account_reference, transaction_desc, timeout=10):
    _require_env_vars('MPESA_SHORTCODE', 'MPESA_PASSKEY', 'MPESA_CALLBACK_URL')
    access_token = get_access_token(timeout=timeout)
    phone_digits = _validate_phone(phone_number)
    amt = _validate_amount(amount)

    timestamp = datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S')
    password = base64.b64encode(f"{SHORTCODE}{PASSKEY}{timestamp}".encode()).decode()
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    payload = {
        "BusinessShortCode": SHORTCODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amt,
        "PartyA": phone_digits,
        "PartyB": SHORTCODE,
        "PhoneNumber": phone_digits,
        "CallBackURL": CALLBACK_URL,
        "AccountReference": account_reference,
        "TransactionDesc": transaction_desc
    }

    resp = requests.post(api_url, json=payload, headers=headers, timeout=timeout)
    resp.raise_for_status()
    logger.info('STK push request successful (status=%s)', resp.status_code)
    # Avoid logging full response body as it may contain sensitive info
    return resp.json()
