# CSV取込で「何行目の何が悪いか」を返す最小実装

BuildShelf運営者が公開する、標準ライブラリだけで動く例です。CSVを読み込めたことと、業務データとして取り込めることは別です。列が足りない行や、整数であるべき在庫数に文字が入った行を、データベースへ書く前に見つけます。

## 試す

このリポジトリのルートで実行します。Python 3.9以上で追加パッケージは不要です。

```sh
python3 csv_import/preflight.py csv_import/sample.csv
```

実測出力は次の通りです。終了コード2は「ファイルを読めたが、不正な行があった」を表します。

```text
row 3: missing_product_code
row 4: invalid_stock
invalid_rows=2
```

[`preflight.py`](../csv_import/preflight.py)は最初にヘッダー重複と必須列を確認し、各行で列数、商品コード、在庫数を検査します。行番号はヘッダーを1行目として数えています。エラーメッセージに元の値を出さないので、ログに個人情報や機密値が紛れ込む可能性を減らせます。

## 取り込みとは分ける

この例は「事前チェック」です。有効な行をDBへ反映しません。実運用では、列名の対応付け、値の正規化、行間の重複、検証済みデータの出力、反映トランザクションを別に設計します。ファイルサイズと行数の上限、文字コードの扱いも対象に合わせて追加してください。

テストは `python3 -m unittest discover -s tests -v` で実行できます。正常行、ヘッダー重複、列数不足、負数、サンプル中の不正行を検証します。

この無料例の先を実装済みソースで始めたい場合は、[CSV Import Validator Mini](https://buildshelfkits.com/ja/products/csv-validator-mini?utm_source=github&utm_medium=repository&utm_campaign=public_examples&utm_content=csv_guide_ja)（列マッピング、正規化、行別検証、JSONL出力）と[本版](https://buildshelfkits.com/ja/products/csv-excel-import?utm_source=github&utm_medium=repository&utm_campaign=public_examples&utm_content=csv_full_ja)（限定的XLSX、ステージング、反映・取消・監査）を比較できます。販売元はBuildShelfです。
