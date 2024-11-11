import hmac
import hashlib
import base64
from django.shortcuts import render

def verify_line_signature(request_body: bytes, signature: str, channel_secret: str) -> bool:
    """
    Verifies the signature of a LINE webhook event.

    Args:
        request_body (bytes): The raw request body as a bytes object.
        signature (str): The value of the X-Line-Signature header.
        channel_secret (str): Your LINE channel secret.

    Returns:
        bool: True if the signature is valid, False otherwise.
    """
    # Create an HMAC hash using SHA256
    hash = hmac.new(
        channel_secret.encode('utf-8'),
        request_body,
        hashlib.sha256
    ).digest()

    # Calculate the base64-encoded signature
    calculated_signature = base64.b64encode(hash).decode('utf-8')

    # Return whether the calculated signature matches the provided one
    return calculated_signature == signature
