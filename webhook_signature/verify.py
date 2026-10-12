"""Educational raw-body HMAC checks and process-local duplicate example."""

import hashlib
import hmac
import json
import re


def verify_stripe(raw: bytes, header: str, secret: str, now: int) -> str:
    """Return the verified Stripe event ID, or raise ValueError."""
    if not 0 < len(raw) <= 1024 * 1024:
        raise ValueError("body size")
    fields = [part.strip().partition("=") for part in header.split(",")]
    timestamps = [value for key, sep, value in fields if sep and key == "t"]
    signatures = [value for key, sep, value in fields if sep and key == "v1"]
    if len(timestamps) != 1 or not re.fullmatch(r"[0-9]{1,12}", timestamps[0]):
        raise ValueError("timestamp header")
    if not 1 <= len(signatures) <= 8 or any(not re.fullmatch(r"[0-9a-f]{64}", value) for value in signatures):
        raise ValueError("signature header")
    timestamp = int(timestamps[0])
    if abs(now - timestamp) > 300:
        raise ValueError("stale timestamp")
    signed = timestamps[0].encode() + b"." + raw
    expected = hmac.new(secret.encode(), signed, hashlib.sha256).hexdigest()
    if not any(hmac.compare_digest(expected, value) for value in signatures):
        raise ValueError("bad signature")
    event = json.loads(raw)
    if not isinstance(event, dict) or not isinstance(event.get("id"), str) or not event["id"]:
        raise ValueError("event ID")
    return event["id"]


def verify_github(raw: bytes, header: str, secret: str, delivery_id: str) -> str:
    """Return the verified delivery ID, or raise ValueError."""
    if not 0 < len(raw) <= 1024 * 1024:
        raise ValueError("body size")
    if not re.fullmatch(r"sha256=[0-9a-f]{64}", header):
        raise ValueError("signature header")
    if not re.fullmatch(r"[A-Za-z0-9-]{1,128}", delivery_id):
        raise ValueError("delivery ID")
    expected = hmac.new(secret.encode(), raw, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, header[7:]):
        raise ValueError("bad signature")
    return delivery_id


def classify_once(identity: str, seen: set) -> str:
    """Process-local illustration only; a restart forgets every identity."""
    if identity in seen:
        return "duplicate"
    seen.add(identity)
    return "first"
