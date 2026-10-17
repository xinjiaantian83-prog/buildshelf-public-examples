# BuildShelf public examples

Small, runnable Python examples for common import, webhook, and change-monitoring mistakes. They use only the Python standard library and synthetic data. Each example is useful on its own; none is a hosted service or a production-ready application.

## Change monitoring: a failed fetch is not unchanged

Read [the last-good-baseline tutorial](docs/last-good-baseline.md) and run the [independent free sample](change_monitor/demo.py):

```sh
python3 change_monitor/demo.py
python3 -m unittest discover -s tests -v
```

The fictional sequence prints `initial`, `unchanged`, `unavailable`, `unchanged`, `changed`, `changed`. A failed read preserves the last successful fingerprint. Run `python3 change_monitor/demo.py --simulate-failure` to print `unavailable` and exit with code `2`, not a successful monitoring result. No external requests are made. The tutorial links to actual-output demos and explains the paid kit's different scope. Prepared with AI assistance and checked with synthetic tests.

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

## PDF to Excel workflow demo

For teams that repeatedly copy invoice, order, or report fields into a fixed workbook, BuildShelf also offers a [Japanese PDF-to-Excel automation service](https://buildshelfkits.com/ja/services/pdf-excel-automation?utm_source=github&utm_medium=repository&utm_campaign=pdf_excel_service&utm_content=readme). The page includes a synthetic invoice PDF and its converted CSV so the source-to-row mapping can be checked without exposing customer data. It is a scoped implementation service, not a universal one-click OCR accuracy claim.

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

## Approval workflow: try the interactive demo

Before buying or implementing an approval system, [try the free approval workflow demo](https://buildshelfkits.com/ja/demos/approval-workflow?utm_source=github&utm_medium=repository&utm_campaign=public_examples&utm_content=approval_demo) to inspect request, approval, return, and audit-history flows. The [Approval Workflow & Audit Trail source kit](https://buildshelfkits.com/ja/products/approval-workflow-audit-trail?utm_source=github&utm_medium=repository&utm_campaign=public_examples&utm_content=approval_kit) provides a Python/SQLite starting point for approval state, delegation, notifications, and audit trails. Integrating your own authentication, notification provider, and business rules remains your responsibility; this is not a hosted production approval service.

## Tests

```sh
python3 -m unittest discover -s tests -v
```

Python 3.9+ is sufficient. No packages, API keys, accounts, network access, or real customer data are needed.

Japanese walkthroughs: [CSV row errors](docs/csv-row-errors-ja.md) and [Stripe/GitHub webhook verification](docs/webhook-signatures-ja.md).

The tested CSV example is also explained in a [BuildShelf Zenn article](https://zenn.dev/buildshelf/articles/9e99b107e196c6) with the header, row-number, and exit-code decisions shown step by step.

The webhook example is explained in a [BuildShelf Qiita article](https://qiita.com/buildshelf/items/3805b1a1b69ff32d213f) covering raw request bytes, Stripe's signed timestamp, GitHub's lack of a signed timestamp, and the limits of process-local duplicate tracking.

## Disclosure and license

BuildShelf publishes these examples and sells the linked source-code kits. This repository contains independent free examples, not the paid kit source. The examples are MIT licensed; see [LICENSE](LICENSE).
