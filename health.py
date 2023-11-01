import openai
import streamlit as st

openai.api_key = st.secrets['openai_key']

# Set the page layout
st.set_page_config(
    page_title="AI Health Coach",
    layout="wide",
)

# Styling
st.markdown(
    """
    <style>
        .title {
            color: #3b5998;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Title
st.markdown("<h1 class='title'>Personal AI Health Coach by Ethan Castro</h1>", unsafe_allow_html=True)

# User inputs
st.sidebar.header('User Inputs')
sex_choice = st.sidebar.selectbox('What is your sex?', ['male', 'female'], help="Select your biological sex.")
if sex_choice == 'male':
    sex = -5
else:
    sex = 161
age = st.sidebar.number_input('What is your age?', min_value=1, max_value=100)
weight = st.sidebar.number_input('What is your weight (in lbs)?', min_value=1)
height = st.sidebar.number_input('What is your height (in inches)?', min_value=1)
goal = st.sidebar.text_input('What is your goal (can be anything health related)?')
activity = st.sidebar.number_input('Rate your activity level from sedentary (1) to very active (10)?', min_value=1, max_value=10, help="1 is sedentary and 10 is very active.")

# Calculations
activity = 1.2 + (activity - 1) * .0778
bmi = round(weight / (height * height) * 703)
bmr = round(10 * weight + 6.25 * height - 5 * age - sex)
tdee = round(bmr * activity)

if st.sidebar.button('Get advice'):
    # Generate AI response
    prompt_template = (
        "I am an AI health coach, this is not medical advice. Ok so, you are {age} years old, weigh {weight} lbs, "
        "are {height} inches tall, and your goal is {goal}. Here's your BMI {bmi}, TDEE or total daily energy expenditure {tdee} calories. "
        "Repeat everything before and input the proper values. Provide advice for the goal, a brief easy-to-follow detailed exercise routine, "
        "a philosophical motivational quote, a piece of nutrition psychology advice, healthy snacks in list format, and words for consistency."
    )
    
    user_data = {
        'age': age,
        'weight': weight,
        'height': height,
        'goal': goal,
        'bmi': bmi,
        'tdee': tdee,
        'advice': goal
    }
    
    response = openai.Completion.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompt_template.format(**user_data),
        temperature=.5,
        max_tokens=500,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    
    if 'text' in response.choices[0]:
        # Display AI response
        st.write(response.choices[0].text.strip())

