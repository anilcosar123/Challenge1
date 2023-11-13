import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt



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

    # Use st.checkbox with Markdown styling for buttons
    if st.checkbox("Homepage", key="Homepage", value=current_tab == 'Homepage', help="<div style='margin-bottom: 10px;'>Homepage</div>"):
        current_tab = 'Homepage'
        st.experimental_set_query_params(tab=current_tab)
        homepage_content()
    
    if st.checkbox("Gym", key="Gym", value=current_tab == 'Gym', help="<div style='margin-bottom: 10px;'>Gym</div>"):
        current_tab = 'Gym'
        st.experimental_set_query_params(tab=current_tab)
        gym_content(data)
    
    if st.checkbox("Health", key="Health", value=current_tab == 'Health', help="<div style='margin-bottom: 10px;'>Health</div>"):
        current_tab = 'Health'
        st.experimental_set_query_params(tab=current_tab)
        health_content()
    
    if st.checkbox("Pop-up", key="Pop-up", value=current_tab == 'Pop-up', help="<div style='margin-bottom: 10px;'>Pop-up</div>"):
        current_tab = 'Pop-up'
        st.experimental_set_query_params(tab=current_tab)
        popup_content()



    # Function for Homepage content
@st.cache_resource(experimental_allow_widgets=True)
def homepage_content():
    
    st.write('With our app you can see the data related to EDA and BVP while keeping a track of your calories and weight!')
    st.write('EDA:', 'BVP:')
    
    # Add some introductory text
    st.write('Average weekly calorie consumption(measured by last 7 inputs in dataframe): 123')
    st.write('Average weekly weight(measured by last 7 inputs in dataframe): 123')
    
    st.write('Pop-up button')

    calendar = pd.DataFrame(index=['Week 1','Week 2','Week 3', 'Week 4'], columns=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
    st.write(calendar)
    
    st.markdown('<style>' + open('icons.css').read() + '</style>', unsafe_allow_html=True)
    
    # Add any additional content you want for the homepage
    st.write('Homepage Button' , )
    
   


# Function for Gym content
@st.cache_resource(experimental_allow_widgets=True)
def gym_content(data):
    
    st.write('This is the gym content.')

    # Call function for interactive line charts
    plot_interactive_line_charts(data, data['Time'].min(), data['Time'].max(), data['Time'].min(), data['Time'].max())

    # Read data for the bar chart from another CSV file
    bar_chart_data_path = r"C:\Users\anilp\Project_Files\10-11-2023 23h06m48s\df_result.csv"
    bar_chart_data = pd.read_csv(bar_chart_data_path)

    # Categorize values into Low, Medium, and High based on percentiles
    low_threshold = bar_chart_data['EDA'].quantile(0.33)
    high_threshold = bar_chart_data['EDA'].quantile(0.67)

    bar_chart_data['Category'] = pd.cut(bar_chart_data['EDA'], bins=[float('-inf'), low_threshold, high_threshold, float('inf')],
                              labels=['Low', 'Medium', 'High'])

    # Create a bar chart for the new data
    fig, ax = plt.subplots()

    # Count the occurrences in each category
    category_counts = bar_chart_data['Category'].value_counts()

    # Bar for each category
    for category in category_counts.index:
        ax.bar(category, category_counts[category], label=category)

    ax.set_ylabel('Count')
    ax.set_title('Category Distribution from Bar Chart Data')
    ax.legend(title='Category')

    # Set y-axis limits
    ax.set_ylim(0, 50)

    # Display the bar chart using st.pyplot
    st.pyplot(fig)

    

# Function for Health content
@st.cache_resource(experimental_allow_widgets=True)
def health_content():
    st.write('This is the health content.')
    #manage_food_history()
    
    calorie = pd.DataFrame(index=['Input values:'], columns=['Your calorie intake on Monday was : 1', 'Your calorie intake on Tuesday was : 2', 'Your calorie intake on Wednesday was : 3',
    'Your calorie intake on Thursday was : 4', 'Your calorie intake on Friday was : 5', 'Your calorie intake on Saturday was : 6', 'Your calorie intake on Sunday was : 7'])


    weight = pd.DataFrame(index=['Input values'], columns=['Your weight on Monday was : ', 'Your weight on Tuesday was : ', 'Your weight on Wednesday was : ',
    'Your weight on Thursday was : ', 'Your weight on Friday was : ', 'Your weight on Saturday was : ', 'Your weight on Sunday was : '])
    
    st.write(calorie)
    st.write('Average calorie consumption for your week was : ')
    
    st.write(weight)
    st.write('Avegare weight for your week was : ')


# Function for Pop-up content
@st.cache_resource(experimental_allow_widgets=True)
def popup_content():
    st.write('This is the pop-up content.')
        

if __name__ == '__main__':
    main()
