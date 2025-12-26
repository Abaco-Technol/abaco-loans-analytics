# Data Governance Policy

## Golden Rule

**Markdown files document HOW to get data, not WHAT the data is.**

- `.md` files describe **processes and procedures**
- `.md` files do NOT contain **static metrics or targets**
- Live data belongs in databases, dashboards, and queries—not documentation

---

## Source of Truth Hierarchy

### 1. Live Database (Highest Authority)
- `fact_loans`, `fact_cash_flows`, `fact_payments`
- `kpi_timeseries_daily` for operational metrics
- Always query for current values

### 2. Configuration Files
- `config/pipeline.yml` - Data pipeline settings
- `config/kpis.yml` - KPI definitions
- These are machine-readable and versioned

### 3. Documentation (Lowest Authority)
- Process guides and how-to instructions
- Strategic planning targets (clearly labeled)
- Historical references and archives

---

## File Organization Standards

### `/docs/` - Operational Documentation
- Process guides
- How-to instructions
- Technical runbooks
- Definitions and formulas

**CONTENT RULES:**
- ✅ "To calculate AUM, query: `SELECT SUM(...)`"
- ✅ "NPL = defaults / total_loans"
- ❌ "Current AUM is $7.4M"
- ❌ "We have 56 active customers"

### `/docs/planning/` - Strategic Planning Documents
- 2025, 2026, and future yearly targets
- OKRs and strategic objectives
- Forecasts and growth plans

**CONTENT RULES:**
- Must have `⚠️ PLANNING DOCUMENT` header at top
- ✅ "2026 TARGET AUM: $16.3M"
- ✅ "Goal: Reach 500 active clients by Q4 2026"
- ❌ "Current AUM: $7.4M" (remove "current")

### `/archives/` - Historical Snapshots
- Past extraction processes and data samples
- Compliance validation reports
- Production readiness snapshots
- Dated clearly: `YYYY-MM-DD_description.md`

**CONTENT RULES:**
- Use consistent date format: `2025-12-04`
- Organize by category: `/extractions/`, `/compliance/`, `/production_readiness/`
- Include timestamp when snapshot was taken
- Mark as historical reference only

---

## Static Data Detection & Prevention

### What NOT to Put in `.md` Files

**Hard-Coded Metrics:**
```
❌ "Current AUM: $7.4M"
❌ "Active customers: 56"
❌ "NPL rate: 3.2%"
❌ "Default rate last month: 2.8%"
```

**Unqualified Targets:**
```
❌ "AUM target: $16.3M" (unclear if planning or current)
❌ "Goal: 200 new customers"
```

**Static Date References:**
```
❌ "As of December 2025, we have..."
❌ "Last week's metrics showed..."
```

### What IS Okay

**Formulas & Calculations:**
```
✅ "To calculate NPL: defaults / total_loans × 100%"
✅ "SELECT SUM(outstanding_principal) FROM fact_loans WHERE status='active'"
```

**Clearly Labeled Targets:**
```
✅ "2026 TARGET AUM: $16.3M"
✅ "PLAN: Reach 500 active clients by 2026-Q4"
✅ "GOAL: Achieve 99.5% SLO for decision SLA"
```

**Document Metadata:**
```
✅ "Last Updated: 2025-12-26"
✅ "Next Review: 2026-Q1"
✅ "Status: PLANNING TARGETS - NOT ACTUALS"
```

---

## Enforcement Mechanisms

### Pre-Commit Hook (Local)
```bash
# Check for currency amounts in docs
if grep -rE --exclude-dir=planning '\$[0-9]+\.?[0-9]*[MK]?' docs/ | grep -v "TARGET\|GOAL\|PLAN\|QUERY"; then
  echo "ERROR: Static dollar amounts found in docs"
  exit 1
fi

# Check for numeric customer counts
if grep -rE --exclude-dir=planning '[0-9]{2,} (active |customers|clients)' docs/ | grep -v "TARGET\|GOAL\|PLAN\|QUERY"; then
  echo "ERROR: Static customer counts found in docs"
  exit 1
fi
```

### Code Review Checklist
- [ ] Does this `.md` file contain static metrics (without TARGET/GOAL/PLAN label)?
- [ ] Are planning targets clearly marked with `⚠️ PLANNING DOCUMENT`?
- [ ] Are dates clearly marked as document timestamps?
- [ ] Could this metric be queried from live data instead?
- [ ] Is this file in the correct directory (docs/, docs/planning/, or archives/)?

### CI/CD Validation
```yaml
name: Check for static metrics in docs
on: pull_request

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Check for unqualified metrics
        run: |
          if grep -rE --exclude-dir=planning '\$[0-9]+\.?[0-9]*[MK]?' docs/ | grep -v "TARGET\|GOAL\|PLAN\|QUERY"; then
            echo "ERROR: Static dollar amounts found in docs (without TARGET/GOAL label)"
            exit 1
          fi
```

---

## Role-Based Responsibilities

### Data Engineering
- **Owns:** Live databases, KPI definitions
- **Responsibility:** Update `config/kpis.yml` when metrics change
- **Action:** Alert team when targets are met/missed in live data

### Product / Strategy
- **Owns:** Strategic planning documents
- **Responsibility:** Update `/docs/planning/` with annual OKRs
- **Action:** Mark all targets clearly as GOAL/PLAN/TARGET

### Operations
- **Owns:** Process documentation and runbooks
- **Responsibility:** Keep `/docs/` current with procedures (no metrics)
- **Action:** Link to live dashboards for current metrics, not copy them

### Compliance / Audit
- **Owns:** Historical snapshots and archives
- **Responsibility:** Organize and date compliance snapshots
- **Action:** Maintain `/archives/` with clear timestamps

---

## Migration Guide for Existing Static Data

If you find static metrics in `.md` files:

### Option 1: Move to Live Query
```markdown
OLD: "Current AUM: $7.4M"
NEW: "To check current AUM: SELECT SUM(outstanding_principal) FROM fact_loans WHERE status='active'"
```

### Option 2: Move to Planning Directory
```markdown
OLD: In /docs/README.md: "AUM target $16.3M"
NEW: In /docs/planning/2026/Strategic_Goals.md: "⚠️ 2026 TARGET AUM: $16.3M"
```

### Option 3: Archive as Historical
```markdown
OLD: In /docs/monthly-report.md: "December metrics..."
NEW: In /archives/reporting/2025-12-04_monthly_snapshot.md: "December 2025 snapshot..."
```

---

## FAQs

**Q: Can I put examples of metrics in documentation?**
A: Yes, but prefix with context: "Example calculation result: $7.4M" or use placeholder: "Example output: $X.XM"

**Q: What if a metric changes weekly, should it be in docs?**
A: No. Instead, document HOW to get it: "Query kpi_timeseries_daily table ordered by date DESC"

**Q: How do I document a strategic goal?**
A: Put it in `/docs/planning/YYYY/` with `⚠️ PLANNING DOCUMENT` header and TARGET prefix

**Q: Can I reference old metrics in discussion?**
A: Yes, if dated: "As of 2025-12-04 snapshot, AUM was $7.4M (see /archives/...)"

---

## Policy Approval & Review

- **Approved by:** Engineering Leadership
- **Effective Date:** 2025-12-26
- **Last Updated:** 2025-12-26
- **Next Review:** 2026-Q1 (Quarterly review cycle)
- **Related Issue:** [Documentation Audit - Static Data Cleanup](<actual-issue-url>)

---

For questions or violations, escalate to the Data Governance committee.
