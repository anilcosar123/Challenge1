import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import altair as alt


# Global variable to track the current tab
# Global variable to track the current tab
current_tab = 'Homepage'

def plot_interactive_bar_chart_EDA():
    
    df = pd.read_csv(r"C:\Users\anilp\Project_Files\13-11-2023 09h53m09s\df_all_eda.csv")

    filtered_df = df[df['EDA'] >= 1]
    
    bins = [0.5, 4, 8, float('inf')]
    labels = ['Low', 'Medium', 'High']
    
    filtered_df['Category'] = pd.cut(filtered_df['EDA'], bins=bins, labels=labels, right=False)

    grouped_df = filtered_df.groupby(['Category', 'EDA']).size().reset_index(name='Count')
   
    median_value = filtered_df['EDA'].median()
    mean_value = filtered_df['EDA'].mean()
    mode_value = filtered_df['EDA'].mode().iloc[0]  

    chart = alt.Chart(grouped_df).mark_bar().encode(
        x='EDA:Q',
        y='Count:Q',
        color='Category:N',
        tooltip=['Category:N', 'EDA:Q', 'Count:Q']
    )

    chart = chart + \
        alt.Chart(pd.DataFrame({'value': [mean_value]})).mark_rule(color='red').encode(x='value:Q', size=alt.value(2)) + \
        alt.Chart(pd.DataFrame({'value': [median_value]})).mark_rule(color='green').encode(x='value:Q', size=alt.value(2)) + \
        alt.Chart(pd.DataFrame({'value': [mode_value]})).mark_rule(color='blue').encode(x='value:Q', size=alt.value(2))

    st.altair_chart(chart, use_container_width=True)
    
    
    
def plot_interactive_bar_chart_BVP():
    
    df = pd.read_csv(r"C:\Users\anilp\Project_Files\13-11-2023 21h24m55s\df_all_bvp.csv")
    
    filtered_df = df[(df['BVP'] >= 2) & (df['BVP'] <= 260)]

    bins = [ 1.5, 4, 8, 500]
    labels = [ 'Low', 'Medium', 'High']

    filtered_df['Category'] = pd.cut(filtered_df['BVP'], bins=bins, labels=labels, right=False)

    grouped_df = filtered_df.groupby(['Category', 'BVP']).size().reset_index(name='Count')
   
    median_value = filtered_df['BVP'].median()
    mean_value = filtered_df['BVP'].mean()
    mode_value = filtered_df['BVP'].mode().iloc[0]  

    chart = alt.Chart(grouped_df).mark_bar().encode(
        x='BVP:Q',
        y='Count:Q',
        color='Category:N',
        tooltip=['Category:N', 'BVP:Q', 'Count:Q']
    )

    chart = chart + \
        alt.Chart(pd.DataFrame({'value': [mean_value]})).mark_rule(color='red').encode(x='value:Q', size=alt.value(2)) + \
        alt.Chart(pd.DataFrame({'value': [median_value]})).mark_rule(color='green').encode(x='value:Q', size=alt.value(2)) + \
        alt.Chart(pd.DataFrame({'value': [mode_value]})).mark_rule(color='blue').encode(x='value:Q', size=alt.value(2))

    st.altair_chart(chart, use_container_width=True)
    

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
    plot_interactive_bar_chart_EDA()

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
    plot_interactive_bar_chart_BVP()

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

# =============================================================================
#     # Use st.checkbox with Markdown styling for buttons
#     if st.checkbox("Homepage", key="Homepage", value=current_tab == 'Homepage', help="<div style='margin-bottom: 10px;'>Homepage</div>"):
#         current_tab = 'Homepage'
#         st.experimental_set_query_params(tab=current_tab)
#         homepage_content()
#     
#     if st.checkbox("Gym", key="Gym", value=current_tab == 'Gym', help="<div style='margin-bottom: 10px;'>Gym</div>"):
#         current_tab = 'Gym'
#         st.experimental_set_query_params(tab=current_tab)
#         gym_content(data)
#     
#     if st.checkbox("Health", key="Health", value=current_tab == 'Health', help="<div style='margin-bottom: 10px;'>Health</div>"):
#         current_tab = 'Health'
#         st.experimental_set_query_params(tab=current_tab)
#         health_content()
#     
#     if st.checkbox("Pop-up", key="Pop-up", value=current_tab == 'Pop-up', help="<div style='margin-bottom: 10px;'>Pop-up</div>"):
#         current_tab = 'Pop-up'
#         st.experimental_set_query_params(tab=current_tab)
#         popup_content()
#         
# =============================================================================
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
