# -----------------------------------------------------------
# Life Time Dashboard App
# This Streamlit application visualizes your past and future time allocation
# based on daily activities and expected lifespan.
# -----------------------------------------------------------
import streamlit as st
import pandas as pd
from datetime import datetime, date
import plotly.express as px
import json

# Set page config for wide layout and custom title
st.set_page_config(page_title="Life Time Dashboard", layout="wide")

# ---- Sidebar Inputs ----
# Collect user inputs for unit, visualization type, and activity durations
st.sidebar.title("🎯 Your Life Dashboard Inputs")

selected_unit = st.sidebar.selectbox(
    "Select unit to display:",
    ['Years', 'Months', 'Weeks', 'Days', 'Hours'],
    index=0,
    key='unit'
)
selected_units = [selected_unit]

st.sidebar.subheader("📊 Visualization Type")
selected_viz = st.sidebar.selectbox(
    "Select visualization:",
    ['Pie Chart', 'Donut Chart', 'Bar Chart'],
    index=0,
    key='viz_type'
)

dob = st.sidebar.date_input("Date of Birth", date(2000, 1, 1))
expected_age = st.sidebar.number_input("Expected Age (years)", min_value=1, max_value=120, value=63)
job_hours = st.sidebar.number_input("Job Hours Per Day", min_value=0.0, max_value=24.0, value=8.0)
eating_hours = st.sidebar.number_input("Eating Hours Per Day", min_value=0.0, max_value=24.0, value=2.0)
travel_hours = st.sidebar.number_input("Travel Hours Per Day", min_value=0.0, max_value=24.0, value=1.0)
sleep_hours = st.sidebar.number_input("Sleep Hours Per Day", min_value=0.0, max_value=24.0, value=7.0)
exercise_hours = st.sidebar.number_input("Exercise Hours Per Day", min_value=0.0, max_value=24.0, value=0.5)
family_hours = st.sidebar.number_input(
    "Family/Friends Time Per Day",
    min_value=0.0,
    max_value=24.0,
    value=2.0
)

# ---- Add Custom Categories ----
# Allow users to define additional activity categories
st.sidebar.subheader("🛠️ Add Custom Categories")
num_custom = st.sidebar.number_input(
    "How many extra categories?",
    min_value=0,
    max_value=10,
    value=0,
    step=1,
    key="num_custom"
)

custom_categories = {}
for i in range(num_custom):
    cat_name = st.sidebar.text_input(
        f"Custom Category {i+1} Name",
        key=f"cat_name_{i}"
    )
    cat_hours = st.sidebar.number_input(
        f"Hours per Day for '{cat_name or 'Unnamed'}'",
        min_value=0.0,
        max_value=24.0,
        value=0.0,
        key=f"cat_hours_{i}"
    )
    if cat_name:
        custom_categories[cat_name] = cat_hours

# ---- Conversion Function ----
# Define how many hours each unit represents for conversion purposes
def hours_per_unit(unit):
    return {
        'Hours': 1,
        'Days': 24,
        'Weeks': 24*7,
        'Months': 24*30.4375,
        'Years': 24*365.25
    }[unit]

# ---- Core Calculations ----
# Compute current age, days lived, and projected remaining time
today = date.today()
age_years = (today - dob).days / 365.25
age_days = (today - dob).days
years_left = max(expected_age - age_years, 0)
days_left = max((expected_age * 365.25) - age_days, 0)
hours_left = days_left * 24
weeks_left = days_left / 7
months_left = days_left / 30.4375 # Average days in a month

# Calculate total committed hours including custom categories and free time
total_committed_hours = (
    job_hours + eating_hours + travel_hours + sleep_hours + exercise_hours + family_hours + sum(custom_categories.values())
)
free_hours_per_day = max(0.0, 24.0 - total_committed_hours)

# ---- Build Activity Categories ----
# Combine fixed activities, custom categories, and free time
categories = {
    "Working": job_hours,
    "Eating": eating_hours,
    "Traveling": travel_hours,
    "Sleeping": sleep_hours,
    "Exercise": exercise_hours,
    "Friends/Family": family_hours,
}
# merge in custom categories
for name, hrs in custom_categories.items():
    categories[name] = hrs

if free_hours_per_day > 0:
    categories["Free Time"] = free_hours_per_day

# ---- Time Spent and Future Projections ----
# Calculate total hours spent so far and hours expected in future per category
# Time spent so far (in hours)
time_spent = {k: v * age_days for k, v in categories.items()}
# Time expected in future (in hours)
time_future = {k: v * days_left for k, v in categories.items()}

# ---- Main Dashboard Display ----
# Title and summary of age and expected lifespan
st.title("⏳ Life Time Dashboard")
st.write(f"### You are **{age_years:.1f}** years old.")
st.write(f"### Estimated lifespan: **{expected_age}** years")

# ---- Display Remaining Life ----
# Remaining life metrics display in selected unit
st.subheader("⌛️ Your Estimated Remaining Life:")
for unit in selected_units:
    factor = hours_per_unit(unit)
    value = {
        'Years': years_left,
        'Months': months_left,
        'Weeks': weeks_left,
        'Days': days_left,
        'Hours': hours_left
    }[unit]
    st.write(f"- {unit}: **{value:.1f}**")


# ---- Charts and Activity Breakdown ----
# Show interactive charts (Pie, Donut, Bar, Treemap) with clickable legend
# Instruction for interactive legends
st.markdown("🔍 *To exclude any category from the chart, click on it in the legend.*")
for unit in selected_units:
    factor = hours_per_unit(unit)
    activities = list(time_spent.keys())
    spent_vals = [h/factor for h in time_spent.values()]
    future_vals = [h/factor for h in time_future.values()]

    if selected_viz in ['Pie Chart', 'Donut Chart']:
        hole = 0.4 if selected_viz == 'Donut Chart' else 0
        fig1 = px.pie(names=activities, values=spent_vals,
                      title=f'Time Spent So Far ({unit})', hole=hole)
        fig1.update_layout(
            title_font_size=28,
            legend_font_size=20,
            font=dict(size=18)
        )
        fig1.update_traces(textposition='inside', textinfo='percent+label', textfont_size=18)
        st.plotly_chart(fig1, use_container_width=True)

        fig2 = px.pie(names=activities, values=future_vals,
                      title=f'Time Left in Future ({unit})', hole=hole)
        fig2.update_layout(
            title_font_size=28,
            legend_font_size=20,
            font=dict(size=18)
        )
        fig2.update_traces(textposition='inside', textinfo='percent+label', textfont_size=18)
        st.plotly_chart(fig2, use_container_width=True)

    elif selected_viz == 'Bar Chart':
        df_bar = pd.DataFrame({
            'Activity': activities,
            'Spent': spent_vals,
            'Remaining': future_vals
        })
        fig_bar = px.bar(
            df_bar,
            x='Activity',
            y=['Spent', 'Remaining'],
            barmode='group',
            title=f'Time Allocation ({unit})'
        )
        fig_bar.update_layout(
            title_font_size=28,
            legend_font_size=20,
            font=dict(size=18),
            xaxis_tickangle=-45
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    elif selected_viz == 'Treemap':
        df_treemap = pd.DataFrame({
            'Type': ['Spent']*len(activities) + ['Remaining']*len(activities),
            'Activity': activities + activities,
            'Value': spent_vals + future_vals
        })
        fig_tree = px.treemap(
            df_treemap,
            path=['Type', 'Activity'],
            values='Value',
            title=f'Time Allocation Treemap ({unit})'
        )
        fig_tree.update_layout(
            title_font_size=28,
            font=dict(size=18)
        )
        st.plotly_chart(fig_tree, use_container_width=True)

# ---- Detailed Time Summary ----
# Present a data table with spent vs remaining values and percentages
st.subheader("📋 Detailed Time Summary")
for unit in selected_units:
    factor = hours_per_unit(unit)
    st.markdown(f"**Summary in {unit}:**")
    summary_data = []
    for activity, spent_h in time_spent.items():
        remaining_h = time_future.get(activity, 0)
        spent_val = spent_h / factor
        rem_val = remaining_h / factor
        total_val = spent_val + rem_val
        pct_spent = (spent_val / total_val * 100) if total_val else 0
        pct_rem = (rem_val / total_val * 100) if total_val else 0
        summary_data.append({
            "Activity": activity,
            f"Spent ({unit})": f"{spent_val:.1f}",
            f"Remaining ({unit})": f"{rem_val:.1f}",
            "% Spent": f"{pct_spent:.1f}",
            "% Remaining": f"{pct_rem:.1f}"
        })
    df_summary = pd.DataFrame(summary_data)
    st.dataframe(df_summary, use_container_width=True)

# ---- Insights & Recommendations ----
# Provide metrics and actionable suggestions based on free time and commitments
st.subheader("💡 Insights & Recommendations")
col1, col2 = st.columns(2)
with col1:
    st.metric("🆓 Free Time per Day (hrs)", f"{free_hours_per_day:.1f}")
    total_free_hours_left = free_hours_per_day * days_left
    st.metric("📆 Free Days Remaining", f"{(total_free_hours_left/24):.0f}")
with col2:
    if free_hours_per_day > 0:
        st.success("You have dedicated free time every day. Consider how to best use it!")
    else:
        st.error("No dedicated free time per day. Consider reducing commitments to avoid burnout.")
    if total_committed_hours > 24:
        st.warning(f"Daily activities sum to {total_committed_hours:.1f} hours, exceeding 24 hours!")

st.markdown("---")
st.info("💡 *\"Time is what we want most, but what we use worst.\"* - William Penn")
st.markdown("---")

# ---- Export & Download ----
# Allow users to download their data as CSV or JSON
st.header("📥 Export & Download")

# Prepare data export
export_df = pd.DataFrame({
    'Activity': list(categories.keys()),
    'Time Spent (hrs)': [time_spent[a] for a in categories.keys()],
    'Time Remaining (hrs)': [time_future[a] for a in categories.keys()]
})
# CSV export
csv_data = export_df.to_csv(index=False)
st.download_button(
    label="Download data as CSV",
    data=csv_data,
    file_name="life_time_data.csv",
    mime="text/csv"
)
# JSON export
json_data = json.dumps({
    'time_spent': time_spent,
    'time_future': time_future,
    'categories': categories
}, default=str, indent=2)
st.download_button(
    label="Download data as JSON",
    data=json_data,
    file_name="life_time_data.json",
    mime="application/json"
)
