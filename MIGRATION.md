# Migration Guide - Unified Pipeline v2.0

## 1. Overview
This document guides the transition from legacy, fragmented scripts to the enterprise-grade **Unified Pipeline** architecture. As of January 2026, the core engine consolidation (Phase 3) is 100% complete.

## 2. Structural Changes

| Component | Legacy Location | Unified Location (v2.0) |
|-----------|-----------------|------------------------|
| Ingestion | `python/ingest/` | `python/pipeline/data_ingestion.py` |
| Transformation | `python/analytics/transformation.py` | `python/pipeline/data_transformation.py` |
| KPI Engine | `python/kpi_engine.py` | `python/pipeline/kpi_calculation.py` |
| Orchestrator | `scripts/run_data_pipeline.py` | `python/pipeline/orchestrator.py` |
| Entry Point | Multiple scripts | `apps/analytics/run_report.py` |

## 3. Mandatory Cutover Actions

### Update Automated Tasks
All cron jobs or GitHub Actions calling `scripts/run_data_pipeline.py` or legacy ingestion scripts MUST be updated to use the new executive runner.

**Legacy Command:**
```bash
python python/ingestion.py --file loans.csv
python python/transformation.py --input raw.csv
```

**Unified Command:**
```bash
python apps/analytics/run_report.py --data data/raw/loans.csv --output reports/summary.md
```

### Configuration Migration
Legacy YAML configs in `config/LEGACY/` are no longer primary. All modifications should be made to:
- `config/pipeline.yml` (Global settings)
- `config/environments/` (Environment overrides)
- `config/kpis/kpi_definitions.yaml` (KPI formulas)

## 4. Verification & Validation

To ensure the migration was successful for your local or production environment, run:

1. **Bootstrap Check**: `python tools/zencoder_bootstrap.py`
2. **KPI Parity**: `make test-kpi-parity`
3. **Quality Audit**: `make audit-code`

## 5. Deletion Schedule
The following directories and files are marked for deletion in **Q1 2026**:
- `config/LEGACY/`
- `python/ingest/` (Legacy)
- `python/financial_analysis.py.bak`
- All scripts in `archives/refactoring/`

## 6. Rollback
If the Unified Pipeline fails due to unforeseen environmental issues:
1. Revert to the `main` branch or the `v1.5-legacy` tag.
2. Legacy code remains available in `archives/` for reference, but should not be used for production runs.

---
*Migration Lead: Zencoder Agent*
