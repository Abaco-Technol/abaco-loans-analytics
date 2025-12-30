#!/usr/bin/env python3
"""
Automated batch runner for client financial analysis notebook.
- Runs the notebook for all (or a sample of) client_ids.
- Exports results to outputs/ as CSV/XLS/JSON.
- Designed for CI/CD or scheduled automation.

Usage:
    python scripts/run_client_analysis_batch.py --notebook notebooks/client_financial_analysis.ipynb [--all] [--sample 10]

Requirements:
- papermill
- pandas
- openpyxl
- (optionally) jupyter
"""
import os
import argparse
import pandas as pd
from pathlib import Path
import papermill as pm
from datetime import datetime

def get_client_ids(loans_path: str) -> list:
    df = pd.read_parquet(loans_path) if loans_path.endswith('.parquet') else pd.read_csv(loans_path)
    return df['customer_id'].dropna().astype(str).unique().tolist()

def main():
    parser = argparse.ArgumentParser(description="Batch run client analysis notebook.")
    parser.add_argument('--notebook', required=True, help='Path to the analysis notebook')
    parser.add_argument('--all', action='store_true', help='Run for all client_ids')
    parser.add_argument('--sample', type=int, default=10, help='Sample N client_ids (default: 10)')
    parser.add_argument('--loans', default='data/loans.csv', help='Path to loans CSV/Parquet for client_id list')
    parser.add_argument('--outdir', default='outputs', help='Output directory')
    args = parser.parse_args()

    client_ids = get_client_ids(args.loans)
    if not args.all:
        client_ids = client_ids[:args.sample]
    print(f"[INFO] Running analysis for {len(client_ids)} clients.")

    out_dir = Path(args.outdir)
    out_dir.mkdir(exist_ok=True)
    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")

    for cid in client_ids:
        out_nb = out_dir / f"client_{cid}_analysis_{ts}.ipynb"
        print(f"[INFO] Running for client_id={cid}")
        pm.execute_notebook(
            args.notebook,
            str(out_nb),
            parameters=dict(client_id=cid)
        )
        # Optionally, parse and collect outputs here

if __name__ == "__main__":
    main()
