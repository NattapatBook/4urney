import base64
import uuid

def short_uuid4():
    return base64.b32encode(uuid.uuid4().bytes).decode().strip('=')