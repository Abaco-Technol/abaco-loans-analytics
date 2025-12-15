#!/bin/bash
set -e

echo ">>> [1/3] Initializing Cascade Data Generation..."
# Ensure we have the latest data structure
python3 scripts/generate_abaco_portfolio_sample.py

echo ">>> [2/3] Executing Cascade Ingestion Pipeline..."
# Run the pipeline to process the generated sample
python3 scripts/run_data_pipeline.py \
    --input "data_samples/abaco_portfolio_sample.csv" \
    --user "don" \
    --action "init_upload"

echo ">>> [3/3] Committing and Uploading..."
# Git initialization and upload sequence
if [ ! -d ".git" ]; then
    git init
    git branch -M main
fi

git add .
git commit -m "chore: update cascade information and init repo" || echo "No changes to commit"

# Push if remote is configured
git push origin main || echo "⚠️  Remote 'origin' not configured or push failed. Data is committed locally."

echo "✅ Execution Complete. Current information from Cascade processed."