# ⏳ Life Time Dashboard

A Streamlit application that visualizes how you have spent your time so far in life and projects how you will spend the rest of your life based on your daily habits. Ideal for self-reflection, time management, and showcasing data skills in your portfolio.

---

## Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the App](#running-the-app)
- [Usage Guide](#usage-guide)
  - [Sidebar Inputs](#sidebar-inputs)
  - [Unit and Visualization Selection](#unit-and-visualization-selection)
  - [Charts and Summaries](#charts-and-summaries)
  - [Insights and Recommendations](#insights-and-recommendations)
  - [Export and Download](#export-and-download)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [Contributing](#contributing)

---

## Features

- **Customizable Inputs**: Enter your date of birth, expected lifespan, and daily hours for work, sleep, exercise, travel, meals, family/friends, plus up to 10 custom activities.
- **Unit Selection**: View results in years, months, weeks, days, or hours.
- **Multiple Visualizations**: Choose from pie charts (including donut), bar charts, and treemaps.
- **Interactive Charts**: Click on legend items to include/exclude categories.
- **Detailed Summary Table**: Compare time spent versus remaining, with percentages.
- **Insights and Recommendations**: See metrics for free time and get actionable suggestions.
- **Data Export**: Download your data as CSV or JSON for further analysis.

---

## Getting Started

### Prerequisites

- Python 3.7 or later
- Streamlit library
- Git (optional)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/life-time-dashboard.git
   cd life-time-dashboard
   ```

2. (Optional) Create and activate a virtual environment:

   ```bash
   python -m venv venv
   # macOS/Linux
   source venv/bin/activate
   # Windows
   venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

### Running the App

Launch the Streamlit server:

```bash
streamlit run life_dashboard_app.py
```

Open the URL printed in the terminal (e.g., [http://localhost:8501](http://localhost:8501)).

---

## Usage Guide

### Sidebar Inputs

- **Select Unit**: Choose your time unit (Years, Months, Weeks, Days, Hours).
- **Select Visualization**: Pick Pie Chart, Donut Chart, or Bar Chart.
- **Date of Birth**: Select via date picker.
- **Expected Age**: Enter your anticipated lifespan in years (default: 63).
- **Daily Activities**: Input hours per day for Work, Sleep, Exercise, Travel, Eating, Family/Friends.
- **Custom Categories**: Add up to 10 extra activities (name + hours).

### Unit and Visualization Selection

Use the dropdowns at the top to dynamically update all metrics and charts in your chosen unit and style.

### Charts and Summaries

- **Pie/Donut Charts**: Visualize proportion of time spent vs. remaining per activity.

- **Bar Chart**: Compare time spent and remaining side-by-side.

- **Treemap**: See hierarchical view of spent vs. remaining time.

- **Detailed Table**: Presents numeric values and percentage breakdowns per activity.

### Insights and Recommendations

View highlighted metrics for daily free time and estimated free days left, with color-coded suggestions to optimize your schedule.

### Export and Download

Download your activity data at the bottom of the app as:

- **CSV**: `life_time_data.csv`
- **JSON**: `life_time_data.json`

---

## Project Structure

```text
├── life_dashboard_app.py   # Main Streamlit application file
├── requirements.txt       # Python dependencies
└── readme.md              # Project documentation
```

---

## Tech Stack

- **Frontend**: Streamlit
- **Data Processing**: Python, pandas
- **Visualization**: Plotly Express

---

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.
