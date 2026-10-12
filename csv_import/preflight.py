"""Free CSV row-error preflight; deliberately does not import data."""

import csv
import sys


def inspect(path: str) -> int:
    with open(path, newline="", encoding="utf-8-sig") as source:
        rows = csv.reader(source)
        header = next(rows, None)
        if not header or len(header) != len(set(header)):
            print("header_error: empty or duplicate column name")
            return 1
        required = {"Product Code", "Stock"}
        if not required.issubset(header):
            print("header_error: Product Code and Stock are required")
            return 1
        columns = {name: index for index, name in enumerate(header)}
        invalid = 0
        for number, row in enumerate(rows, start=2):
            errors = []
            if len(row) != len(header):
                errors.append("column_count")
            else:
                if not row[columns["Product Code"]].strip():
                    errors.append("missing_product_code")
                try:
                    if int(row[columns["Stock"]]) < 0:
                        errors.append("negative_stock")
                except ValueError:
                    errors.append("invalid_stock")
            if errors:
                invalid += 1
                print(f"row {number}: {','.join(errors)}")
        print(f"invalid_rows={invalid}")
        return 2 if invalid else 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python3 csv_import/preflight.py input.csv", file=sys.stderr)
        raise SystemExit(1)
    try:
        raise SystemExit(inspect(sys.argv[1]))
    except (OSError, csv.Error) as error:
        print(f"input_error: {type(error).__name__}", file=sys.stderr)
        raise SystemExit(1)
