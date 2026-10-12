"""Run two synthetic first/duplicate deliveries without a network call."""

import hashlib
import hmac
import json

try:
    from webhook_signature.verify import classify_once, verify_github, verify_stripe
except ModuleNotFoundError:
    from verify import classify_once, verify_github, verify_stripe


def run() -> None:
    secret = "synthetic-demo-secret"
    raw = json.dumps({"id": "evt_example", "type": "checkout.completed"}, separators=(",", ":")).encode()
    timestamp = 1_700_000_000
    stripe_sig = hmac.new(secret.encode(), str(timestamp).encode() + b"." + raw, hashlib.sha256).hexdigest()
    stripe_id = verify_stripe(raw, f"t={timestamp},v1={stripe_sig}", secret, timestamp)
    seen_stripe = set()
    print("stripe:", classify_once(stripe_id, seen_stripe) + ",", classify_once(stripe_id, seen_stripe))

    github_sig = hmac.new(secret.encode(), raw, hashlib.sha256).hexdigest()
    github_id = verify_github(raw, f"sha256={github_sig}", secret, "synthetic-delivery-1")
    seen_github = set()
    print("github:", classify_once(github_id, seen_github) + ",", classify_once(github_id, seen_github))


if __name__ == "__main__":
    run()
