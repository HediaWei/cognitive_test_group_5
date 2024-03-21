import requests
from bs4 import BeautifulSoup
from IPython.display import display, HTML, clear_output
import random
import time
import pandas as pd
import json
import ipywidgets as widgets
from ipywidgets import Layout, VBox
from jupyter_ui_poll import ui_events


'''
I acknowledge the use of AI tools (ChatGPT.3.5) by OpenAI to help with debugging/ fixing issues related to the ipywidgets module
and to help with making the dictionary of questions that produces each of the cube arrangements
URL: https://chat.openai.com/
'''


#Fixed random seed to ensure the constant 
random.seed(114)

#Source：Moodle：Button demo code.ipynb
event_info = {
    'type': '',
    'description': '',
    'time': -1
}

#Source：Moodle：Button demo code.ipynb
def wait_for_event(timeout=-1, interval=0.001, max_rate=20, allow_interupt=True):    
    start_wait = time.time()

    # set event info to be empty
    # as this is dict we can change entries
    # directly without using
    # the global keyword
    event_info['type'] = ""
    event_info['description'] = ""
    event_info['time'] = -1

    n_proc = int(max_rate*interval)+1
    
    with ui_events() as ui_poll:
        keep_looping = True
        while keep_looping==True:
            # process UI events
            ui_poll(n_proc)

            # end loop if we have waited more than the timeout period
            if (timeout != -1) and (time.time() > start_wait + timeout):
                keep_looping = False
                
            # end loop if event has occured
            if allow_interupt==True and event_info['description']!="":
                keep_looping = False
                # add pause before looping
            # to check events again
            time.sleep(interval)
    
    # return event description after wait ends
    # will be set to empty string '' if no event occured
    return event_info

#Source：Moodle：Button demo code.ipynb
def register_event(btn):
    # display button description in output area
    event_info['type'] = "click"
    event_info['description'] = btn.description
    event_info['time'] = time.time()
    return

#For generateing the random questions
def generate_problem(question_count):
    if question_count <= 8:
        num1 = random.randint(0, 10)
        num2 = random.randint(0, 10)
        num3 = random.randint(0, 10)
    elif 9 <= question_count <= 15:
        num1 = random.randint(11, 50)
        num2 = random.randint(11, 50)
        num3 = random.randint(0, 10)
    else:
        # Handle the case when question_count is outside the specified ranges
        raise ValueError("Invalid question_count")
    operator1 = random.choice(['+', '-'])
    operator2 = random.choice(['+', '-','*'])
    return num1, num2, num3, operator1, operator2

# Function to send data to a Google Form
def send_to_google_form(data_dict, form_url):
    ''' Helper function to upload information to a corresponding google form 
        You are not expected to follow the code within this function!
    '''
    form_id = form_url[34:90]
    view_form_url = f'https://docs.google.com/forms/d/e/{form_id}/viewform'
    post_form_url = f'https://docs.google.com/forms/d/e/{form_id}/formResponse'

    page = requests.get(view_form_url)
    content = BeautifulSoup(page.content, "html.parser").find('script', type='text/javascript')
    content = content.text[27:-1]
    result = json.loads(content)[1][1]
    form_dict = {}
    
    loaded_all = True
    for item in result:
        if item[1] not in data_dict:
            print(f"Form item {item[1]} not found. Data not uploaded.")
            loaded_all = False
            return False
        form_dict[f'entry.{item[4][0][0]}'] = data_dict[item[1]]
    
    post_result = requests.post(post_form_url, data=form_dict)
    return post_result.ok

# Function for retrieving user details if they consent

def get_details():
    name_info = '''Enter your anonymised ID

                To generate an anonymous 4-letter unique user identifier please enter:
                - two letters based on the initials (first and last name) of a childhood friend
                - two letters based on the initials (first and last name) of a favourite actor / actress

                e.g. if your friend was called Charlie Brown and film star was Tom Cruise
                    then your unique identifier would be CBTC'''
    
    display(HTML(name_info))
    #with details_output:
    # input widget
    # display widget
    display(HTML(f"<span style='color:black; font-size: 20px; display: block; text-align: center;'>Unique Anynomous code:(4 letters)</span>"))
    name_input_widget = widgets.Text(description="name", layout=Layout(width='50%', margin='0 auto'))
    display(name_input_widget)
    
    display(HTML(f"<span style='color:black; font-size: 20px; display: block; text-align: center;'>What is your age? </span>"))
    age_input_widget = widgets.Text(description="age", layout=Layout(width='50%', margin='0 auto'))
    display(age_input_widget)
    
    display(HTML(f"<span style='color:black; font-size: 20px; display: block; text-align: center;'>What is your gender?(Male/Female)</span>"))
    gender_input_widget = widgets.Text(description="gender", layout=Layout(width='50%', margin='0 auto'))
    display(gender_input_widget)
    
    display(HTML(f"<span style='color:black; font-size: 20px; display: block; text-align: center;'>Do you drink alcohol before test within 12h (Y/N)?</span>"))
    alcohol_input_widget = widgets.Text(description="alcohol", layout=Layout(width='50%', margin='0 auto'))
    display(alcohol_input_widget)
    
    display(HTML(f"<span style='color:black; font-size: 20px; display: block; text-align: center;'>Do you/ have you ever smoked (Y/N)?</span>"))
    smoking_input_widget = widgets.Text(description="smoking", layout=Layout(width='50%', margin='0 auto'))
    display(smoking_input_widget)
    
    name = name_input_widget.value
    age = age_input_widget.value
    gender = gender_input_widget.value
    alcohol = alcohol_input_widget.value
    smoking = smoking_input_widget.value
    
    return name, age, gender, alcohol, smoking

# Call the function to display the centered input fields


# Display number and operator to give a question
def display_problem(num1, operator1, num2, operator2, num3):
    # Display the problem using HTML-like formatting
    display(HTML(f"<span style='color: red; font-size: 30px;'>{num1}</span>"))
    time.sleep(2)
    clear_output(wait=True)

    display(HTML(f"<span style='color: red; font-size: 30px;'>{operator1}{num2}</span>"))
    time.sleep(2)
    clear_output(wait=True)
    
    display(HTML(f"<span style='color: red; font-size: 30px;'>{operator2}{num3}</span>"))
    time.sleep(1)
    clear_output(wait=True)

#use to confirm user input is int or float
def type_check(value):
    type_value = type(value)
    if type_value == int or type_value==float:
        return value
    else:
        return -100000 #must be wrong

#Colab by group member Qianzhi Sang

# code for consent botton 

def willingness_check(btn1,btn2):
    # we need to set up each button
    # to call the register_event
    # function when clicked
    btn1.on_click(register_event) 
    btn2.on_click(register_event) 

    myhtml1 = HTML("<span style='font-size: 20px;display: block; text-align: center;'> Would you like to enter your details to be used for research purposes? </span>")
    display(myhtml1)
    
    buttons_box = widgets.HBox([btn1, btn2])
    # Center the buttons horizontally, under help with chatgpt.
    centered_buttons = widgets.Box([buttons_box], layout=widgets.Layout(justify_content='center'))
    display(centered_buttons)
    
    result = wait_for_event(timeout=60)
    clear_output()

    if result['description']!="":
        print(f"User clicked: {result['description']}")
        return(result['description'])
    else:
        print("User did not click in time")
    

#Source:Moodle Week 6, Using_buttons_and_text_input_fix.ipynb
def text_input(prompt=None):
    text_input = widgets.Text(description=prompt, style= {'description_width': 'initial'})
    import warnings
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    text_input.on_submit(register_text_input_event)
    display(text_input)
    event = wait_for_event(timeout=-1)
    text_input.disabled = True
    return event['description']

#Source:Moodle Week 6, Using_buttons_and_text_input_fix.ipynb
def register_text_input_event(text_input):
    event_info['type'] = "text_entry"
    event_info['description'] = text_input.value
    event_info['time'] = time.time()
    return

# Main calculation test
def main():
    correct_answers = 0
    score = 0
    total_time = 0
    num_problems = 15  # You can change the number of problems

    display(HTML(f"<span style='color: black; font-size: 20px;'>Math Calculation Ability Test: Here is the example for your further step calculation, if you see '2+3*2' it would be (2+3)*2</span>"))

    consent_info = '''Please read:

                      We wish to record your response data to an anonymised public data repository. 
                      Your data will be used for educational teaching purposes practising data analysis and visualisation.

                      please click yes if you are consent to shareing your data toward us, If not, please just click no.'''
    display(HTML(consent_info))
    
    name,age,gender,alcohol,smoking = get_details()

    #The two buttons
    btn1 = widgets.Button(description="Yes")
    btn2 = widgets.Button(description="No")

    if_consent = willingness_check(btn1,btn2)
    
    if if_consent == 'Yes':
        #Time list that store the time spend each time
        time_list_set1 = []
        time_list_set2 = []

        for i in range(1, num_problems + 1):
            num1, num2, num3, operator1, operator2 = generate_problem(i)

            display(HTML(f"<span style='color: black; font-size: 20px;'>Get ready for problem {i}...</span>"))
            time.sleep(2)
            clear_output(wait=True)

            # Display the problem for 2 seconds
            display_problem(num1, operator1, num2, operator2, num3 )

            # Record start time
            start_time = time.time()
        
            # Ask the user to solve the problem
            display(HTML(f"<span style='color: black; font-size: 20px;'>What's the answer? </span>"))
            

            #Use the Text_input_function
            user_input = text_input(prompt='The answer is:')
            user_answer = type_check(user_input) 
            #now user input must be int/float to prevent bug, if not,the answer is a 100% wrong answer to punish
        
            # Record end time
            end_time = time.time()
            # Calculate the time spent on the current question
            time_spent = end_time - start_time
        
            if 1 <= i <= 8:
                time_list_set1.append(time_spent)
            elif 9 <= i <= 15:
                time_list_set2.append(time_spent)
        
            total_time += time_spent
        
            # Calculate the correct answer
            if operator1 == '+' and operator2 == '+':
                correct_answer = num1 + num2 + num3
            elif operator1 == '+' and operator2 == '-':
                correct_answer = num1 + num2 - num3
            elif operator1 == '+' and operator2 == '*':
                correct_answer = (num1 + num2 )* num3
            elif operator1 == '-' and operator2 == '+':
                correct_answer = num1 - num2 + num3
            elif operator1 == '-' and operator2 == '-':
                correct_answer = num1 - num2 - num3
            elif operator1 == '-' and operator2 == '*':
                correct_answer = (num1 - num2) * num3

            # Check if the user's answer is correct
            if user_answer == correct_answer:
                print(f"Correct! You earned 1 point. Time: {time_spent:.2f} seconds\n")
                correct_answers += 1
                score += 1
            else:
                print(f"Incorrect. The correct answer is {correct_answer}. No point earned. Time: {time_spent:.2f} seconds\n")

    # Calculate the average time spent
    average_time_set1 = sum(time_list_set1) / len(time_list_set1) if time_list_set1 else 0
    average_time_set2 = sum(time_list_set2) / len(time_list_set2) if time_list_set2 else 0
        
    # Display the results using HTML
    display(HTML(f"<p style='color: blue; font-size: 18px;display: block; text-align: center;'>You got {correct_answers} out of {num_problems} problems correct.</p>"))
    display(HTML(f"<p style='color: blue; font-size: 18px;display: block; text-align: center;'>Your total score is {score}.</p>"))
    display(HTML(f"<p style='color: blue; font-size: 18px;display: block; text-align: center;'>Total time spent on calculation: {total_time:.2f} seconds.</p>"))
    display(HTML(f"<p style='color: blue; font-size: 18px;display: block; text-align: center;'>Average time spent for questions 1-8: {average_time_set1:.2f} seconds.</p>"))
    display(HTML(f"<p style='color: blue; font-size: 18px;display: block; text-align: center;'>Average time spent for questions 9-15: {average_time_set2:.2f} seconds.</p>"))
    
    myhtml1 = HTML("<span style='font-size: 20px;'> Would you like to enter your details to be used for research purposes? </span>")
    display(myhtml1)

    panel = widgets.HBox([btn1, btn2])
    display(panel)

    result = wait_for_event(timeout=-1)
    clear_output()

    #indentation 
    if result['description']!="":
        print(f"User clicked: {result['description']}")
    else:
        print("User did not click in time")

    # Dictionaries for user information and test results
    data_dict1 = {'Name': name, 'Age': age, 'Gender': gender, 'Alcohol': alcohol, 'Smoking': smoking}
    data_dict2 = {'Average_time_easy': average_time_set1, 
                  'Average_time_hard': average_time_set2, 
                  'Total_time': total_time, 
                  'Final_grade': score,
                  'q1': time_list_set1[0],
                  'q2': time_list_set1[1],
                  'q3': time_list_set1[2],
                  'q4': time_list_set1[3],
                  'q5': time_list_set1[4],
                  'q6': time_list_set1[5],
                  'q7': time_list_set1[6],
                  'q8': time_list_set1[7],
                  'q9': time_list_set2[0],
                  'q10': time_list_set2[1],
                  'q11': time_list_set2[2],
                  'q12': time_list_set2[3],
                  'q13': time_list_set2[4],
                  'q14':time_list_set2[5],
                  'q15':time_list_set2[6]}

    # Create a new dictionary by copying data_dict1 and updating it with data_dict2
    new_data_dict = data_dict1.copy()
    new_data_dict.update(data_dict2)

    # Send data to Google Form
    form_url = 'https://docs.google.com/forms/d/e/1FAIpQLSdtOV3JVnW1jtoSxjP8HsBm9lJUupjaJ3ck3Fem95XEkRm28g/viewform?usp=sf_link'
    if_success = send_to_google_form(new_data_dict, form_url)
    return if_success

main()