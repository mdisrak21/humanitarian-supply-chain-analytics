# 📦 Humanitarian Supply Chain & Aid Distribution Analytics

An interactive humanitarian supply chain and aid distribution analytics dashboard built with Python and Streamlit.

## 🚀 Live Demo

👉 https://humanitarian-supply-chain-analytics.streamlit.app/

## 📸 Dashboard Preview

![Humanitarian Supply Chain & Aid Distribution Analytics](dashboard.PNG)

## 📌 Project Overview

This project is a humanitarian supply chain and aid distribution analytics dashboard designed to support data-driven decision-making in humanitarian logistics and relief operations.

The system allows users to monitor humanitarian aid inventory, track shipments, identify supply gaps, monitor distribution activities, analyze beneficiary reach, and generate operational reports.

The project uses synthetic data for educational and portfolio purposes.

## 🎯 Objectives

- Monitor humanitarian aid inventory across warehouses
- Identify low-stock and potential supply-gap items
- Track humanitarian shipments and delivery status
- Monitor aid distribution across different districts
- Track households and beneficiaries reached
- Analyze district-level distribution performance
- Generate downloadable operational reports
- Demonstrate humanitarian logistics data analysis and visualization

## 📊 Key Features

### 📦 Inventory Management

- Add and manage humanitarian aid inventory
- Monitor warehouse-level stock
- Define minimum stock thresholds
- Identify low-stock items
- Calculate supply gaps
- Analyze inventory by aid category

### 🚚 Shipment Tracking

- Add new shipment records
- Track shipment origin and destination
- Record dispatch and expected delivery dates
- Monitor shipment status
- Identify delivered and active shipments
- Filter shipments by status

### 📍 Distribution Monitoring

- Add humanitarian distribution records
- Monitor distribution centers
- Track district-level aid distribution
- Record households reached
- Record beneficiaries reached
- Analyze distributed quantities

### ⚠️ Supply Gap Analysis

- Automatically identify items below minimum stock
- Calculate stock gaps
- Highlight potential humanitarian supply shortages
- Support operational replenishment decisions

### 📑 Reporting

- Generate inventory reports
- Generate shipment reports
- Generate distribution reports
- Generate district-level performance reports
- Download reports as CSV files

## 🛠️ Technologies Used

- Python
- Streamlit
- Pandas
- Plotly
- SQLite
- Git & GitHub

## 🗄️ Database

The application uses SQLite for local data storage.

Main database entities:

`aid_inventory`

`shipments`

`distributions`

The database stores:

### Aid Inventory

- Item name
- Aid category
- Warehouse
- Quantity
- Minimum stock level
- Unit
- Updated date

### Shipments

- Shipment code
- Item name
- Origin
- Destination
- Quantity
- Dispatch date
- Expected delivery date
- Shipment status

### Distributions

- Distribution date
- District
- Distribution center
- Item name
- Distributed quantity
- Households reached
- Beneficiaries reached

## 🔄 Data Workflow

```text
Aid Inventory
       ↓
SQLite Database
       ↓
Shipment Tracking
       ↓
Data Processing with Pandas
       ↓
Supply Gap Analysis
       ↓
Distribution Monitoring
       ↓
Beneficiary Reach Analysis
       ↓
Interactive Dashboard
       ↓
Reports & CSV Export

```

## ⚙️ Installation & Usage

```bash
git clone https://github.com/mdisrak21/humanitarian-supply-chain-analytics.git
cd humanitarian-supply-chain-analytics
pip install -r requirements.txt
streamlit run app.py
```

## 🔮 Future Improvements

- Add route optimization.
- Add stock-out alerts.
- Add geographic supply chain maps.
- Add delivery performance forecasting.
