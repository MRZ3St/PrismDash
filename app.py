import pandas as pd
import streamlit as st
import plotly.express as px

# Load the dataset
dataset = pd.read_excel("temp2.xlsx", sheet_name="Dash")
top_ten_data = pd.read_excel("temp2.xlsx", sheet_name="TopTenTest")  # Load TopTenTest sheet
dept_data = pd.read_excel("temp2.xlsx", sheet_name="Dept")

# Set page configuration
st.set_page_config(page_title="Prism_DashBoard", layout="wide")

# Sidebar navigation options
navigation_option = st.sidebar.radio("Navigation", ["Home", "My Department"])

# Add a background image with opacity using HTML and CSS
st.markdown(
    """
    <style>
        body {
            background-image: url(https://images.pexels.com/photos/3586966/pexels-photo-3586966.jpeg?auto=compress&cs=tinysrgb&w=600);
            background-size: cover;
            background-repeat: no-repeat;
            background-position: center;
            height: 100vh; /* Set the height to 100% of the viewport height */
            opacity: 0.8;
        }
    </style>
    """,
    unsafe_allow_html=True
)

if navigation_option == "Home":
    st.subheader("Fatigue Severity Distribution")

    # Mapping of severity levels to corresponding names
    severity_mapping = {1: "Severe", 2: "High", 3: "Significant", 4: "Guarded", 5: "Low"}

    # Display severity squares at the top
    severity_levels = [1, 2, 3, 4, 5]

    # Create a container for the squares and names with left margin
    squares_container = st.empty()
    left_margin_percentage = 5  # Adjust this value as needed

    # Set the width and height of each square container as a percentage of the total width and height
    square_width_percentage = 12
    square_height_percentage = 70  # Adjust this value as needed

    # Set the margin between squares
    margin_between_squares = 2

    # Create a string containing HTML for the entire row of squares and names
    squares_html = " ".join(
        f'<div style="display:inline-block;text-align:center;width:{square_width_percentage}%;'
        f'margin-right:{margin_between_squares}%;margin-left:{left_margin_percentage}%;overflow:hidden;">'
        f'<div style="border:1px solid #2F4F4F;background-color:#2F4F4F;color:white;height:auto;padding:5px;margin-bottom:5px;">{severity_mapping.get(level)}</div>'
        f'<div style="border:2px solid gray;height:{square_height_percentage}%;padding:20px;border-radius:5px;margin:5px;">{dataset[dataset["ClockInStatus"] == level]["EmployeeName"].count()}</div>'
        f'</div>'
        for level in severity_levels
    )

    # Add a border to create a continuous line at the bottom of the squares
    squares_html += '<div style="border-bottom: 1px solid gray; width: 100%; margin-top: 10px;"></div>'

    # Render the entire row of squares and names
    squares_container.markdown(squares_html, unsafe_allow_html=True)

    # Display the filtered data if filters are selected
    # No filter in the sidebar, so no need for this part

    # Container for the chart square
    chart_square_container = st.empty()

    # Set the width and height of the chart square as a percentage of the total width and height
    chart_square_width_percentage = 30
    chart_square_height_percentage = 50

    # Create a string containing HTML for the chart square
    chart_square_html = (
        f'<div style="display:flex;justify-content:center;align-items:center;width:{chart_square_width_percentage}%;'
        f'height:{chart_square_height_percentage}%;border:2px solid #2F4F4F;background-color:#2F4F4F;color:white;border-radius:5px;margin:10px;">'
    )

    # Render the chart square

    # Bar chart for top ten departments with the most people in "High" fatigue
    bar_chart_container_high = st.empty()
    top_departments_high = dataset[dataset["ClockInStatus"] == 2].groupby('Dept')['EmployeeName'].count().sort_values(ascending=False).head(10)
    fig_high = px.bar(
        top_departments_high,
        x=top_departments_high,
        y=top_departments_high.index,
        orientation='h',
        text=top_departments_high,
        labels={'EmployeeName': 'Number of People in High Fatigue'},
        title='Top 10 Departments with Most People in High Fatigue'
    )

    # Remove x-axis labels
    fig_high.update_layout(xaxis=dict(tickmode='array', tickvals=[]))

    fig_high.update_traces(textposition='outside')  # Display text outside the bar

    # Set the chart width and height to 1/3 of its current size
    chart_width = 150  # (1/3 of 500)
    chart_height = 130  # (1/3 of 400)

    # Set a fixed border for the chart
    border_size = 2
    border_color = "#2F4F4F"  # Dark gray color for the border
    border_style = "solid"
    chart_border_style = f"{border_size}px {border_style} {border_color}"

    # Render the chart inside the chart square

    # Bar chart for top ten departments with the most people in "Guarded" fatigue
    bar_chart_container_guarded = st.empty()
    top_departments_guarded = dataset[dataset["ClockInStatus"] == 4].groupby('Dept')['EmployeeName'].count().sort_values(ascending=False).head(10)
    fig_guarded = px.bar(
        top_departments_guarded,
        x=top_departments_guarded,
        y=top_departments_guarded.index,
        orientation='h',
        text=top_departments_guarded,
        labels={'EmployeeName': 'Number of People in Guarded Fatigue'},
        title='Top 10 Departments with Most People in Guarded Fatigue'
    )

    # Remove x-axis labels
    fig_guarded.update_layout(xaxis=dict(tickmode='array', tickvals=[]))

    fig_guarded.update_traces(textposition='outside')  # Display text outside the bar

    # Render the chart inside the chart square

    left_column, right_column = st.columns(2)
    left_column.plotly_chart(fig_high, use_container_width=True)
    right_column.plotly_chart(fig_guarded, use_container_width=True)

    # Bar chart for top ten employees with the highest BLTScore
    bar_chart_container_blt = st.empty()
    top_employees_blt = top_ten_data.sort_values(by='BLTScores', ascending=False).head(10)
    fig_blt = px.bar(
        top_employees_blt,
        x='BLTScores',
        y='employeename',
        orientation='h',
        text='BLTScores',
        labels={'BLTScores': 'BLT Scores'},
        title='Top 10 Employees with Highest BLT Scores'
    )

    # Remove x-axis labels
    fig_blt.update_layout(xaxis=dict(tickmode='array', tickvals=[]))

    fig_blt.update_traces(textposition='outside')  # Display text outside the bar

    # Set the chart width and height to 1/3 of its current size
    chart_width = 150  # (1/3 of 500)
    chart_height = 130  # (1/3 of 400)

    # Set a fixed border for the chart
    border_size = 2
    border_color = "#2F4F4F"  # Dark gray color for the border
    border_style = "solid"
    chart_border_style = f"{border_size}px {border_style} {border_color}"

    # Render the chart inside the chart square
    bar_chart_container_blt.plotly_chart(fig_blt, use_container_width=True)

    # Replace NULL values with 0 in the columns for the last four weeks
    columns_to_fill = ["fourweeks", "threeweeks", "twoweeks", "currentweek"]
    dept_data[columns_to_fill] = dept_data[columns_to_fill].fillna(0)

    # Sum the values in each row to get the total tests over 4 weeks per department
    dept_data["total_tests_4_weeks"] = dept_data[columns_to_fill].sum(axis=1)

    # Filter out departments with zero tests
    dept_data = dept_data[dept_data["total_tests_4_weeks"] > 0]

    # Pie chart for tests performed over 4 weeks per department
    pie_chart_container = st.empty()

    fig_pie = px.pie(
        names=dept_data["Dept"],
        values=dept_data["total_tests_4_weeks"],
        title='Tests Performed Over 4 Weeks per Department',
        labels={'total_tests_4_weeks': 'Total Tests'},
        width=8 * chart_width,  # Increase the width by 15%
        height=8 * chart_height  # Increase the height by 15%
    )

    # Render the pie chart
    pie_chart_container.plotly_chart(fig_pie, use_container_width=True)

elif navigation_option == "My Department":
    st.subheader("My Department Features")

    # Dropdown menu for selecting the user's department
    selected_department = st.selectbox("Select Your Department", dataset["Dept"].unique())

    # Mapping of severity levels to corresponding names
    severity_mapping = {1: "Severe", 2: "High", 3: "Significant", 4: "Guarded", 5: "Low"}

    # Severity levels for displaying squares
    severity_levels = [1, 2, 3, 4, 5]

    # Set the width and height of each square container as a percentage of the total width and height
    square_width_percentage = 12
    square_height_percentage = 70  # Adjust this value as needed

    # Set the margin between squares
    margin_between_squares = 2

    # Set the left margin
    left_margin_percentage = 5  # Adjust this value as needed

    # Display severity squares at the top based on the selected department
    selected_dept_data = dataset[dataset["Dept"] == selected_department]
    severity_squares_html = " ".join(
        f'<div style="display:inline-block;text-align:center;width:{square_width_percentage}%;'
        f'margin-right:{margin_between_squares}%;margin-left:{left_margin_percentage}%;overflow:hidden;">'
        f'<div style="border:1px solid #2F4F4F;background-color:#2F4F4F;color:white;height:auto;padding:5px;margin-bottom:5px;">{severity_mapping.get(level)}</div>'
        f'<div style="border:2px solid gray;height:{square_height_percentage}%;padding:20px;border-radius:5px;margin:5px;">{selected_dept_data[selected_dept_data["ClockInStatus"] == level]["EmployeeName"].count()}</div>'
        f'</div>'
        for level in severity_levels
    )

    # Add a border to create a continuous line at the bottom of the squares
    severity_squares_html += '<div style="border-bottom: 1px solid gray; width: 100%; margin-top: 10px;"></div>'

    # Render the severity squares
    st.markdown(severity_squares_html, unsafe_allow_html=True)

    # You can add additional features for the selected department here.


