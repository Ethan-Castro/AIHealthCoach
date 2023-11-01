import openai
import streamlit as st

# Set API Key
openai.api_key = st.secrets['openai_key']

# Set page config
st.set_page_config(
    page_title="AI Health Coach",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Styles
st.markdown(
    """
    <style>
        .reportview-container {
            background: #FFFFFF;
        }
        .title {
            color: #3b5998;
            font-size: 36px;
        }
        .section-header {
            color: #555;
            font-size: 24px;
            margin-bottom: 10px;
        }
        .sidebar .sidebar-content {
            background: #FFFFFF;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# App Header
st.markdown("<h1 class='title'>AI Health Coach by Ethan Castro</h1>", unsafe_allow_html=True)

# User Inputs in Sidebar
with st.sidebar:
    st.markdown("<h2 class='section-header'>Your Details</h2>", unsafe_allow_html=True)

    sex_choice = st.selectbox('Sex:', ['Male', 'Female'])
    sex = -5 if sex_choice == 'Male' else 161
    age = st.number_input('Age:', min_value=1, max_value=100)
    weight = st.number_input('Weight (lbs):', min_value=1)
    height = st.number_input('Height (inches):', min_value=1)
    goal = st.text_input('Your Health Goal:')
    activity = st.slider('Activity Level:', min_value=1, max_value=10, value=5, help="1 = Sedentary, 10 = Very Active")

# Calculations
activity_scale = 1.2 + (activity - 1) * .0778
bmi = round(weight / (height * height) * 703)
bmr = round(10 * weight + 6.25 * height - 5 * age - sex)
tdee = round(bmr * activity_scale)

# Display Calculations & Get Advice Button
st.markdown("<h2 class='section-header'>Your Metrics</h2>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    st.subheader("BMI:")
    st.write(bmi)
with col2:
    st.subheader("BMR:")
    st.write(bmr)
with col3:
    st.subheader("TDEE (calories per day):")
    st.write(tdee)

if st.button('Get Health Advice'):
    # Generate AI response
    prompt_template = (
        "I am an AI health coach, and this is not medical advice. You are {age} years old, weigh {weight} lbs, "
        "are {height} inches tall, and your goal is {goal}. Your BMI is {bmi}, and your TDEE is {tdee} calories. "
        "Provide advice for the goal, a brief exercise routine, a motivational quote, nutrition psychology advice, "
        "healthy snacks, and words for consistency."
    )

    user_data = {
        'age': age,
        'weight': weight,
        'height': height,
        'goal': goal,
        'bmi': bmi,
        'tdee': tdee,
    }

    response = openai.Completion.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompt_template.format(**user_data),
        temperature=.5,
        max_tokens=505,
    )
    
    if response.choices:
        st.markdown("<h2 class='section-header'>AI Generated Health Advice</h2>", unsafe_allow_html=True)
        st.write(response.choices[0].text.strip())

# Footer
st.markdown(
    """
    <footer>
        <p>Made with ❤️ by Ethan Castro</p>
    </footer>
    """,
    unsafe_allow_html=True
)
