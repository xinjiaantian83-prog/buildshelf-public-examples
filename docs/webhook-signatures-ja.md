# Stripe/GitHub Webhookで署名検証と重複配信を分けて考える

BuildShelf運営者による、Python標準ライブラリだけの実行例です。署名検証は「本文が正しい秘密鍵で署名されたか」を確認します。重複判定は「同じ配信をすでに扱ったか」を確認します。目的が異なるため、両方が必要です。

## まず生の本文を検証する

[`verify.py`](../webhook_signature/verify.py)は、JSONとして解析する前の`bytes`をHMAC-SHA256へ渡します。JSONへ変換してから再シリアライズすると、空白やキー順の違いで署名対象が変わります。比較には`hmac.compare_digest`を使います。

Stripe例では`Stripe-Signature`の`t`と`v1`を読み、署名と時刻差300秒以内を確認してからイベントIDを取り出します。GitHub例では`X-Hub-Signature-256`と`X-GitHub-Delivery`を確認します。**GitHubの署名には時刻が含まれないため、初めて見る正当な署名が新しい配信だとは証明できません。**

```sh
python3 webhook_signature/demo.py
python3 -m unittest discover -s tests -v
```

合成データで実際に得た出力:

```text
stripe: first, duplicate
github: first, duplicate
```

この`first`/`duplicate`はPythonの`set`による**同一プロセス内だけ**の例です。再起動すると消え、複数プロセス間でも共有されません。業務処理が失敗した配信を`first`と記録したままにする危険もあります。実運用では永続的な受信状態、処理完了状態、復旧経路を設計してください。テストには本文改変、古いStripe時刻、不正な配信IDが含まれます。

プロトコルの根拠は[Stripe公式の署名検証資料](https://docs.stripe.com/events/manage-webhook-endpoints#signature-errors)と[GitHub公式の検証資料](https://docs.github.com/en/webhooks/using-webhooks/validating-webhook-deliveries)です。

永続的なSQLite重複判定が必要なら[Webhook Mini](https://buildshelfkits.com/ja/products/webhook-signature-mini?utm_source=github&utm_medium=repository&utm_campaign=public_examples&utm_content=webhook_guide_ja)、キュー・再試行・DLQ・安全な再実行まで必要なら[本版](https://buildshelfkits.com/ja/products/webhook-reliability?utm_source=github&utm_medium=repository&utm_campaign=public_examples&utm_content=webhook_full_ja)の機能範囲を確認できます。販売元はBuildShelfです。
