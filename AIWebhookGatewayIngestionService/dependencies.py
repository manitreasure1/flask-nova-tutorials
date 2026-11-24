import hmac
import hashlib
from flask import request
from flask_nova import HTTPException, status


SECRET_TOKEN = "webhook-key" # todo: env


def verify_webhook_signature() -> None:
    signature = request.headers.get("X-Signature")
    if not signature:
        raise HTTPException(
            status_code=status.UNAUTHORIZED,
            detail="Missing X-Signature header"
        )


    expected = hmac.new(
        SECRET_TOKEN.encode('utf-8'),
        request.get_data(),
        hashlib.sha256
    ).hexdigest()


    if not hmac.compare_digest(signature, expected):
        raise HTTPException(
            status_code=status.FORBIDDEN,
            detail="Invalid signature digest"
        )






