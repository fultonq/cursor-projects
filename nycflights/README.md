# NYC Flights 2013 — Data Science Project

End-to-end analysis of the [nycflights13](https://github.com/tidyverse/nycflights13) tables (336,776 outbound flights from EWR, JFK, and LGA in 2013) using **pandas**, **numpy**, **seaborn**, and **scikit-learn**, with an interactive **Streamlit** dashboard.

## What this project does

| Stage | What you get |
| --- | --- |
| Load & profile | Five related tables, dtypes, cardinality, memory, missingness |
| Clean / NA | Cancelled vs diverted vs operated; weather and aircraft imputation with missingness flags |
| Dimensionality | Drop IDs/constants, correlation pruning, PCA, SelectKBest |
| EDA | Delay distributions, carrier/hour/origin views, weather, cancellations |
| ML | Predict departure delay, arrival delay, and P(delay ≥ 15 min) |
| Dashboard | Filterable Streamlit app for all of the above plus what-if predictions |

Delay models use a **temporal split** (train January–October, test November–December) so future schedules and weather cannot leak into training. Actual departure/arrival clock times and air time are **not** used as features for departure-delay models.

## Setup

```bash
cd nycflights
python -m pip install -r requirements.txt
```

## Pipeline

All commands are run from `nycflights/` so the package imports resolve:

```bash
export PYTHONPATH=.
python -m nycflights_ds download   # CSVs from Rdatasets (nycflights13)
python -m nycflights_ds profile    # shape, dtypes, NA, nunique
python -m nycflights_ds prepare    # joins, NA policy, features → parquet
python -m nycflights_ds eda        # seaborn figures → reports/figures
python -m nycflights_ds train      # sklearn pipelines → models/
```

`download` also writes `data/sample/` (a few thousand real rows) for tests and a lightweight dashboard mode.

Train on every January–October row (slower, slightly better):

```bash
python -m nycflights_ds train --full
```

## Streamlit

```bash
cd nycflights
PYTHONPATH=. streamlit run app/streamlit_app.py
```

Tabs: **Overview**, **Profile & NA**, **EDA**, **Dimensionality**, **Predict**, **Model lab**.

Use the sidebar to switch `raw` (full year) vs `sample`, and to filter origin, carrier, and month.

## Holdout results (Nov–Dec 2013)

Trained on a 50,000-row sample of January–October, evaluated on all November–December operated flights.

| Target | Model | Headline metric | vs mean baseline |
| --- | --- | --- | --- |
| Departure delay (min) | HistGradientBoosting | MAE 18.2, R² 0.06 | baseline MAE 20.4 |
| Arrival delay (min) | Ridge (uses dep. delay) | MAE 12.3, R² 0.84 | baseline MAE 25.0 |
| Delayed ≥ 15 min | Logistic (balanced) | ROC-AUC 0.71, recall 0.46 | prevalence 22% |

Departure delay is noisy from pre-departure features alone (weather, schedule, carrier, aircraft). Arrival delay is much more predictable once departure delay is known. The linear departure model does **not** beat a mean baseline on a later-year holdout — a useful reminder that November–December delay regimes differ from earlier months.

## Tests

```bash
cd nycflights
PYTHONPATH=. pytest tests -q
```

## Modeling notes

- **Targets:** `dep_delay` (minutes), `arr_delay` (minutes, includes observed/predicted `dep_delay`), `dep_delayed` (FAA 15-minute threshold).
- **Estimators:** `HistGradientBoosting*` (handles numeric NA, ordinal categoricals) and a Ridge / logistic baseline (`ColumnTransformer` + scale + one-hot + `TargetEncoder` for destination).
- **Joins:** `airlines` on `carrier`, `planes` on `tailnum`, origin/dest `airports`, hourly `weather` on origin + date + scheduled hour.

## Layout

```
nycflights/
  nycflights_ds/     # load, clean, features, dimensionality, eda, model
  app/streamlit_app.py
  tests/
  data/raw/          # gitignored full CSVs
  data/sample/       # committed subset
  models/            # joblib bundle after train
  reports/figures/   # seaborn exports after eda
```
