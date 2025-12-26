# Cascade Data Extraction Process

## Purpose

This document describes **HOW** to extract data from Cascade Debt platform.  
It does **NOT** contain actual data values or extraction results.

## Prerequisites

- Cascade API credentials configured in GitHub secrets
- Python environment activated (Python 3.9+)
- Database connection verified
- Access to `CASCADE_TOKEN` via vault or secrets manager

## Extraction Steps

### 1. Authenticate

```bash
export CASCADE_TOKEN=$(vault read -field=token secret/cascade)
# Or from GitHub Secrets:
# CASCADE_TOKEN is injected automatically in workflows
```

### 2. Run Fresh Extraction

Download current data from Cascade platform:

```bash
python scripts/cascade_ingest.py --fresh --validate
```

Verify data quality:

```bash
python scripts/validate_cascade_data.py
```

### 3. Confirm Data Freshness

Check platform update status:

```bash
python scripts/check_cascade_freshness.py
```

Expected output shows last update timestamp and validation status.

## Validation Checks

The extraction process includes:
- Data completeness validation
- Schema conformance checks
- Foreign key integrity verification
- Duplicate detection
- Outlier flagging (if configured)

## Output Location

Extracted data is written to:
- Database tables: `staging_cascade_*` (temporary)
- Final tables: `fact_loans`, `fact_cash_flows` (after validation)
- Logs: `logs/cascade_ingest_YYYY-MM-DD.log`

## Troubleshooting

### Issue: Authentication fails

**Solution:**
1. Verify `CASCADE_TOKEN` is set: `echo $CASCADE_TOKEN`
2. Rotate token in Meta Business Manager
3. Update GitHub secret `CASCADE_API_KEY`
4. Re-run extraction

### Issue: Data validation errors

**Solution:**
1. Check error logs: `tail -f logs/cascade_ingest_*.log`
2. Review schema expectations in `CASCADE_DATA_SOURCES.md`
3. Verify platform endpoint changes
4. Contact Cascade support if schema changed

### Issue: Extraction times out

**Solution:**
1. Check network connectivity
2. Reduce batch size in `scripts/cascade_ingest.py`
3. Run during off-peak hours (off-business hours in Mexico)
4. Check Cascade platform status

## Historical References

For past extraction examples and snapshots:
- See: `/archives/extractions/YYYY-MM-DD/`

**IMPORTANT:** Always use fresh data for production workflows.  
Historical extractions are reference only.

## Schedule

- **Daily extractions:** 02:00 UTC (off-business hours in Mexico)
- **Weekly validation:** Mondays at 06:00 UTC
- **Monthly reconciliation:** First Monday of month at 10:00 UTC

## Related Documentation

- [Cascade Data Sources](CASCADE_DATA_SOURCES.md)
- [Data Pipeline Validation](../archived/pipeline_validation.md)
- [Extraction Troubleshooting](../runbooks/cascade_extraction_troubleshooting.md)

---

**Last Updated:** 2025-12-26  
**Next Review:** 2026-01-15  
**Owner:** Data Engineering
