import contextlib
import hashlib
import hmac
import io
import pathlib
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from csv_import.preflight import inspect
from webhook_signature.verify import classify_once, verify_github, verify_stripe


class CsvTests(unittest.TestCase):
    def check(self, source):
        with tempfile.TemporaryDirectory() as directory:
            path = pathlib.Path(directory) / "input.csv"
            path.write_text(source, encoding="utf-8")
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                status = inspect(str(path))
            return status, output.getvalue()

    def test_synthetic_sample(self):
        status, output = self.check((ROOT / "csv_import/sample.csv").read_text())
        self.assertEqual(status, 2)
        self.assertIn("row 3: missing_product_code", output)
        self.assertIn("row 4: invalid_stock", output)

    def test_clean_file(self):
        self.assertEqual(self.check("Product Code,Stock\nA,0\n")[0], 0)

    def test_duplicate_header(self):
        self.assertEqual(self.check("Product Code,Stock,Stock\nA,1,2\n")[0], 1)

    def test_column_count(self):
        self.assertIn("row 2: column_count", self.check("Product Code,Stock\nA\n")[1])

    def test_negative_stock(self):
        self.assertIn("row 2: negative_stock", self.check("Product Code,Stock\nA,-1\n")[1])


class WebhookTests(unittest.TestCase):
    raw = b'{"id":"evt_demo"}'
    secret = "only-for-synthetic-tests"
    now = 1_700_000_000

    def stripe_header(self, raw=None, timestamp=None):
        raw = self.raw if raw is None else raw
        timestamp = self.now if timestamp is None else timestamp
        signed = str(timestamp).encode() + b"." + raw
        signature = hmac.new(self.secret.encode(), signed, hashlib.sha256).hexdigest()
        return f"t={timestamp},v1={signature}"

    def test_stripe_valid(self):
        self.assertEqual(verify_stripe(self.raw, self.stripe_header(), self.secret, self.now), "evt_demo")

    def test_stripe_rejects_changed_raw_body(self):
        with self.assertRaisesRegex(ValueError, "bad signature"):
            verify_stripe(self.raw + b" ", self.stripe_header(), self.secret, self.now)

    def test_stripe_rejects_stale_timestamp(self):
        with self.assertRaisesRegex(ValueError, "stale timestamp"):
            verify_stripe(self.raw, self.stripe_header(), self.secret, self.now + 301)

    def test_stripe_rejects_duplicate_timestamp_header(self):
        with self.assertRaisesRegex(ValueError, "timestamp header"):
            verify_stripe(self.raw, self.stripe_header() + ",t=1700000000", self.secret, self.now)

    def test_github_valid_and_tampered(self):
        signature = hmac.new(self.secret.encode(), self.raw, hashlib.sha256).hexdigest()
        self.assertEqual(verify_github(self.raw, "sha256=" + signature, self.secret, "delivery-1"), "delivery-1")
        with self.assertRaisesRegex(ValueError, "bad signature"):
            verify_github(self.raw + b" ", "sha256=" + signature, self.secret, "delivery-1")

    def test_github_rejects_invalid_delivery_id(self):
        signature = hmac.new(self.secret.encode(), self.raw, hashlib.sha256).hexdigest()
        with self.assertRaisesRegex(ValueError, "delivery ID"):
            verify_github(self.raw, "sha256=" + signature, self.secret, "bad id")

    def test_process_local_duplicate_classification(self):
        seen = set()
        self.assertEqual(classify_once("delivery-1", seen), "first")
        self.assertEqual(classify_once("delivery-1", seen), "duplicate")
        self.assertEqual(classify_once("delivery-1", set()), "first")


if __name__ == "__main__":
    unittest.main()
