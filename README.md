# 売上CSV → 自動レポート（Sales CSV → Auto Report）

## 概要
売上CSV（`date, product, price, quantity`）を読み込み、
**日別売上 / 商品別売上 / 売上TOP N** を集計し、CSVとグラフ（PNG）を自動生成する Python ツールです。

- input/ にCSVを置いて実行するだけ
- output/report_YYYYMMDD_HHMMSS/ に結果を出力

## Before / After

- **Before**：Excelで集計・グラフ作成を手作業で実施
- **After**：CSVを input/ に置いて実行するだけで、  
  売上集計・税抜/税込切替・CSV/グラフ生成まで自動化

---

## フォルダ構成

```text
sales_csv_auto_report/
├─ input/      # 売上CSVファイル（date, product, price, quantity）
├─ output/     # 集計結果（CSV / PNG）
├─ main.py     # メインスクリプト
├─ .gitignore
└─ README.md
```
## 機能

- 売上CSVの自動読み込み（複数CSV対応）
- 日別売上の集計
- 商品別売上の集計
- 売上TOP N商品の抽出
- 税抜 / 税込（tax-rate指定）売上の切り替え
- 集計結果を CSV / グラフ（PNG）で出力

---

## 派生版としての追加価値（機能差分）

本ツールは、単純な売上集計スクリプトをベースに、
**実務利用を想定した拡張**を加えた派生版です。

### 元ツールとの差分

| 項目 | 元ツール | 本ツール |
|----|----|----|
| 売上集計 | 税抜のみ | **税抜 / 税込を切り替え可能** |
| 消費税対応 | なし | **`--tax-rate` で指定可能** |
| 実行単位 | 固定 | **CLI引数で柔軟に制御** |
| 出力 | CSVのみ | **CSV + グラフ（PNG）** |
| 実務用途 | 検証用 | **請求書チェック / 売上確認に対応** |

### 実務での強み

- 税率を明示的に指定できるため  
  👉 **「税抜・税込どちらで計算したか」が結果から明確**
- CSVベースのため  
  👉 **Excel・スプレッドシートへの再利用が容易**
- 実行ログに依存せず  
  👉 **再現性のある売上レポートを即生成**

## 派生版（sales_csv_auto_report）の差分ポイント

このリポジトリは、元の「自動レポート」ツールを **売上CSV向けに特化**して派生開発した版です。

- ✅ 入力が「売上CSV（date, product, price, quantity）」前提で、集計ロジックを最適化
- ✅ 複数CSVをまとめて結合 → 売上を一括集計できる
- ✅ `--tax-rate` で **税抜 / 税込を切り替え**（請求書チェックや社内レポートに直結）
- ✅ 実行ごとに `output/report_YYYYMMDD_HHMMSS/` に結果を分離して保存（履歴が残る）

## 出力内容

## 出力例（実行後）

実行すると、output 配下にタイムスタンプ付きフォルダが作成されます。

```text
output/
└─ report_YYYYMMDD_HHMMSS/
   ├─ merged_sales.csv
   ├─ daily_sales.csv
   ├─ product_sales.csv
   ├─ top5_products.csv
   ├─ daily_sales.png
   └─ top5_products.png
```

※ 毎回内容が変わるため、出力結果は Git 管理していません。

## CSV出力内容

- `merged_sales.csv`：全CSVを結合した売上データ
- `daily_sales.csv`：日別売上集計
- `product_sales.csv`：商品別売上集計
- `top5_products.csv`：売上上位N商品の一覧

## グラフ出力

- 日別売上グラフ（PNG）
- 売上TOP N 商品グラフ（PNG）

※ グラフは output/report_YYYYMMDD_HHMMSS/ 配下に自動生成されます  
※ 出力例は毎回変わるため、README には固定表示していません
---

## 使い方

### 1. 売上CSVを配置

```text
input/sales_sample.csv
```

### 2. 実行

```bash
python3 main.py --top 10
```

## 引数（CLIオプション）

このスクリプトは、実行時に引数を指定することで挙動を変更できます。

- `--input-dir`：入力CSVのフォルダ（デフォルト：`input`）
- `--output-dir`：出力先フォルダ（デフォルト：`output`）
- `--top`：売上上位の表示件数（デフォルト：`5`）
- `--tax-rate`：消費税率  
  - `0.0`（デフォルト：税抜）
  - `0.08`（税込：8%）
  - 💡 税率を指定することで、税抜・税込どちらの売上集計にも対応  
    実務の請求書チェックや売上レポート作成にそのまま利用可能

### 使用例

```bash
# 税抜（デフォルト）
python3 main.py

# 税込 8%
python3 main.py --tax-rate 0.08

# Top10商品を出力
python3 main.py --top 10

# 入力・出力フォルダを指定
python3 main.py --input-dir data --output-dir result --tax-rate 0.08
```

### 例（全部指定）
```bash
python3 main.py --input-dir input --output-dir output --top 5 --tax-rate 0.08
```