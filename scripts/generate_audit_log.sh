#!/bin/bash
# Vibe Solutioning Audit Trail Generator
# Purpose: Generate comprehensive audit logs for compliance and traceability
# Enforces: Zero tolerance for fragility, Traceability is King, Code is Law

set -euo pipefail  # Exit on error, undefined variables, pipe failures

# Configuration
LOG_FILE="audit_log.json"
LOG_DIR="${LOG_DIR:-.}"
FULL_LOG_PATH="${LOG_DIR}/${LOG_FILE}"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
COMMIT_SHA="${COMMIT_SHA:-$(git rev-parse HEAD 2>/dev/null || echo 'unknown')}"
PR_NUMBER="${PR_NUMBER:-0}"
BRANCH="${GITHUB_REF_NAME:-$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo 'unknown')}"
REPO="${GITHUB_REPOSITORY:-unknown}"
ACTOR="${GITHUB_ACTOR:-automation}"
RUN_ID="${GITHUB_RUN_ID:-0}"

# Color output for terminals
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'  # No Color

# Functions
log_message() {
    echo -e "${GREEN}[AUDIT]${NC} $1"
}

error_message() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

warning_message() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

# Initialize audit log
initialize_audit_log() {
    log_message "Initializing audit log for commit: $COMMIT_SHA"
    
    # Create audit directory if it doesn't exist
    mkdir -p "$LOG_DIR"
    
    # Start with metadata
    cat > "$FULL_LOG_PATH" <<EOF
{
  "metadata": {
    "generated_at": "$TIMESTAMP",
    "commit_sha": "$COMMIT_SHA",
    "branch": "$BRANCH",
    "pull_request": $PR_NUMBER,
    "repository": "$REPO",
    "actor": "$ACTOR",
    "workflow_run_id": "$RUN_ID",
    "tool_version": "1.0.0",
    "compliance_framework": "Vibe Solutioning"
  },
  "events": []
}
EOF
}

# Add audit event
add_audit_event() {
    local event_type="$1"
    local event_description="$2"
    local event_status="${3:-success}"
    local event_timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    
    # Create temporary file
    local temp_file=$(mktemp)
    
    # Extract events array and add new event
    jq ".events += [{\"timestamp\": \"$event_timestamp\", \"type\": \"$event_type\", \"description\": \"$event_description\", \"status\": \"$event_status\"}]" "$FULL_LOG_PATH" > "$temp_file"
    
    # Replace original file
    mv "$temp_file" "$FULL_LOG_PATH"
}

# Scan for code quality violations
scan_code_quality() {
    log_message "Scanning for code quality violations..."
    
    # Check for financial calculations using float (should use Decimal)
    if git diff HEAD~1 HEAD -- '*.py' '*.ts' '*.tsx' | grep -E 'float.*amount|float.*price|float.*rate|float.*balance'; then
        add_audit_event "code_quality_violation" "Financial data using float instead of Decimal" "warning"
        warning_message "Financial data should use Decimal type, not float"
    else
        add_audit_event "code_quality_check" "Financial data validation passed" "success"
        log_message "✓ Financial data validation passed"
    fi
    
    # Check for hardcoded secrets
    if git diff HEAD~1 HEAD | grep -iE 'password|api_key|secret|token|credentials' | grep -v '# ' | grep -v 'skip'; then
        add_audit_event "security_violation" "Potential secrets detected in code" "critical"
        error_message "Secrets detected in code diff!"
        return 1
    else
        add_audit_event "security_check" "No secrets detected in code diff" "success"
        log_message "✓ Security check passed (no secrets detected)"
    fi
}

# Check for fragile code patterns
scan_fragility() {
    log_message "Scanning for fragile code patterns..."
    
    local fragile_count=0
    
    # Check for eval() usage
    if git diff HEAD~1 HEAD -- '*.py' | grep -E '^\+.*eval\(' | grep -v '#'; then
        add_audit_event "fragility_violation" "eval() usage detected" "warning"
        warning_message "eval() usage detected - potential security risk"
        ((fragile_count++))
    fi
    
    # Check for bare except clauses
    if git diff HEAD~1 HEAD -- '*.py' | grep -E '^\+.*except:$'; then
        add_audit_event "fragility_violation" "Bare except clause detected" "warning"
        warning_message "Bare except clauses reduce debuggability"
        ((fragile_count++))
    fi
    
    # Check for TODO/FIXME comments (incomplete code)
    if git diff HEAD~1 HEAD | grep -E '^\+.*(TODO|FIXME|HACK|XXX)' | head -5; then
        add_audit_event "code_maturity" "Incomplete code markers found" "warning"
        warning_message "Code contains TODO/FIXME markers - ensure completeness"
    fi
    
    if [ $fragile_count -eq 0 ]; then
        add_audit_event "fragility_check" "No fragile code patterns detected" "success"
        log_message "✓ Fragility check passed"
    fi
}

# Verify traceability
verify_traceability() {
    log_message "Verifying traceability and audit trail requirements..."
    
    # Check for logging in critical operations
    if git diff HEAD~1 HEAD -- 'src/**/*payment*' 'src/**/*transaction*' | grep -c 'log\|audit\|trace'; then
        add_audit_event "traceability_check" "Audit trail logging present in critical operations" "success"
        log_message "✓ Traceability verified"
    else
        add_audit_event "traceability_check" "Critical operations may lack audit trail" "warning"
        warning_message "Verify audit trail logging in financial operations"
    fi
}

# Generate compliance summary
generate_compliance_summary() {
    log_message "Generating compliance summary..."
    
    local event_count=$(jq '.events | length' "$FULL_LOG_PATH")
    local success_count=$(jq '[.events[] | select(.status=="success")] | length' "$FULL_LOG_PATH")
    local warning_count=$(jq '[.events[] | select(.status=="warning")] | length' "$FULL_LOG_PATH")
    local critical_count=$(jq '[.events[] | select(.status=="critical")] | length' "$FULL_LOG_PATH")
    
    # Add summary to log
    jq ".summary = {\"total_events\": $event_count, \"successful\": $success_count, \"warnings\": $warning_count, \"critical\": $critical_count}" "$FULL_LOG_PATH" > "${FULL_LOG_PATH}.tmp"
    mv "${FULL_LOG_PATH}.tmp" "$FULL_LOG_PATH"
    
    log_message "═══════════════════════════════════════════════════════"
    log_message "AUDIT LOG SUMMARY"
    log_message "───────────────────────────────────────────────────────"
    log_message "Total Events: $event_count"
    log_message "Successful Checks: $success_count"
    log_message "Warnings: $warning_count"
    log_message "Critical Issues: $critical_count"
    log_message "═══════════════════════════════════════════════════════"
    
    if [ "$critical_count" -gt 0 ]; then
        error_message "Critical compliance violations detected!"
        return 1
    fi
}

# Main execution
main() {
    log_message "Starting Vibe Solutioning Audit Trail Generation"
    log_message "Repository: $REPO | Branch: $BRANCH | Commit: $COMMIT_SHA"
    
    initialize_audit_log
    add_audit_event "workflow_start" "Audit trail generation started" "success"
    
    # Run all audit checks
    scan_code_quality || true
    scan_fragility || true
    verify_traceability || true
    generate_compliance_summary || {
        add_audit_event "workflow_end" "Audit trail generation completed with critical issues" "critical"
        error_message "Audit failed - critical compliance violations detected"
        exit 1
    }
    
    add_audit_event "workflow_end" "Audit trail generation completed successfully" "success"
    
    # Verify the file was created
    if [ -f "$FULL_LOG_PATH" ]; then
        log_message "✓ Audit log successfully created: $FULL_LOG_PATH"
        log_message "✓ File size: $(wc -c < "$FULL_LOG_PATH") bytes"
        
        # Print final audit log
        log_message "Final audit log (pretty-printed):"
        jq '.' "$FULL_LOG_PATH"
    else
        error_message "Failed to create audit log"
        exit 1
    fi
}

# Run main function
main "$@"
