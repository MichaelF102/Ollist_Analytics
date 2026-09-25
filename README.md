# ⚡ Olist Brazilian E-Commerce &bull; Executive Analytics Platform

A professional, 5-page **Streamlit Business Intelligence & Decision Support Platform** translating static Power BI reports into dynamic, insight-driven analytical telemetry.

Powered by actual transaction data across **99,441 orders**, **112,650 order items**, and **96,096 unique customers**, this application marries modern SaaS aesthetics with an automated **4-Layer Insight Engine** underneath every visual.

---

## 👥 Project Team & Equal Work Distribution (50% - 50%)

This project was conceived, designed, and engineered through an equal partnership between two members across both **Power BI report authoring** and **Streamlit full-stack implementation**:

| Team Member | Roll No & Student ID | Core Modules Owned | Key Responsibilities |
| :--- | :--- | :--- | :--- |
| **Michael Fernandes** | **Roll No: 06**<br>ID: `2509006` | • **Page 1:** Executive Overview (Sales & Revenue)<br>• **Page 2:** Customers, Products & Geography | • Power BI Page 1 & Page 2 DAX measures and visuals<br>• Core Streamlit architecture & fast Parquet caching pipeline<br>• Custom modern dark SaaS design system (`style.css`)<br>• Sales & Customer analytics engines (`sales.py`, `customers.py`)<br>• Global multi-criteria sidebar filter system |
| **Nisarg Shah** | **Roll No: 05**<br>ID: `2509005` | • **Page 3:** Delivery Performance & Logistics Analytics<br>• **Page 4:** Customer Experience & Reviews | • Power BI Page 3 & Page 4 DAX delivery & review measures<br>• Streamlit Delivery & Reviews engines (`delivery.py`, `reviews.py`)<br>• Interactive Plotly Sankey diagram (Buyer &rarr; Seller &rarr; Outcome)<br>• Carrier handoff 2D latency heatmap & Seller SLA scatter plot<br>• Hero Visual: Ratings collapse combo chart & root cause diagnostic<br>• Reusable 4-layer automated Insight Engine (`insights.py`) |

---

## 🏛️ Application Architecture & Page Breakdown

```text
Ollist-Brazil_Visualization/
├── app.py                                # Main Portal Landing Page & Navigation Router
├── pages/
│   ├── 01_Executive_Overview.py          # Page 1: Business Performance & Sales Trends
│   ├── 02_Customer_Product_Intelligence.py # Page 2: Customers, Products & Geography
│   ├── 03_Delivery_Analytics.py          # Page 3: Delivery Performance & Logistics
│   ├── 04_Customer_Experience.py         # Page 4: Customer Experience & Reviews
│   └── 05_Work_Distribution.py           # Page 5: Work Distribution & Team Contributions
├── components/
│   ├── header.py                         # Top breadcrumbs, live model status & filter pills
│   ├── sidebar.py                        # Global filters (Year, Quarter, Region, State, Category, Status)
│   ├── kpi_cards.py                      # Custom HTML/CSS KPI cards with color accents
│   ├── charts.py                         # Plotly charts styled with dark modern SaaS BI theme
│   ├── insight_cards.py                  # 4-Layer Insight Cards & Executive Callout Banners
│   └── tables.py                         # Formatted category tables with summary totals
├── analytics/
│   ├── data_loader.py                    # Cached Parquet data loader with global filter engine
│   ├── sales.py                          # Sales, orders, AOV & revenue calculations
│   ├── customers.py                      # Customer counts, repeat purchasing & frequency
│   ├── products.py                       # Category volumes, crosstabs & regional demand
│   ├── delivery.py                       # Transit times, days late, seller SLAs & Sankey flows
│   ├── reviews.py                        # Customer satisfaction, delay buckets & root cause
│   └── insights.py                       # Deterministic 4-layer Insight Engine
├── assets/
│   ├── style.css                         # Custom dark BI design system (Glassmorphism & typography)
│   └── brazil_geo.json                   # Local, offline Brazil states GeoJSON for choropleth maps
├── data/
│   ├── raw/                              # Original Olist Brazilian E-Commerce CSVs
│   └── processed/                        # High-speed Parquet caches (orders, items, payments)
├── requirements.txt                      # Python dependencies
├── .gitignore                            # Version control exclusions
└── README.md                             # Project documentation
```

---

## 📊 Analytical Pages Summary

### 00. Main Portal (`app.py`)
* High-level executive KPIs (Gross Revenue: R$ 16.01M, Total Orders: 99.4K, Unique Buyers: 96.1K, On-Time Delivery: 93.2%, Avg Review: 4.09 ⭐).
* Interactive module portal cards linking to all analytical pages.
* Overview of technology stack, data pipeline, and team ownership.

### 01. Executive Overview & Business Performance
* **Question:** *"How is the business performing across sales, orders, and customer acquisition?"*
* **KPIs:** Total Orders (99K), Total Revenue (R$ 16.01M), Unique Customers (96K), Average Order Value (R$ 160.99), Products Sold (113K).
* **Visuals:** Dual-axis monthly order & revenue growth curve, day-of-week purchasing pattern (peaking Monday-Wednesday), payment instrument concentration (Credit Card 78.3%), top 10 states by revenue (led by SP), and non-delivered order status breakdown.

### 02. Customer & Product Intelligence
* **Question:** *"Who buys, what sells, and where are customers concentrated?"*
* **KPIs:** Unique Customers (96K), Repeat Customers (3K), Repeat Customer Rate (~3.1%), Unique Products (33K), Categories (73), Products Sold (113K).
* **Visuals:** Brazil state customer density map, top 10 cities ranking, category regional share matrix heatmap across 5 macro-regions, top product categories, order frequency histogram (exposing the ~3.1% repeat customer bottleneck), and category performance table.

### 03. Delivery Performance & Logistics Analytics
* **Question:** *"Where are delivery problems occurring and how efficiently are orders fulfilled?"*
* **KPIs:** Avg Delivery Time (12.56 days), Avg Days Late (10.6 days), Late Delivery % (6.8%), On-Time Delivery % (93.2%), Total Delivered Orders.
* **Visuals:** Seller volume vs on-time SLA scatter plot with 85% reference line, 2D carrier handoff latency heatmap, state on-time delivery rate choropleth map, and inter-regional Sankey diagram (Buyer Region &rarr; Seller Region &rarr; Delivery Outcome) with route corridor insights.

### 04. Customer Experience & Reviews
* **Question:** *"How does logistics fulfillment directly shape customer satisfaction?"*
* **KPIs:** Average Review Score (4.09), Low Rating Rate (14.7%), On-Time Rating (4.29), Late Order Rating (2.32), Severe Delay Rating (1.71).
* **Hero Visual:** The **2.59-point Sentiment Cliff** combo chart (review score falling from 4.29 to 1.70 as delays exceed 8+ days while low ratings surge to 79.0%).
* **Visuals:** Product sales vs review score treemap, interactive multi-dimensional root-cause diagnostic selector (by Delay Bucket, Customer Region, Seller Region, State, Category), and monthly time series combo tracking operational deterioration vs customer review sentiment.

### 05. Work Distribution & Team Contributions
* Detailed breakdown of deliverables, technical ownership, and equal 50%-50% contribution balance between Michael Fernandes and Nisarg Shah.

---

## 💡 The 4-Layer Insight Engine

Unlike conventional dashboards that only display charts, every visual is accompanied by an automated, structured insight card:
1. **Finding:** The observed empirical pattern from the chart.
2. **Evidence:** Exact computed numbers, shares, and ratios from the dataset.
3. **Business Interpretation:** Strategic meaning without making unsupported causal claims.
4. **Operational Implication:** Direct operational takeaways for logistics, merchandising, or customer retention.

---

## 🚀 Installation & Local Setup

### 1. Clone or Open the Repository
```bash
git clone <repository_url>
cd Ollist-Brazil_Visualization
```

### 2. Set Up a Virtual Environment (Recommended)
```bash
# Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit Application
```bash
streamlit run app.py
```
*The application will automatically pre-cache datasets to Parquet on first launch and open in your default browser at `http://localhost:8501`.*

---

## 🛠️ Technology Stack
* **Frontend & Interactivity:** [Streamlit](https://streamlit.io/) (Multi-page app with `st.navigation`, reactive filters, custom CSS)
* **Data Processing & Analytics:** [Pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/), [PyArrow](https://arrow.apache.org/docs/python/)
* **Visualizations:** [Plotly Graph Objects](https://plotly.com/python/) & [Plotly Express](https://plotly.com/python/plotly-express/)
* **Cartography:** Plotly Choropleth with offline GeoJSON for all 27 Brazilian states (UF)
* **BI Reference:** Microsoft Power BI
