"""Independent MIT-licensed teaching example; synthetic inputs, no network."""
import argparse
from hashlib import sha256


def observe(last_good, http_status, content):
    """HTTP success AND validated extracted bytes are required for comparison.

    None status represents a transport failure; None content a failed extraction.
    A 304 without a validated cached representation is deliberately unavailable.
    """
    if http_status is None or not 200 <= http_status < 300 or content is None:
        return "unavailable", last_good
    if not isinstance(content, bytes):
        raise TypeError("content must be validated bytes or None")
    fingerprint = sha256(content).hexdigest()
    state = "initial" if last_good is None else "unchanged" if fingerprint == last_good else "changed"
    return state, fingerprint


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--simulate-failure", action="store_true")
    args = parser.parse_args()
    if args.simulate_failure:
        print(observe(None, None, None)[0])
        return 2
    baseline = None
    expected = ["initial", "unchanged", "unavailable", "unchanged", "changed", "changed"]
    fixtures = [(200,b"price=10"),(200,b"price=10"),(None,None),(200,b"price=10"),(200,b"price=12"),(200,b"")]
    actual = []
    for status, content in fixtures:
        state, baseline = observe(baseline, status, content)
        actual.append(state)
        print(state)
    # Zero means the offline demonstration matched its assertions, not a live fetch succeeded.
    return 0 if actual == expected else 1


if __name__ == "__main__":
    raise SystemExit(main())
