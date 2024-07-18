import hashlib
import hmac
import datetime

def hash_payload(payload):
    return hashlib.sha256(payload.encode('utf-8')).hexdigest()

def create_canonical_request(method, uri, query_string, headers, payload_hash):
    canonical_headers = ''.join(f'{k}:{v}\n' for k, v in headers.items())
    signed_headers = ';'.join(headers.keys())
    canonical_request = f"{method}\n{uri}\n{query_string}\n{canonical_headers}\n{signed_headers}\n{payload_hash}"
    return canonical_request

def create_string_to_sign(canonical_request, request_date, credential_scope):
    hashed_canonical_request = hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()
    string_to_sign = f"AWS4-HMAC-SHA256\n{request_date}\n{credential_scope}\n{hashed_canonical_request}"
    return string_to_sign

def sign(key, msg):
    return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()

def get_signature_key(key, date_stamp, region_name, service_name):
    k_date = sign(('AWS4' + key).encode('utf-8'), date_stamp)
    k_region = sign(k_date, region_name)
    k_service = sign(k_region, service_name)
    k_signing = sign(k_service, 'aws4_request')
    return k_signing

def calculate_signature(secret_key, date_stamp, region_name, service_name, string_to_sign):
    signing_key = get_signature_key(secret_key, date_stamp, region_name, service_name)
    signature = hmac.new(signing_key, string_to_sign.encode('utf-8'), hashlib.sha256).hexdigest()
    return signature