import streamlit as st
from dataset import df, spaces, stat, dweightweek, dweightphys
import json
import pandas as pd
from pandas import concat
import requests
URL = 'http://127.0.0.1:8000/{}' #вставить когда фастапи допишу
st.title('Weight Change Research')


st.subheader('Short overview')
st.dataframe(data = df)
st.write('The dataset provides information about the research of gaining and loosing weight by people of different ages and leading different lifestyles.')

st.subheader('Data Cleanup')
st.write("Let's look at the number of spaces in the dataset:")
st.dataframe(data=spaces, height=493, hide_index=True)
st.write("As we can see, there is no blank spaces, so dataset needn't filling.")

st.subheader('Info about columns')
st.write('Some descriptive statistics:')
st.dataframe(data = stat, hide_index=True)


st.header('Graphs and hypothesis')
st.subheader(body = 'Duration X Weight Change')
st.write('Hypothesis: The more the duration')
st.line_chart(data = dweightweek, x = 'Duration (weeks)', height=300)
st.write('As we can see, the more the duration of the research, the more the weight is able to change.')

st.subheader(body = 'Physical Activity Level X Max Weight Loss')
st.write('Hypothesis: People, who vere very active, have experienced the biggest weight loss.')
st.bar_chart(data=dweightphys.sort_values('Max Weight Loss'), x = 'Physical Activity Level', y = 'Max Weight Loss')
st.write('What stands out from the graph, participants lost the most of weight when they were moderately active. Those, who were very active, might not only burn fat but also gain muscle mass.')

st.subheader('Age X Weight Change (lbs) X Physical Activity')
st.write('Hypothesis 1: Young people under 30 will have the most significant weight loss.')
st.write('Hypothesis 2: Older people lead the most inactive lifestyle.')
# st.scatter_chart(data = df, x = 'Physical Activity Level', y = 'Age', width = 50, height = 600)
st.scatter_chart(data = df, x = 'Age', y = 'Weight Change (lbs)', color = 'Physical Activity Level', width = 50, height = 600)
st.write('The plot says, that the biggest weight loss has been experienced by 35 - 45 years old. Youngsters under 30 years got the second place, while older people of age 50 - 60 had the least weight loss. Just like in the previous graph, that those, who lost the largest weight, were moderately active. Older people were mostly sedentary or lightly active, so they lost less weight than others.')

st.header('Dataset transformation')

st.write("Let's convert lbs into kilograms.")
dft = df
weightchange = dft['Weight Change (lbs)']
for i in weightchange:
    i/=0.453592
currentweight = dft['Current Weight (lbs)']
for i in currentweight:
    i/=0.453592
finalweight = dft['Final Weight (lbs)']
for i in finalweight:
    i/=0.453592
dft['Weight Change (kg)'] = weightchange
dft['Current Weight (kg)'] = currentweight
dft['Final Weight (kg)'] = finalweight
dft.drop(columns=['Weight Change (lbs)', 'Current Weight (lbs)', 'Final Weight (lbs)'])
st.dataframe(dft[['Weight Change (kg)', 'Current Weight (lbs)', 'Final Weight (kg)']], hide_index=True)
st.write("Let's also add column 'Weight Change (kg) per week' to see the velocity of changing weight.")
dft['Weight Change (kg) per week'] = dft['Weight Change (kg)']/dft['Duration (weeks)']
st.dataframe(dft['Weight Change (kg) per week'], hide_index = True)

st.header('Weight change prediction')
with st.form('form'):
    st.write('Fill in the form:')
    age = st.slider('Enter the age:', step=1, max_value=59, min_value=18)
    gender = st.selectbox('Enter the gender', options=['M', 'F', 'Attack Helicopter'])
    current_weight = st.number_input('Enter current weight (kg)', min_value=0, max_value=300)
    bmr = st.number_input('Enter the BMR:', min_value=0, max_value=4000)
    daily_consumed = st.number_input('Enter the number of calories which are daily consumed', min_value=0, max_value=5000)
    duration = st.number_input('Enter duration of the lifestyle:', min_value=0, max_value = 30)
    physical_activity = st.selectbox('Enter physical activity level:', options=['Sedentary', 'Lightly Active', 'Moderately Active', 'Very Active'])
    
    sent = st.form_submit_button('Compute')

dft = dft.rename(columns={'Current Weight (kg)': 'Current_Weight_kg', 'BMR (Calories)': 'BMR_Calories', 'Daily Calories Consumed': 'Daily_Calories_Consumed', 'Duration (weeks)': 'Duration_weeks', 'Physical Activity Level': 'Physical_Activity_Level'})

if sent:
    request_data = json.dumps({
        'Gender': gender,
        'Physical_Activity_Level': physical_activity,
        'Age': age,
        'Current_Weight_kg': current_weight,
        'BMR_Calories': bmr,
        'Daily_Calories_Consumed': daily_consumed,
        'Duration_weeks': duration,
    })
    response = requests.post(URL.format('weight'), request_data)
    data = json.loads(response.content)
    st.metric(label='Expected Weight Change (kg)', value=f'{data['result']:.2f}')