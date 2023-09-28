import openai
import streamlit as st

openai.api_key = st.secrets['openai_key']

centered_image = f"<center><img src='Untitled design (10).jpg' width='300'></center>"
st.markdown(centered_image, unsafe_allow_html=True)

st.title('Personal AI Health Coach by Ethan Castro')

# Get user input
sex_choice = st.selectbox('What is your sex?', ['male', 'female'])
if sex_choice == 'male':
    sex = -5
else:
    sex = 161
age = st.number_input('What is your age?', min_value=1, max_value=100)
weight = st.number_input('What is your weight (in lbs)?', min_value=1)
height = st.number_input('What is your height (inches)?', min_value=1)
goal = st.text_input('What is your goal (can be anything health related)?')
activity = st.number_input('Rate your activity level from sedentary (1) to very active (10)?', min_value=1, max_value=10)

# Convert the 1-10 activity scale to 1.2-1.9 scale
activity = 1.2 + (activity - 1) * .0778
bmi = round(weight / (height * height) * 703)
bmr = round(10 * weight + 6.25 * height - 5 * age - sex)
tdee = round(bmr * activity)



if st.button('Get advice'):
    # Generate AI response

    prompt_template = (
    "This is the script you repeat first 'I am an AI health coach, this is not medical advice. Ok so, you are {age} years old, weigh {weight} lbs, are {height} inches tall, and your goal is {goal}. Here's your BMI {bmi}, TDEE or total daily energy expenditure {tdee} calories, Repeat everything before and input the proper values' Then provide advice for the goal, a brief easy-to-follow detailed exercise routine, a philosophical motivational quote, a piece of nutrition psychology advice, healthy snacks in list format, and words for consistency. "
     )
    
    user_data = {
        'age': age,  # Example age
        'weight': weight,  # Example weight in lbs
        'height': height,  # Example height in inches
        'goal': goal,  # Example goal
        'bmi': bmi,  # Example BMI value
        'tdee': tdee,  # Example TDEE value
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
    
# You can then format this prompt with the specific details:

    prompt = prompt_template.format(**user_data)
    print(response)  # Debug print statement
    
    
    if response.choices:
            print(response.choices[0])  # Debug print statement
            print("Your BMR is:", bmr)
    
    if 'text' in response.choices[0]:
                # Display AI response
                st.write(response.choices[0].text.strip())
    

  
