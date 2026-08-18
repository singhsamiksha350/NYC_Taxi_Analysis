# 🚕 NYC Taxi Demand & Trip Analysis Dashboard

Analyzed 200,000 NYC taxi trips using Python and Tableau to identify temporal demand patterns, high-demand pickup zones, trip-distance and duration distributions, travel-speed variations, payment and tipping behavior, and borough-level trip flows. Developed an interactive dashboard combining nine complementary visualizations.

---

## 1. Project Overview

This project explores **NYC Yellow Taxi trip data** to answer questions across three themes:

- 🚕 **Demand** — when and where taxi demand is highest
- 🚦 **Efficiency** — how trip distance, duration, and speed vary
- 💰 **Behavior** — how passengers pay, tip, and move between boroughs

The goal was to go beyond single charts and build a cohesive, interactive dashboard that tells a full operational story — the kind of demand/efficiency/behavior analysis relevant to any transportation or logistics business.

---

## 2. Dataset

- **Source:** [NYC TLC Yellow Taxi Trip Record Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)
- **Period used:** January 2024
- **Full dataset:** ~38.3 million rows, 19 columns
- **Sample used:** 200,000 randomly sampled trips (`random_state=42` for reproducibility), to keep the dataset manageable for Tableau Public while preserving the underlying patterns.
- **Supporting data:** [NYC Taxi Zone Lookup Table](https://www.nyc.gov/assets/tlc/downloads/csv/taxi_zone_lookup.csv) — maps `LocationID` to `Borough` and `Zone` names. Joined twice (once for pickup, once for dropoff) to enable borough-level flow analysis.

---

## 3. Data Preparation with Python

Using `pandas`, the full January 2024 Parquet file was downloaded directly from NYC TLC's CloudFront-hosted source, then randomly sampled down to 200,000 trips and exported to CSV for use in Tableau.

See [`python/data_sampling.py`](python/data_sampling.py).

```python
import pandas as pd

url = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-01.parquet"
df = pd.read_parquet(url)

df_sample = df.sample(n=200000, random_state=42)
df_sample.to_csv("taxi_sample.csv", index=False)
```

---

## 4. Individual Visualizations

### 📊 Chart 1 — Trips by Hour
**Question:** When during the day is taxi demand highest?
Counts trips by pickup hour to reveal daily demand rhythm — low-demand hours, daytime activity, and evening peaks.

![Trips by Hour](screenshots/01_trips_by_hour.png)

---

### 📍 Chart 2 — Top 20 Pickup Zones
**Question:** Where do the most taxi trips begin?
Ranks NYC taxi zones by pickup volume, highlighting the areas with the most concentrated demand — useful for understanding where vehicles are most needed.

![Top 20 Pickup Zones](screenshots/02_top_20_pickup_zones.png)

---

### 📏 Chart 3 — Trip Distance Distribution
**Question:** How far are taxi passengers typically traveling?
Bins trips by distance to show that most trips are short-to-medium distance. A calculated field (`Valid Trip Distance`, capped at 30 miles) prevents extreme outliers from distorting the chart.

![Trip Distance Distribution](screenshots/03_trip_distance_distribution.png)

---

### 🔥 Chart 4 — Trips by Hour & Day
**Question:** When exactly during the week is demand highest?
A heatmap (weekday × hour, colored by trip count) reveals recurring peak windows — e.g., distinguishing "Friday is busy" from "Friday evening specifically is busy." One of the strongest charts in the dashboard for demand planning.

![Trips by Hour & Day](screenshots/04_trips_by_hour_day.png)

---

### 🚦 Chart 5 — Average Speed by Hour
**Question:** How does taxi travel speed change throughout the day?
A calculated field derives average speed (trip distance ÷ trip duration), averaged by pickup hour, to surface congestion and traffic patterns across the day.

![Average Speed by Hour](screenshots/05_average_speed_by_hour.png)

---

### ⏱️ Chart 6 — Trip Duration Distribution
**Question:** How long do taxi trips normally last?
Trip duration (calculated via `DATEDIFF` on pickup/dropoff timestamps) is grouped into 5-minute bins, showing that short trips dominate the dataset.

![Trip Duration Distribution](screenshots/06_trip_duration_distribution.png)

---

### 💳 Chart 7 — Payment Type Breakdown
**Question:** How are passengers paying for their trips?
Compares trip volume across payment methods (per NYC TLC's coding: `1` = Credit card, `2` = Cash, `3` = No charge, `4` = Dispute) to understand passenger payment preferences. Credit card is the dominant method by a wide margin.

![Payment Type Breakdown](screenshots/07_payment_type_breakdown.png)

---

### 💰 Chart 8 — Tip % by Hour
**Question:** Does tipping behavior vary throughout the day?
Calculates tip percentage (tip amount ÷ fare amount) by hour rather than raw tip totals, giving a fairer view of tipping behavior relative to fare size.

![Tip % by Hour](screenshots/08_tip_percentage_by_hour.png)

---

### 🗺️ Chart 9 — Dropoff Borough Flow
**Question:** How do passengers move between NYC boroughs?
Using two joined copies of the taxi zone lookup table (one for pickup, one for dropoff), this matrix/heatmap visualizes trip volume between every pickup–dropoff borough pair. The dashboard reveals a particularly large **Manhattan → Manhattan** flow.

![Dropoff Borough Flow](screenshots/09_dropoff_borough_flow.png)

---

## 5. Final Dashboard

All nine visualizations were combined into a single interactive Tableau dashboard, organized into three sections:

| Demand | Trip Efficiency | Customer / Revenue Behavior |
|---|---|---|
| Trips by Hour | Trip Distance Distribution | Payment Type Breakdown |
| Top 20 Pickup Zones | Average Speed by Hour | Tip % by Hour |
| Trips by Hour & Day | Trip Duration Distribution | Dropoff Borough Flow |

![Full Dashboard](screenshots/dashboard.png)
---

## 6. Key Findings

- **Demand follows a clear commuter pattern.** Trips bottom out around **4 AM** (~1K trips) and climb steadily to a peak between **5–6 PM** (~14K trips), with a secondary plateau around midday (12–1 PM, ~13K trips). This double-hump shape is consistent with morning build-up and an evening rush-hour peak.
- **JFK Airport is the single busiest pickup zone**, ahead of Midtown Center and the Upper East Side — a reminder that airport transfers are a major, steady demand driver alongside core Manhattan business districts.
- **The vast majority of trips are short-distance.** Over 65K trips fall in the 0–1 mile bin alone, with volume dropping off sharply past ~5 miles — most taxi trips are short intra-Manhattan hops, not long cross-borough journeys.
- **Trip duration mirrors distance**: the majority of trips last under 20 minutes, with volume dropping off sharply after the 20–30 minute bin — reinforcing that most rides are quick, short-range trips rather than long hauls.
- **Average speed spikes sharply around 11 AM** (~41 mph vs. a baseline of 10–15 mph the rest of the day). Given that midday hours are typically *more* congested, not less, this is most likely a data artifact (e.g., a small number of low-duration/high-distance outlier trips skewing the hourly average) rather than a genuine traffic pattern — worth noting as a data-quality observation rather than a real efficiency signal.
- **Credit card is by far the dominant payment method** (payment type `1`), used in roughly 5x more trips than cash (type `2`), with "no charge" and "dispute" trips being rare edge cases.
- **Tipping behavior tracks demand, not just fare size.** Tip percentage is lowest overnight (~14% around 4–5 AM) and rises through the day to peak in the early evening (~20% around 6 PM) — riders tip more generously during peak commute hours.

- **Manhattan dominates overall trip volume by a huge margin** — 178,626 of the 200,000 sampled trips have a Manhattan dropoff, vs. under 20K for Queens and under 2K each for the Bronx, Brooklyn, and Staten Island. *(Note: as currently built, this matrix only populates same-borough diagonal cells — e.g., Manhattan→Manhattan, Brooklyn→Brooklyn — rather than true cross-borough pairs like Bronx→Manhattan. This likely points to a join issue between the two pickup/dropoff zone lookups and is worth revisiting; as-is, it's more accurately described as a dropoff-borough volume breakdown than a full flow analysis.)*

---

## 7. Tools Used

- **Python (pandas)** — downloading, sampling, and exporting the raw dataset
- **Tableau** — data connection, joins, calculated fields, binning, filtering, aggregation, and dashboard design
- **Dataset:** NYC TLC Yellow Taxi Trip Record Data + NYC Taxi Zone Lookup Table

---

## 8. How to Reproduce

1. Clone this repo
2. Run `python/data_sampling.py` to regenerate `taxi_sample.csv`
3. Open `tableau/NYC_Taxi_Dashboard.twbx` in [Tableau Public](https://public.tableau.com/) (free)
4. The workbook is pre-connected to `data/taxi_sample.csv` and `data/taxi_zone_lookup.csv`

---

## Repository Structure

```
NYC-Taxi-Data-Analysis/
│
├── README.md
├── data/
│   ├── taxi_sample.csv
│   └── taxi_zone_lookup.csv
├── python/
│   └── data_sampling.py
├── tableau/
│   └── NYC_Taxi_Dashboard.twbx
└── screenshots/
    ├── 01_trips_by_hour.png
    ├── 02_top_20_pickup_zones.png
    ├── 03_trip_distance_distribution.png
    ├── 04_trips_by_hour_day.png
    ├── 05_average_speed_by_hour.png
    ├── 06_trip_duration_distribution.png
    ├── 07_payment_type_breakdown.png
    ├── 08_tip_percentage_by_hour.png
    ├── 09_dropoff_borough_flow.png
    └── dashboard.png
```
