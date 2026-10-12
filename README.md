# BuildShelf public examples

Small, runnable Python examples for two common import and webhook mistakes. They use only the Python standard library and synthetic data. Each example is useful on its own; neither is a hosted service or a production-ready application.

## CSV: report row errors before importing

```sh
python3 csv_import/preflight.py csv_import/sample.csv
```

Expected output (exit code `2`, meaning invalid rows were found):

```text
row 3: missing_product_code
row 4: invalid_stock
invalid_rows=2
```

The script checks duplicate and required headers, column counts, product codes, and nonnegative integer stock values. It reports row numbers without echoing source values. Adapt these rules and add data-size limits before using untrusted files. Validation alone does not import or commit data.

For column mapping, normalization, JSONL export, and a value-free error file, see [CSV Import Validator Mini](https://buildshelfkits.com/products/csv-validator-mini?utm_source=github&utm_medium=repository&utm_campaign=public_examples&utm_content=csv_mini). The [full CSV/Excel kit](https://buildshelfkits.com/products/csv-excel-import?utm_source=github&utm_medium=repository&utm_campaign=public_examples&utm_content=csv_full) adds staged promotion, rollback, and audit history. A longer [CSV validation guide](https://buildshelfkits.com/articles/csv-import-row-validation?utm_source=github&utm_medium=repository&utm_campaign=public_examples&utm_content=csv_guide) explains the boundary.

## Webhooks: verify the raw body before handling a duplicate

```sh
python3 webhook_signature/demo.py
```

Expected output:

```text
stripe: first, duplicate
github: first, duplicate
```

`webhook_signature/verify.py` implements a small Stripe timestamped HMAC check and a GitHub SHA-256 HMAC check. It classifies duplicates only inside one process using a Python set. It does **not** persist receipts, confirm downstream processing, retry failures, or prevent a first-seen GitHub delivery from being old: GitHub's signature has no signed timestamp. Do not treat this toy receiver as a production replay defense. Keep raw request bytes unchanged, enforce body limits, store secrets safely, and use durable delivery state in a real receiver.

Protocol references: [Stripe's raw-body signature guidance](https://docs.stripe.com/events/manage-webhook-endpoints#signature-errors) and [GitHub's signature validation guidance](https://docs.github.com/en/webhooks/using-webhooks/validating-webhook-deliveries).

For persistent SQLite receipt classification, see [Webhook Signature & Replay Protection Mini](https://buildshelfkits.com/products/webhook-signature-mini?utm_source=github&utm_medium=repository&utm_campaign=public_examples&utm_content=webhook_mini). The [full reliability kit](https://buildshelfkits.com/products/webhook-reliability?utm_source=github&utm_medium=repository&utm_campaign=public_examples&utm_content=webhook_full) adds queueing, retries, dead letters, and guarded replay. The [webhook reliability guide](https://buildshelfkits.com/articles/production-webhook-reliability?utm_source=github&utm_medium=repository&utm_campaign=public_examples&utm_content=webhook_guide) discusses the failure lifecycle.

## Tests

```sh
python3 -m unittest discover -s tests -v
```

Python 3.9+ is sufficient. No packages, API keys, accounts, network access, or real customer data are needed.

Japanese walkthroughs: [CSV row errors](docs/csv-row-errors-ja.md) and [Stripe/GitHub webhook verification](docs/webhook-signatures-ja.md).

The tested CSV example is also explained in a [BuildShelf Zenn article](https://zenn.dev/buildshelf/articles/9e99b107e196c6) with the header, row-number, and exit-code decisions shown step by step.

## Disclosure and license

BuildShelf publishes these examples and sells the linked source-code kits. This repository contains independent free examples, not the paid kit source. The examples are MIT licensed; see [LICENSE](LICENSE).
