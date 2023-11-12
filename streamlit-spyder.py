import streamlit as st
import pandas as pd
import plotly.express as px



# Global variable to track the current tab
# Global variable to track the current tab
current_tab = 'Homepage'


# Function to plot interactive line charts for EDA and BVP
def plot_interactive_line_charts(data, start_time_eda, end_time_eda, start_time_bvp, end_time_bvp):
    st.subheader('Interactive Line Charts')
    
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

    # Filter data for BVP based on time range
    filtered_data_bvp = data[(data['Time'] >= start_time_bvp) & (data['Time'] <= end_time_bvp)]
    
    # Plot line chart for BVP
    fig_bvp = px.line(filtered_data_bvp, x='Time', y='BVP', title="Line Chart for BVP")
    fig_bvp.update_layout(
        xaxis_title='Time',
        yaxis_title='BVP',
        showlegend=True
    )
    
    st.plotly_chart(fig_bvp)

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


    # Function for Homepage content
@st.cache_resource
def homepage_content():
    
    st.write('This is the homepage content.')

    st.title('Welcome to Your App Homepage')
    
    # Add some introductory text
    st.write('This is the homepage of your phone app.')

    # Display a calendar image (replace the URL with your own image)
    st.image(r"C:\Users\anilp\Project_Files\streamlit stuff\calendar.jpg", caption='Your Calendar Image', use_column_width=True)

    # Add any additional content you want for the homepage
    st.write('Feel free to explore other tabs using the navigation sidebar.')
    
   


# Function for Gym content
@st.cache_resource
def gym_content(data):
    
    st.write('This is the gym content.')
    # Define slider for interactivity - Line Charts
    st.subheader("Line Chart Configuration for EDA")
    start_time_line_eda = st.slider("Select Start Time - Line Chart (EDA)", min_value=data['Time'].min().timestamp(), max_value=data['Time'].max().timestamp(), value=data['Time'].min().timestamp())
    end_time_line_eda = st.slider("Select End Time - Line Chart (EDA)", min_value=data['Time'].min().timestamp(), max_value=data['Time'].max().timestamp(), value=data['Time'].max().timestamp())

    st.subheader("Line Chart Configuration for BVP")
    start_time_line_bvp = st.slider("Select Start Time - Line Chart (BVP)", min_value=data['Time'].min().timestamp(), max_value=data['Time'].max().timestamp(), value=data['Time'].min().timestamp())
    end_time_line_bvp = st.slider("Select End Time - Line Chart (BVP)", min_value=data['Time'].min().timestamp(), max_value=data['Time'].max().timestamp(), value=data['Time'].max().timestamp())

    # Call function for interactive line charts
    plot_interactive_line_charts(data, pd.Timestamp(start_time_line_eda, unit='s'), pd.Timestamp(end_time_line_eda, unit='s'),
                                 pd.Timestamp(start_time_line_bvp, unit='s'), pd.Timestamp(end_time_line_bvp, unit='s'))
    

# Function for Health content
@st.cache_resource
def health_content():
    st.write('This is the health content.')
    manage_food_history()
    


# Function for Pop-up content
@st.cache_resource
def popup_content():
    st.write('This is the pop-up content.')
        

    # Add content for Tab 3 as needed

# Main Streamlit app
def main():
    global current_tab

    # Read data from CSV file
    csv_file_path = r"C:\Users\anilp\Project_Files\testing\df_result.csv"
    data = pd.read_csv(csv_file_path)

    # Convert 'Time' column to datetime format
    data['Time'] = pd.to_datetime(data['Time'])

    # Header with navigation buttons
    header_html = """
        <style>
            .header {
                display: flex;
                justify-content: space-between;
            }
            .nav-buttons {
                display: flex;
            }
            .nav-button {
                margin-right: 10px;
            }
        </style>
        <div class="header">
            <h1>Gym/Health</h1>
            <div class="nav-buttons">
                <button class="nav-button" onclick="setTab('Homepage');">Homepage</button>
                <button class="nav-button" onclick="setTab('Gym');">Gym</button>
                <button class="nav-button" onclick="setTab('Health');">Health</button>
            </div>
        </div>
    """

    st.markdown(header_html, unsafe_allow_html=True)
    
    
    # Extract the tab name from the URL
    tab = st.experimental_get_query_params().get("tab", ["Homepage"])[0]

    current_tab = tab  # Update the current tab

    # Use st.cache to cache the function results
    if tab == 'Homepage':
        homepage_content()

    elif tab == 'Gym':
        gym_content(data)

    elif tab == 'Health':
        health_content()

    elif tab == 'Pop-up':
        popup_content()

    
    


if __name__ == '__main__':
    main()
