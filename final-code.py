import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
#import plotly.figure_factory as ff
#import plotly.graph_objs as go


# Global variable to track the current tab
current_tab = 'Homepage'

def plot_interactive_bar_chart_EDA():
    
    df_eda =pd.read_csv(r"C:\Users\anilp\Project_Files\23-11-2023 11h59m03s\df_all_eda.csv", header=0)
    
    # Define category labels
    category_labels = ['Low', 'Mid', 'High']
    # Define the category thresholds
    num_categories = 3
    
    #Define the min and max of HR
    eda_min = df_eda['EDA'].min()
    eda_max = df_eda['EDA'].max()
    
    thresholds = [eda_min]
    thresholds.extend([eda_min + (i + 1) * ((eda_max - eda_min) / num_categories) for i in range(num_categories - 1)])
    thresholds.append(eda_max)

    # Categorize values
    categories = pd.cut(df_eda['EDA'], bins=thresholds, labels=category_labels)

    # Group by category and count occurrences
    category_counts = categories.value_counts().reindex(category_labels, fill_value=0)

    # Create a DataFrame with category labels and counts
    df_counts = pd.DataFrame({'Categories': category_counts.index, 'Counts': category_counts.values})

    # Create a bar chart using Plotly Express
    fig_eda = px.bar(df_counts, x='Categories', y=[thresholds[i + 1] - thresholds[i] for i in range(num_categories)], base=thresholds[:-1], title="Overall EDA Data")
    
    fig_eda.update_traces(
        hoverinfo='y',
        hovertemplate='Threshold: %{y}'
    )

    fig_eda.update_layout(
        xaxis_title='Categories',
        yaxis_title='Thresholds',
        showlegend=False
    )

    st.plotly_chart(fig_eda)
    
def plot_interactive_bar_chart_HR():
    
    df_hr =pd.read_csv(r"C:\Users\anilp\Project_Files\23-11-2023 11h57m59s\df_all_hr.csv", header=0)
    
    # Define category labels
    category_labels = ['Low', 'Mid', 'High']
    # Define the category thresholds
    num_categories = 3
    
    #Define the min and max of HR
    hr_min = df_hr['HR'].min()
    hr_max = df_hr['HR'].max()
    
    thresholds = [hr_min]
    thresholds.extend([hr_min + (i + 1) * ((hr_max - hr_min) / num_categories) for i in range(num_categories - 1)])
    thresholds.append(hr_max)

    # Categorize values
    categories = pd.cut(df_hr['HR'], bins=thresholds, labels=category_labels)

    # Group by category and count occurrences
    category_counts = categories.value_counts().reindex(category_labels, fill_value=0)

    # Create a DataFrame with category labels and counts
    df_counts = pd.DataFrame({'Categories': category_counts.index, 'Counts': category_counts.values})

    # Create a bar chart using Plotly Express
    fig_hr = px.bar(df_counts, x='Categories', y=[thresholds[i + 1] - thresholds[i] for i in range(num_categories)], base=thresholds[:-1], title="Overall HR Data")
    
    fig_hr.update_traces(
        hoverinfo='y',
        hovertemplate='Threshold: %{y}'
    )

    fig_hr.update_layout(
        xaxis_title='Categories',
        yaxis_title='Thresholds',
        showlegend=False
    )

    st.plotly_chart(fig_hr)

# Function to plot interactive line charts for EDA and BVP
def plot_interactive_line_charts(data, start_time_eda, end_time_eda, start_time_bvp, end_time_bvp):
    
    # Filter data for EDA based on time range
    filtered_data_eda = data[(data['Time'] >= start_time_eda) & (data['Time'] <= end_time_eda)]
    
    # Plot line chart for EDA
    fig_eda = px.line(filtered_data_eda, x='Time', y='EDA', title="Line Chart for EDA")
    fig_eda.update_layout(
        xaxis_title='Time',
        yaxis_title='EDA',
        showlegend=True
    )
    
    st.plotly_chart(fig_eda)
    plot_interactive_bar_chart_EDA()

    # Filter data for BVP based on time range
    filtered_data_bvp = data[(data['Time'] >= start_time_bvp) & (data['Time'] <= end_time_bvp)]
    
    # Plot line chart for BVP
    fig_hr = px.line(filtered_data_bvp, x='Time', y='HR', title="Line Chart for HR")
    fig_hr.update_layout(
        xaxis_title='Time',
        yaxis_title='HR',
        showlegend=True
    )
    
    st.plotly_chart(fig_hr)
    plot_interactive_bar_chart_HR()

# Function to manage food consumption history in Tab 2
def manage_food_history():
    st.subheader('Food Consumption Tracker')
    
    # Create or load the food history data
    if 'food_history' not in st.session_state:
        st.session_state.food_history = pd.DataFrame(columns=['Datetime', 'Food', 'Calories'])
    
    # Input for the user to enter consumed food and calories
    food_consumed = st.text_input('Enter the Consumed Food:')
    calories_consumed = st.number_input('Enter the Calories Consumed:', min_value=0)
    
    # Button to add the input to the history
    if st.button('Add to History'):
        current_datetime = pd.Timestamp.now()
        st.session_state.food_history = st.session_state.food_history.append({'Datetime': current_datetime, 'Food': food_consumed, 'Calories': calories_consumed}, ignore_index=True)
        st.success(f"Added: {food_consumed} with {calories_consumed} calories at {current_datetime} to the history.")

    # Expander to show and hide the history
    with st.expander("Food Consumption History"):
        st.write(st.session_state.food_history)

    # Calculate and display average weekly calorie consumption
    st.subheader('Average Weekly Calorie Consumption')
    st.session_state.food_history['Datetime'] = pd.to_datetime(st.session_state.food_history['Datetime'])
    weekly_calories_user = st.session_state.food_history.set_index('Datetime').resample('W-Mon')['Calories'].sum()
    average_weekly_calories_user = weekly_calories_user.mean()
    st.write(f'The average weekly calorie consumption based on user inputs is: {average_weekly_calories_user:.2f} calories.')

    # Calculate and display average weekly calorie consumption for the entire history
    weekly_calories_total = st.session_state.food_history.resample('W-Mon', on='Datetime')['Calories'].sum()
    average_weekly_calories_total = weekly_calories_total.mean()
    st.write(f'The average weekly calorie consumption for the entire history is: {average_weekly_calories_total:.2f} calories.')



    # Add content for Tab 3 as needed

# Main Streamlit app
def main():
    global current_tab

    # Read data from CSV file
    csv_file_path = r"C:\Users\anilp\Project_Files\testing\df_result.csv"
    data = pd.read_csv(csv_file_path)

    # Convert 'Time' column to datetime format
    data['Time'] = pd.to_datetime(data['Time'])

    # Extract the tab name from the URL
    tab = st.experimental_get_query_params().get("tab", ["Homepage"])[0]

    current_tab = tab  # Update the current tab

    if st.button("Homepage"):
         current_tab = 'Homepage'
         st.experimental_set_query_params(tab=current_tab)
         homepage_content()
    
    elif st.button("Gym"):
         current_tab = 'Gym'
         st.experimental_set_query_params(tab=current_tab)
         gym_content(data)
    
    elif st.button("Health"):
         current_tab = 'Health'
         st.experimental_set_query_params(tab=current_tab)
         health_content()
    
    elif st.button("Pop-up"):
         current_tab = 'Pop-up'
         st.experimental_set_query_params(tab=current_tab)
         popup_content()



    # Function for Homepage content
@st.cache_resource(experimental_allow_widgets=True)
def homepage_content():
    
    st.write('With our app you can see the data related to EDA and BVP while keeping a track of your calories and weight!')
    st.divider()
    st.write('The EDA stands for Electrodermal activity. EDA is used to measure the conductance of the skin, also known as sweat.')
    st.write(' The BVP stands for blood volume pulse. The BVP is used as a method to measure heartbeats by measuring the volume of blood that flows through the arteries where the sensor is placed, the E4 empathica wristband.')
    
    st.divider()
    st.write('Average weekly calorie consumption(measured by last 7 inputs in dataframe): 123')
    st.write('Average weekly weight(measured by last 7 inputs in dataframe): 123')
    st.divider()

    #st.write('Pop-up Button')
    calendar = pd.DataFrame(index=['Week 1','Week 2','Week 3', 'Week 4'], columns=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
    st.write(calendar)
    
    #st.markdown('<style>' + open('icons.css').read() + '</style>', unsafe_allow_html=True)
    
    # Add any additional content you want for the homepage
    #st.write('Homepage Button')
    
   


# Function for Gym content
@st.cache_resource(experimental_allow_widgets=True)
def gym_content(data):
    
    st.write('This is the gym content.')

    # Call function for interactive line charts
    plot_interactive_line_charts(data, data['Time'].min(), data['Time'].max(), data['Time'].min(), data['Time'].max())

    

# Function for Health content
@st.cache_resource(experimental_allow_widgets=True)
def health_content():
    st.write('This is the health content.')
    #manage_food_history()
    
    calorie = pd.DataFrame(index=['Input values:'], columns=['Your calorie intake on Monday was : 1', 'Your calorie intake on Tuesday was : 2', 'Your calorie intake on Wednesday was : 3',
    'Your calorie intake on Thursday was : 4', 'Your calorie intake on Friday was : 5', 'Your calorie intake on Saturday was : 6', 'Your calorie intake on Sunday was : 7'])


    weight = pd.DataFrame(index=['Input values'], columns=['Your weight on Monday was : ', 'Your weight on Tuesday was : ', 'Your weight on Wednesday was : ',
    'Your weight on Thursday was : ', 'Your weight on Friday was : ', 'Your weight on Saturday was : ', 'Your weight on Sunday was : '])
    
    st.write(calorie, 'Average calorie consumption for your week was : ')
    
    st.write(weight, 'Avegare weight for your week was : ')

# Function for Pop-up content
@st.cache_resource(experimental_allow_widgets=True)
def popup_content():
    st.write('This is the pop-up content.')
        

if __name__ == '__main__':
    main()
