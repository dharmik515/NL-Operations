# NL Operations — Model Architecture

## Overview
Streamlit automation tool that replaces manual daily Excel operations for a recommerce company trading smartphones worldwide. Takes 3 daily upload files and produces a formatted master template plus analytics dashboards.

**Primary file:** [ui/master_template_app.py](ui/master_template_app.py)

**Run:** `streamlit run ui/master_template_app.py`

**Tech stack:** Python 3.9, Streamlit 1.29, Pandas, OpenPyXL, Plotly

---

## Inputs (uploaded daily)

| File | Format | Sheet | Key columns |
|------|--------|-------|-------------|
| Hanger Stocktake | .xlsm | Sheet1 | Room, Hangar, LOA, IMEI, Deal ID, BACKEND |
| Totes Stocktake | .xlsm | Sheet1 | Room, Hangar, LOA, IMEI, Deal ID, BACKEND |
| Stack Bulk Upload | .xlsx | BulkSell | 29 cols incl. Appraisal, Brand, Asset Label, Sell Grade, Appraisal VATType, Appraisal Status, Storage Member Country |

## Output
16-column formatted Excel master template (`StockTake Template` sheet):

`Room, Bin, Location, IMEI, Deal Id, Category, Brand, Model, Grade, VAT Type, Status, Stack, Country, PP, Conversion, PP in AED`

> PP (Purchase Price) from eWallet is deferred.

---

## Data Flow

```
Upload files
    ↓
process_hanger / process_totes  → cleaned stocktake dataframes
    ↓
build_lookup(stack_df)          → Appraisal-keyed dict
    ↓
build_master_template(...)      → joined master dataframe
    ↓
export_excel(df)                → formatted .xlsx
    ↓
Download + analytics / diagnostics dashboards
```

---

## Key Functions

### Ingestion & cleaning
- **`is_low_value_file(file)`** — detects low-value file variant.
- **`read_stack_bulk(file)`** — 4-method repair cascade for corrupted files (openpyxl → data_only → strip validation → xlrd).
- **`process_hanger(file)`**
  - Filters rows where `Room` is not null.
  - AE filter: `Deal ID → BACKEND → 'No deal ID'`.
  - Location merge: `Hangar (int) + LOA (letter)` → e.g. `61A`.
  - IMEI clean: float → int → string (prevents scientific notation).
- **`process_totes(file)`** — same as hanger, but `Location = LOA` only and `Bin = 'Totes'`.
- **`build_low_value_template(lv_file)`** — low-value template builder.

### Joining
- **`build_lookup(stack_df)`** — dict keyed on Appraisal code → `{Category, Brand, Model, Grade, VAT Type, Status, Stack, Country}`.
- **`build_master_template(hanger_df, lookup)`** — joins stocktake data with stack bulk via `Deal Id`.

### Export
- **`export_excel(df)`** — openpyxl formatting; IMEI column forced to text format (`@`) to prevent scientific notation.

### Helpers
- **`_is_real_device(imei_val)`** — returns `False` if IMEI is `''`, `'nan'`, `'0'`, `'none'`, `'empty pocket'`. Used to exclude physical empty pockets from the occupied set and device lookup.
- **`_clean_imei(val)`** / **`_norm_imei(val)`** — float → int → string normalization. Critical because hanger_raw stores IMEIs as floats (`355352083374666.0`) while master_df stores them as strings.

### Dashboards
- **`show_analytics(hanger_file, totes_file, master_df)`** — full analytics dashboard.
- **`show_diagnostics(hanger_file, totes_file, master_df)`** — smart diagnostics dashboard.
- **`show_daily_delta(hanger_file, totes_file)`** — day-over-day delta view.
- **`show_stock_intelligence(stack_file)`** — stack bulk intelligence view.

---

## Critical Logic

**Empty pocket detection** — physical empty pockets (no real device) are excluded from the occupied set so they don't render as filled on the hanger map.

**IMEI normalization** — uniform float→int→string conversion across all sources prevents join failures between hanger_raw (floats) and master_df (strings).

**Occupied set** — built only from rows passing `_is_real_device`. Drives hanger map coloring.

---

## Session State Keys

| Key | Purpose |
|-----|---------|
| `show_analytics` | bool — toggles analytics panel |
| `show_diagnostics` | bool — toggles diagnostics panel |
| `master_df_result` | stores master_df after generation so dashboards can reuse it |
