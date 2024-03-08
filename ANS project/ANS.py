from IPython.display import display,HTML,Image,clear_output
import time
import os
import re
import random as rd
import pandas as pd
import ipywidgets as widgets
from jupyter_ui_poll import ui_events
import requests
from bs4 import BeautifulSoup
import json

'''I acknowlage the use of AI tools(ChatGPT.3.5) by OpenAI
URL:https://chat.openai.com/c/b08d946c-eb37-4dd9-b302-2df65b8e8bbf
for some background researches on ANS test knowledge and fixing some bugs
related to packages ipywidgets which is about the relationship of time of button
and input,mainly in the function willingness_checker() and usage of ConnectionError
at ANS_test() function'''

empty_frame = Image('0-0.png',width=600)

#Source:Moodle：Button demo code.ipynb
event_info = {
    'type': '',
    'description': '',
    'time': -1
}

#Our main way is storing file and answer in a dictionary
def file_parser(directory):
    answer_dict = {} #Use dictonary to store answer each time
    folder_open = os.listdir(directory) #Use os package for list of directory
    for dirs in folder_open:
        if dirs == '.DS_Store': #Some hidden file may affect our selection
            continue
        else:
            nums = re.match(r'(\d+)-(\d+)\.png', dirs)
            #Regular expression for extracting the numbers
            #Learned Regex in Biol0053
            if int(nums.group(1)) > int(nums.group(2)):
                answer_dict[dirs] = 'left'
            if int(nums.group(2)) > int(nums.group(1)): #The pictures had already named by number of spots
                answer_dict[dirs] = 'right'
    return answer_dict

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

# this function lets buttons
# register events when clicked

#Source：Moodle：Button demo code.ipynb
def button_inner_function(btn):
    # display button description in output area
    event_info['type'] = "click"
    event_info['description'] = btn.description
    event_info['time'] = time.time()
    return

#Write a function for code of selecting left or right
def button_selection(timeout):
    #The time that stop the user from answering:
    

    button_left = widgets.Button(description='left')
    button_right = widgets.Button(description='right')
    
    #These button will return an "left" or "right"
    button_left.on_click(button_inner_function)
    button_right.on_click(button_inner_function)

     #The panel that the result shows
    panel = widgets.HBox([button_left,button_right])
    display(panel)

    selection = wait_for_event(timeout=timeout)
    return selection['description']

#Then we are now able to make candidates to use the button to input results.

def individual_test(figure_dir):
    #Displaying the figures
    Fig = Image(f'pic_pac/{figure_dir}',width=600)
    display(Fig)
    time.sleep(0.75) #0.75s display of picture
    clear_output(wait=False)
    display(empty_frame)
    mark = 0
    
    #output is store as a dictionary as well
    output_dict = {}

    #Looping part
    time_1 = time.time() #Initial time
    candidate_answer = button_selection(timeout = 3)
    time_2 = time.time() #Final time

    #Checking if the answer correct
    if candidate_answer == answer_dict[figure_dir]:
        mark = 1
        print("Correct")
    elif candidate_answer == '':
        print('Times up! Ready for the next question')
    else:
        print("Oops You are incorrect")

    output_dict['mark'] = mark
    output_dict['responce_time'] = time_2 - time_1
    output_dict['candidate_answer'] = candidate_answer
    time.sleep(1.5) #1.5 second between question
    clear_output(wait=False)
    return output_dict

#This is the aiming format of data
'''overall_data = {'Name':[],'Age':[],'Total_marks':[],'candidate_answers_by_question':[],
                    'reactiontime_by_question':[],
                    'left_by_question':[],'right_by_question':[],
                    'correctness':[]}'''

#function that packs multiple tests together "OLD VERSION"
'''def multiple_tests(answer_dict,overall_data):
    question_number  = 0
    Marks = 0 #Numbers of correct answers
    for keys in answer_dict:
        individual_dict = individual_test(keys)
        Marks = Marks + individual_dict['mark']
        question_number = question_number + 1
        print(f'Now is question number {question_number}')

         #The module to record the left and right number for future scientific studies
        nums = re.match(r'(\d+)-(\d+)\.png', keys)

        #Storing data of each questions
        overall_data['left_by_question'].append(int(nums.group(1)))
        overall_data['right_by_question'].append(int(nums.group(2)))
        overall_data['reactiontime_by_question'].append(individual_dict['responce_time'])
        overall_data['candidate_answers_by_question'].append(individual_dict['candidate_answer'])
        overall_data['Mark_by_question'].append(individual_dict['mark'])
    overall_data['Total_marks'] = Marks
    print(f"Your Marks are {Marks}")

    return overall_data #output an assigned dictionary for uploading'''

#This code had then been rewrited to satisfying the new needs
def multiple_tests(answer_dict,overall_data,Cycle=4):
    question_number  = 0
    Marks = 0 #Numbers of correct answers
    answer_list = list(answer_dict.keys()) #Dict have no sequence , so we have to make a list
    cyc = 1
    for i in range(Cycle): #Recycle the answer dict
        rd.seed(cyc) #The seed are 1,2,3,4 for 4 cycle which is acturally fixed
        print(f'Now is the {cyc} th cycle')
        rd.shuffle(answer_list)
        for keys in answer_list:
            individual_dict = individual_test(keys)
            Marks = Marks + individual_dict['mark']
            question_number = question_number + 1
            print(f'Now is question number {question_number}')

            #The module to record the left and right number for future scientific studies
            nums = re.match(r'(\d+)-(\d+)\.png', keys)

            #Storing data of each questions
            overall_data['left_by_question'].append(int(nums.group(1)))
            overall_data['right_by_question'].append(int(nums.group(2)))
            overall_data['reactiontime_by_question'].append(individual_dict['responce_time'])
            overall_data['candidate_answers_by_question'].append(individual_dict['candidate_answer'])
            overall_data['Mark_by_question'].append(individual_dict['mark'])
            cyc = cyc+1
    
    overall_data['Total_marks'] = Marks
    print(f"Your Marks are {Marks}")

    return overall_data #output an assigned dictionary for uploading

def button_start(): #A button to control when  to start
    button_start = widgets.Button(description='Start')
    button_start.on_click(button_inner_function)

    panel = widgets.HBox((button_start,))
    display(panel)

    #By repeating trying, if selection == 'Start': must return False instead of true
    selection = wait_for_event(timeout = 100)
    if selection == 'Start':
        return False
    else:
        return True

def button_yn(timeout):
    #The time that stop the user from answering:
    
    button_left = widgets.Button(description='Yes')
    button_right = widgets.Button(description='No')
    
    button_left.on_click(button_inner_function)
    button_right.on_click(button_inner_function)

     #The panel that the result shows
    panel = widgets.HBox([button_left,button_right])
    display(panel)

    selection = wait_for_event(timeout=timeout)
    return selection['description']

#Write a function to check the willingness of the Candidates
#The use of widget.text is to avoid the use of input() which generate bugs here
#Knowledges are by reading URL: https://ipywidgets.readthedocs.io/en/latest/how-to/index.html
#Which I learned how to use the .value characsitic to find the input, bypassing input()

def Willingness_checker(Overall_data):
    print(name_info)
    name_widget = widgets.Text(placeholder='ID')
    display(name_widget)
    #name = name_widget.value
    #It will not working here as it read the value immediately
    #We have to place it after the button

    print("Please enter your following details:")
    age_widget = widgets.Text(placeholder='Age')
    display(age_widget)
    #age = age_widget.value
    
    #Learned the usage of widget.Text by combining website sources and ChatGPT which
    #had show me an example of widget use
    gender_widget = widgets.Text(placeholder = 'Gender (F/M)')
    display(gender_widget)

    occ_widget = widgets.Text(placeholder = 'Occupation')
    display(occ_widget)

    smoc_widget = widgets.Text(placeholder = 'Are you smoking?(Yes/No)')
    display(smoc_widget)

    alc_widget = widgets.Text(placeholder = 'Have you drank alcohol with in 12 hours?(Yes/No)')
    display(alc_widget)

    willingness = button_yn(-1) #use -1 as class example
    
    if willingness == 'Yes':
        #To allow the input of value
        name = name_widget.value
        age = age_widget.value
        gender = gender_widget.value
        occ = occ_widget.value
        smoc=smoc_widget.value
        alc = alc_widget.value
        Overall_data['Name'] = name
        Overall_data['Age'] = age
        Overall_data['Gender'] = gender
        Overall_data['Occupation'] = occ
        Overall_data['Smoking']=smoc
        Overall_data['Alcohol_consumption']= alc
        print(Overall_data)
        return True

    else:
        print('data delected')
        return False

#Function that saving the test results to local enviorments
def saving_to_discs(single_results,if_csv,if_append):
    if if_append == False:
        single_results_local = pd.DataFrame(single_results)
        if if_csv == True:
            single_results_local.to_csv()
    if if_append == True:
        #before if append,we need to have a single_result_local
        single_results_new = pd.DataFrame(single_results)
        single_results_local = pd.concat([single_results_local,single_results_new],
                                         axis ='rows' ,ignore_index=True)
        

#Source: Moodle: 3-Reaction_Timer.ipynb
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
        
def Main():
    answer_dict = file_parser("pic_pac")
    # dictionary that store everything
    overall_data = {'Name':[],'Age':[],'Total_marks':[],'candidate_answers_by_question':[],
                    'reactiontime_by_question':[],'Mark_by_question':[],
                    'left_by_question':[],'right_by_question':[],
                    }
    while True: #While true so we can wait the button
        if_start = button_start()
        if if_start == True:
            print(Consent_info)
            willingness = Willingness_checker(overall_data)
            if willingness == True:
                clear_output(wait=False)
                print('Start in 3 seconds')
                time.sleep(3)
                single_results = multiple_tests(answer_dict, overall_data)
                print('Test_overed')
                clear_output(wait=False)
                return single_results
            else:
                print('We would not save any data online')
                return overall_data #Empty in name to be selected
        else:
            print("Your session has expired")
            break


#Source: Moodle BIOS0030 Cognitive Test Project - Notes and To do list
Consent_info = '''
Please read:

We wish to record your response data to an anonymised public data repository.
Your data will be used for educational teaching purposes practising data analysis and visualisation.

please click yes if you are consent to shareing your data toward us, If not, please just click no.
'''

#Source: Moodle BIOS0030 Cognitive Test Project - Notes and To do list
name_info = '''
Enter your anonymised ID

To generate an anonymous 4-letter unique user identifier please enter:
- two letters based on the initials (first and last name) of a childhood friend
- two letters based on the initials (first and last name) of a favourite actor / actress

e.g. if your friend was called Charlie Brown and film star was Tom Cruise
     then your unique identifier would be CBTC'''

def Ans_tests(answer_dict):
    #Main code
    answer_dict = answer_dict
    test_result= Main()
    Google_url = 'https://docs.google.com/forms/d/e/1FAIpQLSf9m1KxQ3YdafOb8bOxlrW6v_xVSwi1pgWkPVrS8EsnCl9eng/viewform?usp=sf_link'

    #If the name is not shared, we can know they rejected to use data
    if test_result['Name'] != []:
        successfulness = send_to_google_form(test_result, Google_url)
        if successfulness == True:
            print("Thank you for contributing in the test, Have a good day")
        elif ConnectionError: #Not working,may be due to sequence of error
            print('''Sorry for poor internet connection,we could
                not submit your data,could yould help us do it again?''')
        else:
            print('an unknown error have been occured,data had failed to be uploaded')
    else:
        print("Thank you for participating in the test, Have a good day")


answer_dict = file_parser("pic_pac")
Ans_tests(answer_dict)
