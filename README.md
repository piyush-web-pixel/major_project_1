# AutoInsight — Automated Data Analysis & Business Intelligence Platform

AutoInsight is an automated data analysis and business intelligence platform that allows users to upload CSV or Excel datasets and automatically generates data profiling, column detection, data cleaning reports, statistical analysis, business KPIs, interactive visualizations, and data-driven insights.

The platform is designed to reduce the manual effort required for initial data analysis and help users quickly understand their datasets.

---

## 🚀 Live Demo

### Frontend
https://major-project-1-2-ok7u.onrender.com

### Backend API
https://major-project-1-1-diwh.onrender.com

---

## 📌 Project Overview

Data analysis usually requires several repetitive steps such as:

- Loading datasets
- Understanding dataset structure
- Detecting column types
- Handling missing values
- Identifying outliers
- Performing statistical analysis
- Finding correlations
- Creating visualizations
- Generating business insights

AutoInsight automates these initial analytical steps through a modular data processing pipeline.

Users simply upload a CSV or Excel file and AutoInsight processes the dataset automatically.

---

## ✨ Features

### 📂 Dataset Upload

Supports:

- CSV
- XLSX
- XLS

Users can upload datasets directly from the web interface.

---

### 🔍 Automatic Dataset Profiling

AutoInsight automatically analyzes:

- Number of rows
- Number of columns
- Missing values
- Duplicate records
- Data types
- Dataset structure
- Basic dataset statistics

---

### 🧠 Automatic Column Detection

The system detects different column roles automatically, including:

- Numeric
- Categorical
- Binary
- Date
- Identifier

Each detected column also receives a confidence score.

Example:

```text
Date              → Date          → 100%
Store ID          → Identifier    → 98%
Category          → Categorical   → 95%
Inventory Level   → Numeric       → 95%
Promotion         → Binary        → 95%
