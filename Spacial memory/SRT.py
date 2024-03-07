import matplotlib.pyplot as plt
import numpy as np
import time
import random
from IPython.display import display, Image, clear_output, HTML
import ipywidgets as widgets
import requests
from bs4 import BeautifulSoup
import json
from jupyter_ui_poll import ui_events

'''
I acknowledge the use of AI tools (ChatGPT.3.5) by OpenAI to help with debugging/ fixing issues related to the ipywidgets module
and to help with making the dictionary of questions that produces each of the cube arrangements
URL: https://chat.openai.com/
'''

#function to send data retrieved at end of test to google form 
#function code taken from Reaction_Timer.ipynb
def send_to_google_form(data_dict, form_url):
    form_id = form_url[34:90]
    view_form_url = f'https://docs.google.com/forms/d/e/{form_id}/viewform'
    post_form_url = f'https://docs.google.com/forms/d/e/{form_id}/formResponse'

    page = requests.get(view_form_url)
    content = BeautifulSoup(page.content, "html.parser").find('script', type='text/javascript')
    content = content.text[27:-1]
    result = json.loads(content)[1][1]
    form_dict = {}

    loaded_all = True
    if result is None:
        print("Error: Result is None")
        return False

    for item in result:
        if item[1] not in data_dict:
            print(f"Form item {item[1]} not found. Data not uploaded.")
            loaded_all = False
            return False
        form_dict[f'entry.{item[4][0][0]}'] = data_dict[item[1]]

    post_result = requests.post(post_form_url, data=form_dict)
    return post_result.ok

#dictionary containing all game questions
game_qs = {
    "question_1": { #one level of dictionary for each question
        "correct": { #the next level of dictionary assigns each variable that will be inputted into draw_cubes function
            "cubes": np.full((5, 5, 5), ''), #defines 5x5x5 string array with entries set to ''
            "operations": [ #'operations' contains the color codes for each 3D array
                ((slice(0,4), 0, 0), 'r'),
                ((3, slice(1,3), 0), 'g'),
                ((slice(1,3), slice(1,3), slice(0,2)), 'b'),
                ((1, 2, 2), 'y')
            ]
        },
        "incorrect": { #contains cube array for the cubes that do not match the question
            "cubes": np.full((5, 5, 5), ''),
            "operations": [
                ((slice(0,4), 0, 0), 'r'),
                ((3, slice(1,4), 0), 'g'),
                ((slice(1,3), slice(1,3), slice(0,2)), 'b'),
                ((1, 2, slice(2,3)), 'y')
            ]
        },
        "view": ["xy", "-yz", "-xz", "-xy"] #a list of different views that each possible answer will take
    },
    "question_2": {
        "correct": {
            "cubes": np.full((5, 5, 5), ''),
            "operations": [
                ((slice(0,3), 2, 0), 'r'),
                ((slice(0,6), 3, 0), 'g')
            ]
        },
        "incorrect": {
            "cubes": np.full((5, 5, 5), ''),
            "operations": [
                ((slice(0,4), 2, slice(0,2)), 'r'),
                ((slice(0,6), 3, 0), 'g')
            ]
        },
        "view": ["xy", "-xz", "xz", "-yz"]
    },
    "question_3": {
        "correct": {
            "cubes": np.full((5,5,5),''),
            "operations":[
                ((3,3,slice(0,4)), 'r'),
                ((3,2,slice(0,3)), 'y'),
                ((2,slice(2,4),0), 'b')
            ]
        },
        "incorrect": {
            "cubes": np.full((5,5,5), ''),
            "operations":[
                ((3,3,slice(0,3)), 'r'),
                ((3,2,slice(0,4)), 'y'),
                ((2,slice(2,4),0), 'b')
            ]
        },
        "view": ["xz", "-yz", "xy", "-xz"]
    },
    "question_4": {
        "correct": {
            "cubes": np.full((5,5,5),''),
            "operations":[
                ((3, 1, slice(0, 1)), 'r'),
                ((slice(2, 4), slice(3, 5), slice(0, 2)), 'g'),
                ((slice(2, 4), slice(2, 6), 0), 'b')
            ]
        },
        "incorrect": {
            "cubes": np.full((5,5,5),''),
            "operations":[
                ((3, 0, slice(0, 4)), 'r'),
                ((slice(2, 4), slice(3, 5), slice(0, 2)), 'g'),
                ((slice(2, 4), slice(2, 6), 0), 'b')
            ]
        },
        "view": ["yz", "xy", "-xz", "-xy"]
    },
    "question_5":{
        "correct": {
            "cubes": np.full((5,5,5), ''),
            "operations":[
                ((2, 2, slice(0,4)), 'g'),
                ((2, slice(3,5),0), 'b')
            ]
        },
        "incorrect":{
            "cubes": np.full((5,5,5),''),
            "operations":[
                ((2, slice(1,3), slice(0,4)), 'g'),
                ((2, slice(3,5),0), 'b')
            ]
        },
        "view": ["-yz", "xz", "-xy", "yz"]
    },
    "question_6":{
        "correct":{
            "cubes": np.full((5,5,5), ''),
            "operations":[
                ((2, 0, 0), 'r'),
                ((1, slice(0, 2), 0), 'g'),
                ((slice(0, 2), 0, 0), 'b')
            ]
        },
        "incorrect":{
            "cubes": np.full((5,5,5),''),
            "operations":[
                ((slice(2,4), 0, 0), 'r'),
                ((1, slice(0, 2), 0), 'g'),
                ((slice(0, 2), 0, 0), 'b')
            ]
        },
        "view": ["-xy", "-yz", "xy", "xz"]
    },
    "question_7":{
        "correct":{
            "cubes": np.full((5,5,5),''),
            "operations":[
                ((slice(0,4), slice(1,4), 0), 'r'),
                ((slice(1,3), slice(2,3), 1), 'g'),
                ((2, 2, 2), 'y')
            ]
        },
        "incorrect":{
            "cubes": np.full((5,5,5), ''),
            "operations":[
                ((slice(0,4), slice(1,4), 0), 'y'),
                ((slice(1,3), slice(2,3), 1), 'r'),
                ((2, 2, 2), 'g')
            ]
        },
        "view": ["-xy", "-yz", "-yz", "xz"]
    },
    "question_8":{
        "correct":{
            "cubes": np.full((5,5,5),''),
            "operations":[
                ((3,3,slice(0,4)), 'g'),
                ((3,4,slice(0,4)), 'r'),
                ((4,slice(0,5), 0), 'b')
            ]
        },
        "incorrect":{
            "cubes": np.full((5,5,5), ''),
            "operations":[
                ((3,3,slice(0,4)), 'r'),
                ((3,4,slice(0,4)), 'g'),
                ((4,slice(0,4), 0), 'b')
            ]
        },
        "view": ["-xy", "-xz", "-yz", "yz"]
    },
    "question_9":{
        "correct":{
            "cubes": np.full((5,5,5),''),
            "operations":[
                ((3,slice(1,3),slice(0,2)), 'g'),
                ((2,slice(1,3),slice(0,3)), 'r'),
                ((slice(2,4),0, 0), 'b'),
                ((4, slice(0,3), 0), 'y')
            ]
        },
        "incorrect":{
            "cubes": np.full((5,5,5), ''),
            "operations":[
                ((3,slice(1,3),slice(0,3)), 'g'),
                ((2,slice(1,3),slice(0,2)), 'r'),
                ((slice(2,4),0, 0), 'y'),
                ((4, slice(0,3), 0), 'b')
            ]
        },
        "view": ["-xy", "-xz", "yz", "-yz"]
    },
    "question_10":{
         "correct":{
            "cubes": np.full((5,5,5),''),
            "operations":[
                ((slice(1,3),slice(1,3),slice(0,2)), 'g'),
                ((slice(1,3),slice(1,3),slice(0,1)), 'r'),
                ((1,0, 0), 'y'),
                ((3, 2, 0), 'b')
            ]
        },
        "incorrect":{
            "cubes": np.full((5,5,5), ''),
            "operations":[
                ((slice(1,3),slice(1,3),slice(0,2)), 'r'),
                ((slice(1,3),slice(1,3),slice(0,1)), 'g'),
                ((1,0, 0), 'b'),
                ((3, 2, 0), 'y')
            ]
        },
        "view": ["xy", "-xz", "yz", "xz"]
    },
    "question_11":{
         "correct":{
            "cubes": np.full((5,5,5),''),
            "operations":[
                ((2, 1, 0), 'g'),
                ((2, slice(1, 4), 1), 'r'),
                ((3 ,3, 1), 'y'),
            ]
        },
        "incorrect":{
            "cubes": np.full((5,5,5), ''),
            "operations":[
                ((slice(1,2), 1, 0), 'y'),
                ((2, slice(1, 4), 1), 'r'),
                ((3 ,3, 1), 'g'),
            ]
        },
        "view": ["-xz", "yz", "xy", "xz"]
    },
    "question_12":{
         "correct":{
            "cubes": np.full((5,5,5),''),
            "operations":[
                ((2, 3, slice(0,2)), 'r'),
                ((3, slice(2, 4), 0), 'b'),
                ((4 ,3, slice(0,2)), 'y'),
            ]
        },
        "incorrect":{
            "cubes": np.full((5,5,5), ''),
            "operations":[
                ((2, 3, slice(0,1)), 'r'),
                ((3, slice(1, 4), 0), 'b'),
                ((4 ,3, slice(0,2)), 'y'),
            ]
        },
        "view": ["xz", "-yz", "-xy", "yz"]
    },
    "question_13":{
         "correct":{
            "cubes": np.full((5,5,5),''),
            "operations":[
                ((1, slice(0,3), 0), 'g'),
                ((slice(2,4), 2, 0), 'b'),
                ((3, slice(0,2), 0), 'b'),
                ((3, 2, 1), 'y'),
            ]
        },
        "incorrect":{
            "cubes": np.full((5,5,5), ''),
            "operations":[
                ((1, slice(0,3), 0), 'b'),
                ((slice(2,4), 2, 0), 'g'),
                ((3, slice(0,2), 0), 'g'),
                ((3, 2, slice(1,2)), 'y'),
            ]
        },
        "view": ["xz", "-yz", "-xy", "yz"]
    },
}

#define event info for button functions
event_info = {
    'type': '',
    'description': '',
    'time': -1
    }

#function to insert colour codes into 3D array so it can be looped through each question
def assign_operations(cube, operations):
    for op in operations:
        cube[op[0]] = op[1] #this matches the format of cube[x,x,x] = 'colour'
    return cube

#function to calculate user's average time at the end
def Average(time): 
    return sum(time) / len(time)

#function to allow buttons to register events when clicked
#function taken from Button demo code.ipynb
def register_event(btn):
    # display button description in output area
    event_info['type'] = "click"
    event_info['description'] = btn.description
    event_info['time'] = time.time()
    return

#function to allow input to register events when user types
#function taken from Using_buttons_and_text_input_fix.ipynb
def register_text_input_event(text_input):
    event_info['type'] = "text_entry"
    event_info['description'] = text_input.value
    event_info['time'] = time.time()
    return

#function to create text input box
#function taken from Using_buttons_and_text_input_fix.ipynb
def text_input(prompt=None):
    text_input = widgets.Text(description=prompt, style= {'description_width': 'initial'})
    import warnings
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    text_input.on_submit(register_text_input_event)
    display(text_input)
    event = wait_for_event(timeout=60)
    text_input.disabled = True
    return event['description']

#function retrieved from Buttom demo code
def wait_for_event(timeout=-1, interval=0.001, max_rate=20, allow_interupt=True):    
    start_wait = time.time()
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

total_time = 0 #global variable for total time
incorrect_input = 0 #global variable for counter of incorrect questions

def draw_cube(ax, cubes, view): #function for the drawing of each cube array
        cubes_draw = np.zeros(cubes.shape)
        cubes_draw[cubes != ''] = 1
        nx, ny, nz = cubes.shape
        ax.axes.set_xlim3d(0, nx)
        ax.axes.set_ylim3d(0, ny)
        ax.axes.set_zlim3d(0, nz)
        #dictionary of views
        views = {
            'xy': (90, -90),
            '-xy': (-90, 90),
            'xz': (0, -90),
            '-xz': (0, 90),
            'yz': (0, 0),
            '-yz': (0, 180)
        }
        # Check if the specified view exists in the dictionary
        if view in views:
            ax.view_init(*views[view]) # Retrieve tuple corresponding to the given 'view'
        ax.voxels(cubes_draw, facecolors=cubes, edgecolors='k', shade=False)

#function to plot cube arrangements on given axes
def cube_arrangements(axes, cube_list, view_list, cube_wrong):
    answer_dic = {0: 'A', 1: 'B', 2: 'C', 3: 'D'}
    for i, (ax, cubes, view) in enumerate(zip(axes, cube_list, view_list)):
        draw_cube(ax, cubes, view)
        ax.set_title(answer_dic[i], fontsize=14, fontweight='bold')
        for axis in [ax.xaxis, ax.yaxis, ax.zaxis]:
            axis.set_ticklabels([])
            axis.line.set_linestyle('')
            axis._axinfo['tick']['inward_factor'] = 0.0
            axis._axinfo['tick']['outward_factor'] = 0.0
        if np.array_equal(cube_list[i], cube_wrong):
            answer = answer_dic[i]
    return answer

#function to print buttons panel and either accept or don't accept user input
def buttons_and_questions(answer):
    global incorrect_input
    a = widgets.Button(description='A', button_style = 'info')
    b = widgets.Button(description='B', button_style = 'info')
    c = widgets.Button(description='C', button_style = 'info')
    d = widgets.Button(description='D', button_style = 'info')
    panel = widgets.HBox([a, b, c, d])

    a.on_click(register_event)
    b.on_click(register_event)
    c.on_click(register_event)
    d.on_click(register_event)

    start_time = time.time()
    display(panel)
    
    while True:
        event = wait_for_event()
        if event['description'] != answer:
            display(HTML("<span style = 'color:red; font-size: 15px; '>Incorrect. Please try again. </span>"))
            incorrect_input = incorrect_input + 1
            continue
        else:
            break
    return start_time

#function for drawing cube arrangements
def draw_cubes(cube_correct, cube_wrong, view_list, seed):
    global total_time #assign global variable so that total_time can be accessed outside the function
    question = HTML("<span style = 'font-size: 20px;'> Which of the views (a-d) CANNOT be made by rotating the cube arrangement shown?</span>")
    display(question)
    time.sleep(1)
    
    fig_q, ax_q = plt.subplots(subplot_kw={'projection': '3d', 'proj_type': 'ortho', 'box_aspect': (4, 4, 4)})
    #plot the 'correct' cube arrangement
    draw_cube(ax_q, cube_correct, 'default')
    display(fig_q)
    time.sleep(1)
    
    #create list containing three arrangements that are correct and one that is incorrect
    cube_list = [cube_correct] * 3 + [cube_wrong]
    #take seed input from function so that list is shuffled the same way each time code is run
    random.seed(seed)
    random.shuffle(cube_list)
    
    #assign figure and 3D axes for plotting- subplotted so that each figure is placed one next to the other in a row
    fig, axes = plt.subplots(1, 4, figsize=(16, 4), subplot_kw={'projection': '3d', 'proj_type': 'ortho', 'box_aspect': (4, 4, 4)})
    
    ans = cube_arrangements(axes, cube_list, view_list, cube_wrong)
    display(fig)
    
    start_time = buttons_and_questions(ans)
    end_time = time.time()
    total_time = end_time - start_time
    
    display(HTML("Well done!"))
    time.sleep(1)
    display(HTML(f"You took {total_time:.2f} seconds"))
    time.sleep(2)

    clear_output()
    
#create list of times that the user has taken for each question
time_list = []
#create list of seeds that can be used for each question when shuffling cube_list
seed_list = [11, 23, 3, 4, 5, 6, 76, 8, 9, 65, 82, 76, 43]

#function for retrieving user details if they consent
def get_details():
    display(HTML("<b> Generate your anonymised ID <b>"))
    display(HTML("To generate an anonymous 4-letter unique user identifier please enter:"))
    display(HTML("   -two letters based on the initials (first name and last name) of a childhood best friend"))
    display(HTML("   -two letters based on the initials (first name and last name) of a favourite actor/actress"))
    display(HTML("e.g. if your friend was called Charlie Brown and film star was Tom Cruise then your unique identifier would be CBTC"))
    time.sleep(0.5)
    name = text_input('ID:')
    
    display(HTML("What is your age?"))
    time.sleep(0.5)
    age = text_input('Age:')
    
    display(HTML("What is your gender?"))
    time.sleep(0.5)
    gender = text_input('Gender:')
    
    display(HTML("What is your occupation?"))
    time.sleep(0.5)
    occupation = text_input('Occupation:')
    
    display(HTML("Do you drink alcohol (Y/N)?"))
    time.sleep(0.5)
    alcohol = text_input('Alcohol consumption:')
    
    display(HTML("Do you/ have you ever smoked (Y/N)?"))
    time.sleep(0.5)
    smoking = text_input('Smoking:')
    
    return name, age, gender, occupation, alcohol, smoking

#function to create consent button- user can selection either 'yes' or 'no'
def consent_button():
    display(HTML("<span style='font-size: 20px;'> DATA CONSENT INFORMATION </span>"))
    time.sleep(1)
    display(HTML("<span style='font-size: 15px;'> We wish to record your response data to an anonymised public data repository. Your data will be used for educational teaching purposes practising data analysis and visualisation.</span>"))
    display(HTML("<span style='font-size: 20px;'> Do you consent to your data being uploaded? </span>"))
    consent_yes = widgets.Button(description = "Yes", button_style = 'success')
    consent_no = widgets.Button(description = "No", button_style = 'danger')
    consent_panel = widgets.HBox([consent_yes, consent_no])
    
    consent_yes.on_click(register_event)
    consent_no.on_click(register_event)
    display(consent_panel)
    user_consent = wait_for_event()
    return user_consent

#function to create button that user can click when they are ready to begin the test
def initialise_test():
    display(HTML("<span style='font-size: 20px;'> Are you ready to begin the test? </span>"))
    button = widgets.Button(description = 'Start the test', button_style = 'primary')
    button.on_click(register_event)
    display(button)
    wait_for_event()
    clear_output()
    pass

#function for the actual running of the test
def run_spatial_reasoning_test(game_qs, seed_list):
    display(HTML("<h1> Welcome to the spatial reasoning test.</h1>"))
    time.sleep(1)
    display(HTML("<span style='font-size: 15px;'> You will be shown a 3D arrangement of coloured cubes and asked to identify which of four 2D plans is not a plan of the 3D cube arrangement you are being shown. </span>"))
    display(HTML("<span style='font-size: 15px;'> There will be 13 questions in total. </span>"))
    time.sleep(2)
    print("")
    consent = consent_button()
    if consent['description'] == 'Yes':
        clear_output()
        display(HTML("<span style='font-size: 15px;'> Thank you for your participation. </span>"))
        display(HTML("<span style='font-size: 15px;'> Please contact a.fedorec@ucl.ac.uk if you have any questions or concerns regarding the stored results.</span>"))
        time.sleep(1)
        display(HTML("<span style='font-size: 20px;'> Please enter some details about yourself. </span>"))
        name, age, gender, occupation, alcohol, smoking = get_details()
    else:
         display(HTML("<span style='font-size: 20px;'> Okay. Your details will not be used in our research. </span>"))
         name, age, gender, occupation, alcohol, smoking = 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A'
    initialise_test()
    
    #loops through each key and value in game_qs dictionary, and each seed in seed_list
    for (key, value), seed in zip(game_qs.items(), seed_list):
        #prints the question number
        qu = key.title()
        qu_main = qu.split("_")
        display(HTML(f"<span style='font-size: 30px;'>{qu_main[0]} {qu_main[1]}:</span>"))
        #creates variable for the 'correct' cube arrangement by retrieving from game_qs
        cube_correct = assign_operations(value["correct"]["cubes"], value["correct"]["operations"])
        #creates variables for 'incorrect' cube arrangment by retrieving from game_qs
        cube_wrong = assign_operations(value["incorrect"]["cubes"], value["incorrect"]["operations"])
        #draws question
        draw_cubes(cube_correct, cube_wrong, value["view"], seed)
        #appends the time taken in that question to time_list
        time_list.append(total_time)
    
    #calculates average time when test is over
    average_time = Average(time_list)
    full_time = sum(time_list)
    
    display(HTML(f"<span style='font-size: 30px;'> Thank you for taking the spatial reasoning test.</span>"))
    display(HTML(f"<span style='font-size: 20px'> You got <strong>{incorrect_input}<strong> question/s wrong overall. </span>"))
    display(HTML(f"<span style='font-size: 20px'> Your average time was <strong>{average_time:.2f}<strong> seconds.</span>"))
    display(HTML(f"<span style='font-size: 20px'> Your total time was <strong>{full_time:.2f}<strong> seconds.</span>"))
    #dictionary of user data that will be uploaded to google form
    data_dict = {
        'Name': name,
        'Age': age,
        'Gender': gender,
        'Occupation': occupation,
        'Alcohol': alcohol,
        'Smoking': smoking,
        'q1': time_list[0],
        'q2': time_list[1],
        'q3': time_list[2],
        'q4': time_list[3],
        'q5': time_list[4],
        'q6': time_list[5],
        'q7': time_list[6],
        'q8': time_list[7],
        'q9': time_list[8],
        'q10': time_list[9],
        'q11': time_list[10],
        'q12': time_list[11],
        'q13': time_list[12],
        'average': average_time,
        'total': full_time,
        'incorrect': incorrect_input,
        }
    #send results to google form
    send_to_google_form(data_dict, 'https://docs.google.com/forms/d/e/1FAIpQLSdjZjry_f_EQB4HBGlEPUvwxdE9uGMW_X5QKSLi469bT8oMOw/viewform?usp=sf_link')

if __name__ == "__main__":
    run_spatial_reasoning_test(game_qs, seed_list)