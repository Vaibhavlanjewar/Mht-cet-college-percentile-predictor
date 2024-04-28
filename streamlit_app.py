
import pandas as pd
import pickle
import streamlit as st

# Assuming 'data.csv' contains your data
df = pd.read_csv('mht_cet2.csv')

# Load the trained Decision Tree Regressor model
with open('decision_tree_model.pkl', 'rb') as file:
    dt_regressor = pickle.load(file)

# Create a dictionary to map encoded values to their original form
gender_map = {0: 'Male', 1: 'Female'}
category_map = {1: 'GEN', 2: 'OBC', 3: 'SC', 4: 'ST', 5: 'EWS'}
seat_type_map = {0: 'AIQ', 1: 'HS', 2: 'OS', 3: 'J&K'}
primary_seat_type_map = {0: 'GEN', 1: 'OBC', 2: 'SC', 3: 'ST', 4: 'GEN-EWS', 5: 'Tuition Fee Waiver'}
secondary_seat_type_map = {0: 'None', 1: 'GEN', 2: 'OBC', 3: 'SC', 4: 'ST', 5: 'GEN-EWS'}
score_type_map = {0: 'percentile'}

# Extract unique college names and branch names from the DataFrame
college_names = df['college_name'].unique()
branch_names = df['branch'].unique()

# Create a dictionary to map college names and branch names to encoded values
college_name_map = {college_name: i for i, college_name in enumerate(college_names)}
branch_name_map = {branch_name: i for i, branch_name in enumerate(branch_names)}

# Add a header
st.header('MHT-CET Percentile Predictor')

# Create dropdown widgets for original features
gender_dropdown = st.selectbox('Gender:', options=list(gender_map.values()))
category_dropdown = st.selectbox('Category:', options=list(category_map.values()))
seat_type_dropdown = st.selectbox('Seat Type:', options=list(seat_type_map.values()))
primary_seat_type_dropdown = st.selectbox('Primary Seat Type:', options=list(primary_seat_type_map.values()))
secondary_seat_type_dropdown = st.selectbox('Secondary Seat Type:', options=list(secondary_seat_type_map.values()))
score_type_dropdown = st.selectbox('Score Type:', options=list(score_type_map.values()))
college_name_dropdown = st.selectbox('College Name:', options=college_names)
branch_name_dropdown = st.selectbox('Branch:', options=branch_names)

# Create a rank input widget
rank_input = st.number_input('Rank:', value=0)

# Create a button widget for prediction
predict_button = st.button('Predict')

# Function to handle button click event
def on_predict_button_clicked():
    # Encode selected values
    gender_encoded = list(gender_map.keys())[list(gender_map.values()).index(gender_dropdown)]
    category_encoded = list(category_map.keys())[list(category_map.values()).index(category_dropdown)]
    seat_type_encoded = list(seat_type_map.keys())[list(seat_type_map.values()).index(seat_type_dropdown)]
    primary_seat_type_encoded = list(primary_seat_type_map.keys())[list(primary_seat_type_map.values()).index(primary_seat_type_dropdown)]
    secondary_seat_type_encoded = list(secondary_seat_type_map.keys())[list(secondary_seat_type_map.values()).index(secondary_seat_type_dropdown)]
    score_type_encoded = list(score_type_map.keys())[list(score_type_map.values()).index(score_type_dropdown)]
    college_name_encoded = college_name_map[college_name_dropdown]
    branch_encoded = branch_name_map[branch_name_dropdown]

    # Create a DataFrame with the selected features
    data = {'rank': [rank_input], 
            'gender_encoded': [gender_encoded], 
            'category_encoded': [category_encoded],
            'seat_type_encoded': [seat_type_encoded],
            'primary_seat_type_encoded': [primary_seat_type_encoded],
            'secondary_seat_type_encoded': [secondary_seat_type_encoded],
            'score_type_encoded': [score_type_encoded],
            'college_name_encoded': [college_name_encoded],
            'branch_encoded': [branch_encoded]
            }
    input_df = pd.DataFrame(data)
    
    # Make prediction using the Decision Tree Regressor model
    percentile_prediction = dt_regressor.predict(input_df)
    
    st.write(f'Predicted Percentile for Rank {rank_input} at {college_name_dropdown}: {percentile_prediction[0]}')

# Check if the predict button is clicked
if predict_button:
    on_predict_button_clicked()

# Add Made by statement

st.text("\n---------------------------------- |Made by - VNBL|--------------------------------------------------------")
st.subheader("Contact Information")
# st.write("Made by: VNBL")
st.write("GitHub: [Vaibhavlanjewar](https://github.com/Vaibhavlanjewar/)")
st.write("LinkedIn: [Vaibhav Lanjewar](https://www.linkedin.com/in/vaibhavlanjewar/)")
st.write("--------------------------------------------------------------------------------------------------------------")