# ログ自動レポート（Log Auto Report）

## 概要
アプリケーションログ（.log / .txt）を自動解析し、  
**ログ件数の集計・可視化・CSV出力** を行う Python ツールです。

手作業でのログ確認や一次分析を自動化することを目的としています。

## Before / After

- **Before**：ログファイルを目視・grepで確認し、件数や傾向を手作業で把握  
- **After**：ログを input/ に置いて実行するだけで、日別件数・レベル別集計・グラフを自動生成

---

## 想定利用シーン

- サーバー / アプリケーションログの一次分析
- INFO / WARN / ERROR の発生傾向を把握したい
- 日別のログ件数を可視化したい
- 障害調査や運用レポート作成の前段階

ログファイルを `input/` に入れて実行するだけで、  
**集計・CSV出力・グラフ生成** までを自動で行います。

---

## フォルダ構成

```text
sales_auto_report/
├─ input/      # 売上CSVファイル（date, product, price, quantity）
├─ output/     # 集計結果（CSV / PNG）
├─ main.py     # メインスクリプト
├─ .gitignore
└─ README.md
```

---

## 対応ログ形式（例）

```
2026-02-02 12:34:56 INFO Application started
[2026-02-02 12:35:10] [ERROR] Database connection failed
2026-02-02T12:36:01Z WARN Slow response detected
```

---

## 機能

- ログファイルの自動解析
- 日別ログ件数の集計
- ログレベル別（INFO / WARN / ERROR）件数集計
- 集計結果を CSV 形式で出力
- 集計結果をグラフ（PNG）として可視化

※ 不正な行（price/quantityが数値でない、dateが解析できない等）は自動で除外して集計します。

---

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

### 日別売上
![Daily Sales](output/report_20260202_184001/daily_sales.png)

### 売上TOP5
![Top5 Products](output/report_20260202_184001/top5_products.png)

---

## 使い方

### 1. ログファイルを配置

```
input/app.log
```

### 2. 実行

```bash
python3 main.py --top 10
```

## 引数（CLIオプション）

このスクリプトは、実行時に引数を指定することで挙動を変更できます。

- `--input-dir`  
  入力CSVのフォルダパス（デフォルト：`input`）

- `--output-dir`  
  出力先フォルダパス（デフォルト：`output`）

- `--top`  
  売上上位N商品の表示件数（デフォルト：`5`）

### 使用例

```bash
# デフォルト設定で実行
python3 main.py

# Top10商品を出力
python3 main.py --top 10

# 入力・出力フォルダを指定
python3 main.py --input-dir data --output-dir result

## 引数（オプション）

このツールは、入力フォルダ・出力フォルダ・Top件数を引数で変更できます。

### 例（全部指定）
```bash
python3 main.py --input-dir input --output-dir output --top 5

---

	•	概要
	•	フォルダ構成
	•	使い方（input → 実行）
	•	Before / After
	•	出力されるファイル・グラフ