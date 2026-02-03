import argparse
import glob
import os
from datetime import datetime

import pandas as pd
import matplotlib.pyplot as plt

INPUT_DIR = "input"
OUTPUT_DIR = "output"

def make_run_dir(base_dir):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = os.path.join(base_dir, f"report_{ts}")
    os.makedirs(run_dir, exist_ok=True)
    return run_dir

def parse_args():
    parser = argparse.ArgumentParser(
        description="売上CSV → 自動レポート（Sales CSV → Auto Report）"
    )
    parser.add_argument(
        "--input-dir",
        default=INPUT_DIR,
        help="入力CSVのフォルダ（デフォルト：input）",
    )
    parser.add_argument(
        "--output-dir",
        default=OUTPUT_DIR,
        help="出力先フォルダ（デフォルト：output）",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=5,
        help="売上上位の表示件数（デフォルト：5）",
    )
    parser.add_argument(
        "--tax-rate",
        type=float,
        default=0.0,
        help="消費税(デフォルト：0.0=税抜)"
    )
    return parser.parse_args()


def ensure_dirs(input_dir: str, output_dir: str):
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)


def find_csv_files(input_dir):
    files = glob.glob(os.path.join(input_dir, "*.csv"))
    if not files:
        raise FileNotFoundError(f"CSVが見つかりません: {input_dir} に .csv を入れてください")
    return files


def load_and_concat_csv(files, tax_rate: float):
    dfs = []

    for f in files:
        df = pd.read_csv(f)

        # 必須列チェックなど（ここはあなたのままでOK）
        required_cols = {"date", "product", "price", "quantity"}
        missing = required_cols - set(df.columns)
        if missing:
            raise ValueError(f"{os.path.basename(f)} に必須列がありません: {missing}")

        df["price"] = pd.to_numeric(df["price"], errors="coerce")
        df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
        df = df[df["price"].notna() & df["quantity"].notna()]

        df["source_file"] = os.path.basename(f)
        dfs.append(df)

    # ✅ forループの外（ここ重要）
    df_all = pd.concat(dfs, ignore_index=True)

    df_all["date"] = pd.to_datetime(df_all["date"], errors="coerce")
    df_all = df_all[df_all["date"].notna()]

    df_all["sales"] = (df_all["price"] * df_all["quantity"]).round(2)

    # ✅ ここで税込売上（df_allが存在してから！）
    df_all["sales_with_tax"] = (df_all["sales"] * (1 + tax_rate)).round(2)

    df_all["date"] = df_all["date"].dt.date

    return df_all

def summarize(df_all, top_n: int = 5, sales_col: str = "sales"):
    daily = (
        df_all.groupby("date", as_index=False)[sales_col]
        .sum()
        .sort_values("date")
        .rename(columns={sales_col: "sales"})
    )

    product = (
        df_all.groupby("product", as_index=False)[sales_col]
        .sum()
        .sort_values(sales_col, ascending=False)
        .rename(columns={sales_col: "sales"})
    )

    topn = product.head(top_n)
    return daily, product, topn


def export_csv(df_all, daily, product, top5, run_dir):
    df_all.to_csv(os.path.join(run_dir, "merged_sales.csv"), index=False)
    daily.to_csv(os.path.join(run_dir, "daily_sales.csv"), index=False)
    product.to_csv(os.path.join(run_dir, "product_sales.csv"), index=False)
    top5.to_csv(os.path.join(run_dir, "top5_products.csv"), index=False)


def export_graphs(daily, top5, run_dir: str):
    daily_sorted = daily.sort_values("date")
    plt.figure(figsize=(10, 5))
    plt.plot(daily_sorted["date"], daily_sorted["sales"], marker="o")
    plt.title("Daily Sales")
    plt.xlabel("Date")
    plt.ylabel("Sales")
    plt.tight_layout()
    plt.savefig(os.path.join(run_dir, "daily_sales.png"), dpi=200)
    plt.close()

    top5_sorted = top5.sort_values("sales", ascending=False)
    plt.figure(figsize=(10, 5))
    plt.bar(top5_sorted["product"], top5_sorted["sales"])
    plt.title("Top Products by Sales")
    plt.xlabel("Product")
    plt.ylabel("Sales")
    plt.tight_layout()
    plt.savefig(os.path.join(run_dir, "top5_products.png"), dpi=200)
    plt.close()


def main():
    args = parse_args()

    ensure_dirs(args.input_dir, args.output_dir)
    run_dir = make_run_dir(args.output_dir)

    files = find_csv_files(args.input_dir)
    df_all = load_and_concat_csv(files, args.tax_rate)
    
    sales_col = "sales_with_tax" if args.tax_rate != 0 else "sales"

    daily, product, top5 = summarize(
        df_all,
        top_n=args.top,
        sales_col=sales_col
    )
    export_csv(df_all, daily, product, top5, run_dir)
    export_graphs(daily, top5, run_dir)

    print("✅ 完了")
    print("出力先:", run_dir)


if __name__ == "__main__":
    main()