import base64
import json
import hashlib
import hmac
import httplib2
import time

toby_ACCESS_TOKEN = '*'
toby_SECRET_KEY = '*'

ACCESS_TOKEN = '*'
SECRET_KEY = '*'


URL = 'https://api.coinone.co.kr/v1/transaction/coin/'
PAYLOAD = {
  "access_token": ACCESS_TOKEN,
  "address": "16ZMTadHVy6kx6dfVNtu4QyRdg1qXSuQR8",
  "auth_number": 270539,
  "qty": 0.0001,
  "currency": "bch",
}

URL = 'https://api.coinone.co.kr/v2/transaction/auth_number/'
PAYLOAD = {
  "access_token": ACCESS_TOKEN,
  "type": "bch",
}


def get_encoded_payload(payload):
  payload[u'nonce'] = int(time.time()*1000)

  dumped_json = json.dumps(payload)
  encoded_json = base64.b64encode(dumped_json)
  print encoded_json
  return encoded_json

def get_signature(encoded_payload, secret_key):
  signature = hmac.new(str(secret_key).upper(), str(encoded_payload), hashlib.sha512);
  return signature.hexdigest()

def get_response(url, payload):
  encoded_payload = get_encoded_payload(payload)
  headers = {
    'Content-type': 'application/json',
    'X-COINONE-PAYLOAD': encoded_payload,
    'X-COINONE-SIGNATURE': get_signature(encoded_payload, SECRET_KEY)
  }
  http = httplib2.Http()
  response, content = http.request(URL, 'POST', headers=headers, body=encoded_payload)
  print response
  return content

def get_result():
  content = get_response(URL, PAYLOAD)
  print content
  content = json.loads(content)

  return content

if __name__   == "__main__":
    print get_result()
