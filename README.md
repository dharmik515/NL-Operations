# NL Operations — Master Template Generator

Streamlit app that automates the daily master template build for the recommerce smartphone operations team. Upload the three daily Excel files (Hanger Stocktake, Totes Stocktake, Stack Bulk Upload) and get back a formatted 16-column master template plus analytics, diagnostics, daily delta, and stock-intelligence dashboards.

## Run locally

```bash
pip install -r requirements.txt
streamlit run ui/master_template_app.py
```

App opens at `http://localhost:8501`.

## Deploy to Streamlit Community Cloud (free public link)

1. Push this repo to GitHub (see below).
2. Go to <https://share.streamlit.io> and sign in with GitHub.
3. Click **New app**.
4. Select this repo, branch `main`, and set **Main file path** to:
   ```
   ui/master_template_app.py
   ```
5. Click **Deploy**. You'll get a public URL like `https://<your-app>.streamlit.app` to share with colleagues.

## Push to GitHub (first time)

After creating an empty repo on GitHub:

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/<your-username>/<repo-name>.git
git push -u origin main
```

## Inputs

| File | Format | Sheet | Key columns |
|------|--------|-------|-------------|
| Hanger Stocktake | .xlsm | Sheet1 | Room, Hangar, LOA, IMEI, Deal ID, BACKEND |
| Totes Stocktake | .xlsm | Sheet1 | Room, Hangar, LOA, IMEI, Deal ID, BACKEND |
| Stack Bulk Upload | .xlsx | BulkSell | Appraisal, Brand, Asset Label, Sell Grade, Appraisal VATType, Appraisal Status, Storage Member Country (29 cols total) |

## Output

16-column formatted master template (`StockTake Template` sheet):

`Room, Bin, Location, IMEI, Deal Id, Category, Brand, Model, Grade, VAT Type, Status, Stack, Country, PP, Conversion, PP in AED`

> PP (Purchase Price) from eWallet is currently deferred.

## Project structure

```
.
├── ui/
│   └── master_template_app.py    # Main Streamlit app
├── .streamlit/
│   └── config.toml               # Server / theme config
├── requirements.txt              # Python dependencies
├── read.md                       # Architecture notes
└── README.md
```

## Notes

- `.gitignore` excludes all `.xlsx` / `.xlsm` / `.csv` files — never commit production stocktake data. Place demo files under `sample_data/` if you want to share examples.
- Do not commit `.streamlit/secrets.toml` if you add one later (already in `.gitignore`).

## Tech stack

Python 3.9 · Streamlit 1.28+ · Pandas · OpenPyXL · Plotly
