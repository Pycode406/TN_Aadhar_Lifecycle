# Tamil Nadu Aadhaar Operational Analytics Dashboard

## Overview

The **Tamil Nadu Aadhaar Operational Analytics Dashboard** is an interactive analytics application built to analyze Aadhaar enrolment and update operations across Tamil Nadu. The dashboard provides visual insights into enrolment trends, update behavior, lifecycle compliance, and district-level operational stress indicators.

The application enables users to explore Aadhaar operational patterns through dynamic visualizations and key performance indicators (KPIs), helping to identify system pressure points and demographic update trends.

This dashboard is implemented using Python with Streamlit for interactive visualization and Plotly for analytical charts.

---

## Objectives

The dashboard aims to:

* Monitor Aadhaar enrolment patterns across age groups.
* Analyze biometric and demographic update trends.
* Identify operational pressure in districts.
* Evaluate compliance with Aadhaar child lifecycle updates.
* Detect volatility in demographic updates among adults.
* Provide an interactive platform for selecting different analytical charts.

---

## Features

### 1. KPI Summary

At the top of the dashboard, key operational metrics are displayed:

* Total Aadhaar Enrolments
* Total Biometric Updates
* Total Demographic Updates

These indicators provide a quick overview of Aadhaar system activity within Tamil Nadu.

---

### 2. Enrolment Composition

A pie chart showing the proportion of Aadhaar enrolments between:

* Children (0–17 years)
* Adults (18+ years)

This helps identify the demographic distribution of Aadhaar registrations.

---

### 3. Update Composition

A donut chart displaying the share of:

* Biometric updates
* Demographic updates

This helps analyze how citizens interact with Aadhaar update services.

---

### 4. Dynamic Chart Selection

Users can dynamically choose two additional analytical charts from the sidebar under **Other Charts**.

Available chart options include:

* Age-wise Aadhaar Enrolment Composition
* Biometric vs Demographic Update Trends
* Enrolment–Update Stress Index (EUSI)
* Child Lifecycle Compliance Trend
* Adult Demographic Volatility
* Biometric Update Demand Trend
* District Update Pressure
* District Stress Classification
* Child Compliance Gap by District

---

### 5. Duplicate Chart Handling

The dashboard prevents rendering identical charts in multiple slots. If the same chart is selected more than once or conflicts with default charts, a warning message is displayed instead of crashing the application.

---

## Data Processing

The application loads Aadhaar datasets stored inside a ZIP file and performs several transformations:

1. Reads enrolment, biometric update, and demographic update datasets.
2. Converts the `date` field into a datetime format.
3. Aggregates records at the state level.
4. Computes operational indicators such as:

### Enrolment–Update Stress Index (EUSI)

Measures the pressure on the Aadhaar system by comparing update requests with new enrolments.

### Child Lifecycle Compliance

Evaluates whether children enrolled in Aadhaar are completing mandatory biometric updates.

### Adult Demographic Volatility

Measures the rate at which adults update their demographic information.

### District Update Pressure

Compares total updates against total enrolments to identify districts with higher operational load.

### District Stress Score

A composite indicator derived from normalized enrolment and update volumes to classify districts into:

* High Stress
* Medium Stress
* Low Stress

---

## Technologies Used

* Python
* Streamlit
* Plotly
* Pandas
* NumPy

---

## File Structure

```
project-folder/
│
├── TNaadhar_lifecycle.py
├── uidai_TN_Datasets.zip
└── README.md
```

---

## How to Run the Dashboard

### Step 1: Install Dependencies

Install required Python libraries:

```
pip install streamlit pandas numpy plotly
```

---

### Step 2: Place Dataset

Ensure the dataset ZIP file is located at the specified path inside the script:

```
C:\Users\parth\Downloads\uidai_TN_Datasets.zip
```

---

### Step 3: Run the Application

Open command prompt in the project directory and run:

```
streamlit run TNaadhar_lifecycle.py
```

The dashboard will automatically open in your web browser.

---

## Dashboard Layout

The dashboard is organized into four main sections:

1. **KPI Summary**
2. **Enrolment Composition Chart**
3. **Update Composition Chart**
4. **Two dynamically selectable analytical charts**

This layout ensures a clear and compact view without excessive scrolling.

---

## Applications

This dashboard can assist:

* Government administrators monitoring Aadhaar operations
* Data analysts studying demographic update patterns
* Policy planners evaluating compliance with Aadhaar lifecycle requirements
* Researchers exploring digital identity infrastructure trends

---

## Future Enhancements

Potential improvements include:

* District-level filtering
* Time-range filtering
* Integration with live Aadhaar datasets
* Geographic visualization of district stress levels
* Exportable reports for administrative review

---

## Author

Developed as part of an analytics project exploring Aadhaar operational data for Tamil Nadu.
