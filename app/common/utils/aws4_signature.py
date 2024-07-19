import hashlib
import hmac

def hash_payload(payload):
    return hashlib.sha256(payload.encode('utf-8')).hexdigest()

def create_canonical_request(method, uri, query_string, headers, payload_hash, signed_headers):
    canonical_headers = ''.join(f'{k.lower()}:{v.strip()}\n' for k, v in sorted(headers.items()) if k.lower() in signed_headers)
    signed_headers_str = ';'.join(sorted(signed_headers))
    canonical_request = f"{method}\n{uri}\n{query_string}\n{canonical_headers}\n{signed_headers_str}\n{payload_hash}"
    return canonical_request

def create_string_to_sign(canonical_request, request_date, credential_scope):
    hashed_canonical_request = hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()
    string_to_sign = f"AWS4-HMAC-SHA256\n{request_date}\n{credential_scope}\n{hashed_canonical_request}"
    return string_to_sign

def sign(key, msg):
    return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()

def getSignatureKey(key, dateStamp, regionName, serviceName):
    kDate = sign(('AWS4' + key).encode('utf-8'), dateStamp)
    kRegion = sign(kDate, regionName)
    kService = sign(kRegion, serviceName)
    kSigning = sign(kService, 'aws4_request')
    return kSigning

def calculate_signature(secret_key, date_stamp, region_name, service_name, string_to_sign):
    signing_key = getSignatureKey(secret_key, date_stamp, region_name, service_name)
    signature = hmac.new(signing_key, string_to_sign.encode('utf-8'), hashlib.sha256).hexdigest()
    return signature