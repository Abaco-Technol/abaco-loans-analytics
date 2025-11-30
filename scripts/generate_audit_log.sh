#!/bin/bash
# Generate a compliant git audit log for a specific date range
# Usage: ./scripts/generate_audit_log.sh "2025-01-01" "2025-12-31"

set -e

START_DATE=$1
END_DATE=$2
OUTPUT_FILE="audit_log_${START_DATE}_to_${END_DATE}.csv"

# Create CSV Header
echo "Commit Hash,Author,Date,Subject,GPG Signature" > $OUTPUT_FILE

# Extract git log with GPG signature verification status (%G?)
git log --since="$START_DATE" --until="$END_DATE" \
    --pretty=format:'"%H","%an","%ad","%s","%G?"' \
    --date=iso >> $OUTPUT_FILE

echo "Audit log generated: $OUTPUT_FILE"

# Verify that all commits have a valid GPG signature ('G')
echo "Verifying GPG signatures..."
if grep -q -v ',"G"' "$OUTPUT_FILE"; then
    echo "WARNING: Unsigned or invalidly signed commits detected!" >&2
    exit 1
fi

echo "SUCCESS: All commits are cryptographically signed."
