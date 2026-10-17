# A failed fetch is not an unchanged document

A Web/PDF monitor needs two independent facts: whether retrieval and extraction succeeded, and whether successfully extracted content differs from the last successful observation. Collapsing these into one boolean hides outages.

## Keep the last good baseline

Suppose the last document says `price=10`. The next request times out. Calling that timeout “unchanged” is misleading: no comparison was possible. Replacing the fingerprint with empty data also loses the baseline. Preserve the last successful fingerprint and record the failure separately.

| Observation | Comparison state | Baseline action |
| --- | --- | --- |
| Successful retrieval/extraction, different bytes | changed | Store new fingerprint |
| Successful retrieval/extraction, same bytes | unchanged | Retain fingerprint |
| Transport, HTTP, or extraction failure | unavailable | Retain last successful fingerprint |

The first successful observation is `initial`, a bootstrap state, not a claim that the market or source changed.

## Run the independent free sample

From this repository's root, with Python 3.9+:

```sh
python3 change_monitor/demo.py
python3 -m unittest discover -s tests -v
```

No dependencies, accounts, keys, purchases, or external requests are needed. [The source](../change_monitor/demo.py) uses fictional in-memory HTTP statuses and byte strings; it is not an HTTP/PDF downloader. Actual expected offline output:

```text
initial
unchanged
unavailable
unchanged
changed
changed
```

The third observation simulates a transport failure. The fourth is unchanged because the failed read did not destroy the last-good fingerprint. The final empty byte string is a successful empty result in this fixture. Real extractors must validate that an empty result is legitimate before passing it to the comparison.

## Failure must remain visible

The `observe(last_good, http_status, content)` function compares only 2xx responses with validated byte content. A non-2xx response, missing status, or failed extraction (`content=None`) returns `unavailable` without changing the baseline. It deliberately does not treat HTTP 304 as unchanged: support for conditional retrieval requires a valid cached representation and is outside this sample.

```sh
python3 change_monitor/demo.py --simulate-failure
```

This prints `unavailable` and exits **2**. The ordinary offline sequence exits 0 only when its demonstration assertions match; it is not a successful live-network check. The tests cover initial, unchanged, changed, timeout/403/500/304/extraction failure, baseline preservation, empty success, invalid types, and CLI exit codes.

When adapting this function, catch only expected transport/extraction exceptions, record failure separately, and return a failure exit status from a real monitoring command. Do not swallow errors into “unchanged”.

## Boundaries before production

- Persist source identity, fingerprint, and last-success time atomically. This sample is memory-only.
- Record failed-observation time separately from last-success time.
- Normalize deliberately; stripping meaningful content creates false negatives. Version extraction rules when their meaning changes.
- A hash mismatch says bytes changed, not what changed or whether it matters. It is not OCR, a semantic diff, or an evidence archive.
- Before adding HTTP, verify access permission and source rules; enforce size/time limits, safe redirects, and network-target restrictions. Never hand arbitrary untrusted URLs to a privileged fetcher.
- Use bounded retries and backoff. A successful HTTP response alone does not prove valid PDF parsing or useful content.

## Inspect output before choosing a tool

The [existing actual-output demo](https://buildshelfkits.com/demos/verified-workflows/?utm_source=github&utm_medium=repository&utm_campaign=last_good_baseline_20261017&utm_content=article#website-pdf) shows a separate Node.js kit's synthetic initial/unchanged/changed output. It is not this Python snippet and does not certify your production environment.

| | This free sample | Website/PDF Mini |
| --- | --- | --- |
| Form | Independent Python educational code | Node.js developer CLI source kit |
| Inputs | Synthetic status and byte fixtures; no network | Website/PDF change-detection workflow requiring setup |
| Storage | In-memory last-good fingerprint | Last-success change detection, not a historical archive |
| Included here | Transition logic and offline tests | Not included in this free repository |
| Not promised | HTTP fetcher, PDF parsing, persistence, alerts | OCR, browser rendering, rich diff, evidence ZIP, built-in scheduler or alerts |

If that packaged scope fits, [Website/PDF Mini is $15 on Gumroad](https://xinjiaantian.gumroad.com/l/website-pdf-change-detector-mini?utm_source=github&utm_medium=repository&utm_campaign=last_good_baseline_20261017&utm_content=article_store). Check its current requirements before purchase. Node 22.13+ is documented; our recorded demo used local Node 25, not Windows/Linux certification. The free example stands alone and requires no purchase.

**Disclosure:** BuildShelf sells the linked kit. This article and independent sample were prepared with AI assistance and checked with synthetic tests. No customer results, production deployment, or time savings are claimed. The free code and article use this repository's existing [MIT license](../LICENSE); the commercial product has separate terms. No paid product source is included.
