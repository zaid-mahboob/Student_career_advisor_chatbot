import streamlit as st
import os
import openai
from dotenv import load_dotenv, find_dotenv
from streamlit_chat import message
_ = load_dotenv(find_dotenv())  # read local .env file


# 1st. You need to ask the student his academic background. 
# 2nd. You need to ask the student his interests try to keep it relevant to the academic backround and ask student if he planning to switch the field. if his interests are not relvevant to his field its fine no issue with it./\
# 3rd. Ask student what skillset does he posses. Try to ask him to highlight those which are relevant to his interests./
# 4th. Based on his academic background, interests, skillset. Suggest him what he needs to do next what skillset does he or she needs to strengthen. Tell him all the emerging fields as well related to his skillset and interests./
# 5th. Ask him where does he see himself after 10 years and based on that provide him a roadmap and a list of skills he should be learning./

openai.api_key = os.environ['OPENAI_API_KEY']

st.set_page_config(page_title='Smart Student Career Consultant',
                   page_icon=":robot_face:",
                   layout='wide',
                   initial_sidebar_state='expanded')

# Initialize your model
def get_model_response(messages, model="gpt-3.5-turbo", temperature=0, max_tokens=500):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return response.choices[0].message["content"]

def update_chat(messages, role, content):
    messages.append({"role": role, "content": content})
    return messages

delimiter = "####"
system_message = f"""
You are a student career consultant who has seen the revolution in all the industries and provided consultation to more than 10000 people./
Here you are to provide consultation to students. You may use some companies information which you have and provide bext path to the student through which he can learn and grow.
You will be provided with student queries such as a student is interested in something and he wants to know what jobs are there which demand that skillset./
On a student wants to apply for a particular job and wants to know what are the job description of that job. \
The customer service query will be delimited with \
{delimiter} characters.

You need to be interactive, ask questions and let student answer your questions./

Lastly, if he has anyother questions answer them and let student clear all his queries.
You are to only provide authentic information to the student or user. /
If a student asks about anything else please say that <you dont have expertise in it. And dont mention that you are a language model just say you are a student consultant>.
"""
messages = [
    {'role': 'system',
     'content': system_message},
]



st.title("🤖 Student Career Consultant By Zaid Mahboob")


if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []


def get_text():
    input_text = st.text_input("You: ","Hello, how are you?", key="input")
    print(type (input_text))
    print (input_text)
    openai_input_text = f"{delimiter}{input_text}{delimiter}"
    update_chat(messages, "user", openai_input_text)
    return input_text 


user_input = get_text()

if user_input:
    output = get_model_response(messages)
    messages = update_chat(messages, "assistant", output)
    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)

if st.session_state['generated']:

    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
