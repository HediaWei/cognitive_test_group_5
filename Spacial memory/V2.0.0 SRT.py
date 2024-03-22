import matplotlib.pyplot as plt
import numpy as np
import time
import random
from IPython.display import display, Image, clear_output, HTML
import ipywidgets as widgets
import requests
from bs4 import BeautifulSoup
from jupyter_ui_poll import ui_events
import pandas as pd
from scipy import stats
import json

'''
I acknowledge the use of AI tools (ChatGPT.3.5) by OpenAI to help with debugging/ fixing issues related to the ipywidgets module
and to help with making the dictionary of questions that produces each of the cube arrangements.
URL: https://chat.openai.com/
'''

#function to send data retrieved at end of test to google form 
#function code taken from Reaction_Timer.ipynb
def send_to_google_form(data_dict, form_url):
    """
     Sends data from dictionary to google form.
    
    This function takes the form ID from the form URL provided and retrieves the content of the form.
    It then maps data from the dictionary into the form fields and sends it to google form
    via HTTP POST request. 
    If any item is missing from data_dict the function returns False.
    
    Parameters
    ----------
    data_dict : dict
        Dictionary of data collected from test to be uploaded to google form.
    form_url : str
        URL of google form for data to be sent to.
    
    Returns
    -------
    bool
        True if data was succesfully sent to google form, or False if it was not.
    """
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
        "correct": { #the next level of dictionary assigns each variable that will be inputted into draw_question function
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

def assign_operations(cube, operations):
    """
    Creates cube arrangements based on list of operations.
    
    This function takes the cube object which can be indexed with three values [x, y, z].
    It then loops through a list of operations provided in the game_qs dictionary and 
    extracts each operation along with the colour associated with it. The function then
    returns a modified cube arrangement based on these operations in the format of 
    cube[x,y,z] = 'color'. 
    
    Parameters
    ----------
    cube: numpy.ndarray
        A 3D array numpy array 5x5x5.
    operations: list of tuples
        Provides information on the index of each cube and its colour.
        
    Returns
    -------
    numpy.ndarray
        A 3D arrangement of cube arrays in the format cube[x,y,z] = 'color'.
    
    See Also
    --------
    run_spatial_reasoning_test : Loops through each operation in game_qs dictionary to provide
    cube array for each question.
    
    Examples
    --------
    >>> cube = np.full((5,5,5), '')
    >>> operation = [((1, slice(0,3), 0), 'g'),
                ((slice(2,4), 2, 0), 'b'),
                ((3, slice(0,2), 0), 'b'),
                ((3, 2, 1), 'y')]
    >>> cube = assign_operations(cube, operation)
    >>> print(cube)
    Function will return a 3D cube arrangement
    """
    for op in operations:
        cube[op[0]] = op[1]
    return cube

def Average(time): 
    """
    Calculates average time.
    
    This function takes the list of times taken for a user to correctly
    answer each question and divides the sum by the length to calculate
    the mean average time.
    
    Parameters
    ----------
    time : list of float
        Time taken for user to complete each question.
    
    Returns
    -------
    float
        Average time taken across all questions.
    
    Examples
    --------
    >>> times = [12.465, 15.476, 11.233]
    >>> Average(times)
    13.058
    """
    return sum(time) / len(time)

#function taken from Button demo code.ipynb
def register_event(btn):
    """
    Registers button input.
    
    This function populates the dictionary event_info with information about
    the button input. It sets the type of event to 'click', stores the 
    description of the button event information, and records the time at the
    moment the button is clicked. 
    
    Parameters
    ----------
    btn : instance of button class
        An instance of where the 'button' class is used in ipywidgets.
    
    See Also
    --------
    register_text_input_event : Registers event for text input.
    
    wait_for_event : Returns input description after wait time ends.
    """
    event_info['type'] = "click"
    event_info['description'] = btn.description
    event_info['time'] = time.time()
    return

#function to allow input to register events when user types
#function taken from Using_buttons_and_text_input_fix.ipynb
def register_text_input_event(text_input):
    """
    Registers text input.
    
    This function populates the dictionary event_info with information about
    the text input. It sets the type of event to 'text_entry', stores the 
    description of the text event information, and records the time at the
    moment the input is confirmed. 
    
    See Also
    --------
    register__event : Registers event for button input.
    
    text_input : Creates text input box.
    """
    event_info['type'] = "text_entry"
    event_info['description'] = text_input.value
    event_info['time'] = time.time()
    return

#function to create text input box
#function taken from Using_buttons_and_text_input_fix.ipynb
def text_input(prompt=None):
    """
    Allows for user input through a text input widget.
    
    This function creates a text input widget using the ipywidgets widgets.Text(), setting
    the description to the prompt. It ignores deprecation warnings to avoid them being
    displayed during creation of the widget. It uses the function register_text_input_event
    to deal with the events triggered by the text input, and then displays the widget. It
    then uses the function wait_for_event and sets timeout to 60 seconds, giving the user 
    60 seconds to input or perform some kind of action. After the event is captured, the 
    widget is disabled to prevent any further input, and the text entered by the user is 
    returned. 
    
    Parameters
    ----------
    prompt : str(optional)
        The text the user wishes to input.
    
    Returns
    -------
    str
        The text inputted by the user.
    
    See Also
    --------
    register_text_input_event : Registers text input.
    
    wait_for_event : Returns input description after wait time ends
    """
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
    """
    Waits for an event to take place with the option to set timeout.
    
    This function records the start time using the time module, then resets the values
    of the event_info dictionary. It then determines how many times to poll UI events
    during each loop based on max_rate and interval. It then enters a loop which 
    continues until either an event has occurred or the timeout period has elapsed.
    The function then returns the event_info dictionary which is updated if an event
    occurs (such as a button input). 
    
    Parameters
    ----------
    timeout : int
        The amount of time the user wishes the loop to run up to
    interval : float
        Determines the delay between each iteration of the loop.
    max_rate : int
        Calculates the number of times the UI events are processed during each interation of the loop
    allow_interupt : bool
        Allows the function to be interupted if an event occurs
    
    Returns
    -------
    dict
        An updated vertsion of the event_info dictionary if an event occurred.
        If no event occurred then it will be set to an empty string ''
    
    See Also
    --------
    register_text_input_event : Registers text input.
    
    register__event : Registers event for button input.
    
    text_input : Creates text input box.
    """
    start_wait = time.time()
    event_info['type'] = ""
    event_info['description'] = ""
    event_info['time'] = -1

    n_proc = int(max_rate*interval)+1
    
    with ui_events() as ui_poll:
        keep_looping = True
        while keep_looping==True:
            ui_poll(n_proc)

            if (timeout != -1) and (time.time() > start_wait + timeout):
                keep_looping = False
                
            if allow_interupt==True and event_info['description']!="":
                keep_looping = False
                
            time.sleep(interval)
    return event_info

total_time = 0 #global variable for total time
incorrect_input = 0 #global variable for counter of incorrect questions

def draw_cube(ax, cubes, view): 
    """
    Draws 3D cube array.
    
    This function initialises a new numpy array called cubes_draw which is 
    the same shape as the input array 'cubes' filled with zeros. It then
    modifies this array so that areas in the array which aren't empty are
    set to 1 (noting the presence of a cube) and the rest are set to 0. It
    then takes the dimensions of the cube array 'cubes' along each axis and 
    sets the limits of the 3D plot. The function then creates a dictionary 
    called 'views' which contains all the possible views of the 3D plot that
    could be made for the answers. It then checks if the parameter 'view' is
    in this dictionary. If it is, it sets the view of the 3D plot and then 
    draws the cube array using ax.voxels.
    
    Parameters
    ----------
    ax : Axes3D
        The 3D axis that the cube visualisation is drawn onto.
    cubes : numpy.ndarray
        A 3D numpy array representing the cube array.
    view : str
        The desired view for the 3D cube arrangement.
    
    See Also
    --------
    assign_operations : Creates cube arrangements based on list of operations.
    
    cube_arrangements : Plots 3D cube arrangements onto a given axis and determines 'incorrect' arrangement.
    
    draw_question : Draws each question including cube arrangements.
    """
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
    if view in views:
        ax.view_init(*views[view])
    ax.voxels(cubes_draw, facecolors=cubes, edgecolors='k', shade=False)

#function to plot cube arrangements on given axes
def cube_arrangements(axes, cube_list, view_list, cube_wrong):
    """
    Plots 3D cube arrangements onto a given axis and determines 'incorrect' arrangement.
    
    This function creates the dictionary answer_dic which contains the four different
    possible answer values each arrangement could get. It then iterates through each 
    axes, cube arrangement and view and calls the draw_cube function to draw the cube
    arrangement on a 3D axis. It then sets the title to the corresponding value in 
    answer_dic and then checks if the current cube arrangement being plotted is equal
    to the incorrect cube arrangement 'cube_wrong'. If it is then it assigns that letter
    to be the 'answer' for that question and returns this letter.
    
    Parameters
    ----------
    axes : list of Axes3D
        A list of 3D axes that the cube arrangements will be drawn onto.
    cube_list : list of numpy.ndarray
        A list of 3D numpy arrays that contains each cube arrangement to be plotted.
    view_list : list of str
        A list of strings specifying the view for each plot in the question.
    cube_wrong : numpy.ndarray
        A 3D numpy array for the specific cube arrangement that is the correct answer.
    
    Returns
    -------
    str
        Returns the letter associated with the correct answer.
    
    See Also
    --------
    
    buttons_and_questions : Prints buttons panel for each possible question answer and accepts user input.
    
    draw_cube : Draws 3D cube array.
    
    draw_question : Draws each question including cube arrangements.
    
    """
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
    """
    Prints buttons panel for each possible question answer and accepts user input.
    
    This function creates an ipywidgets button for each possible answer and then
    creates a HBox panel on which they will be layed out. It then assigns the 
    register_event function to be used when a button is clicked. It starts timing
    the user when the panel is displayed and uses the wait_for_event function
    to register when a button is clicked. If the button clicked is not correct, the
    function displays an incorrect message, adds to a counter incorrect_input 
    counting the number of times the user has clicked the wrong button, and then
    loops back round to continue displaying the buttons until they click the correct
    answer. When the correct answer button is clicked, the loop is broken and the 
    start time is returned.
    
    Parameters
    ----------
    answer : str
        The letter associated with the correct answer determined by cube_arrangements.
    
    Returns
    -------
    float
        The time at which the buttons panel was first displayed.
    
    See Also
    --------
    register_event : Registers event for button input.
    
    wait_for_event : Waits for an event to take place with the option to set timeout.
    
    cube_arrangements : Plots 3D cube arrangements onto a given axis and determines 'incorrect' arrangement.
    """
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
def draw_question(cube_correct, cube_wrong, view_list, seed):
    """
    Draws each question and plots cube arrangements.
    
    This function first prints what the user is expected to do in each question. It then creates
    a matplotlib figure and axis on which the main question cube arrangement (the arrangement of 
    which the user will have to find the incorrect rotation of) will be plotted onto. It then uses
    the draw_cube function to draw this cube arrangement which is the parameter cube_correct and 
    displays it. A list is then created made out of the correct cube arrangement and the incorrect
    cube arrangement (the answer). Taking a seed from the list 'seed', the function then randomly 
    shuffles the order of these arrangements in the list. A figure and axis is created for the 
    four possible answers, creating subplots along a panel. The list of possible answers and the
    numpy array for the 'correct' answer (incorrect arrangement) are put into the cube_arrangements
    function for the 3D cubes to be plotted onto a 3D axis and the correct answer is returned. The
    plots are then displayed and the buttons_and_questions function is called to display the 
    panel of buttons and start timing the user. When the user clicks a button, the 
    button_and_questions function returns the start time and the end time is recorded. The total time
    is calculated from these and then the output is cleared.
    
    Parameters
    ----------
    cube_correct : numpy.ndarray
        A 3D numpy array for the cube arrangement that will first be displayed in the question.
    cube_wrong : numpy.ndarray
        A 3D numpy array for the cube arrangement that is not the same as the arrangement shown in the question.
        This arrangement will be the 'correct' answer.
    view_list : list of str
        A list of strings for the different rotations that the cube arrangements will be shown at in the question.
    seed : list of int
        A list of integers representing seeds for each question so that the random shuffling is reproducible.
    
    See Also
    --------
    draw_cube : Draws 3D cube array.
    
    cube_arrangements : Plots 3D cube arrangements onto a given axis and determines 'incorrect' arrangement.
    
    buttons_and_questions : Prints buttons panel for each possible question answer and accepts user input.
    """
    global total_time #assign global variable so that total_time can be accessed outside the function
    question = HTML("<span style = 'font-size: 20px;'> Which of the views (a-d) CANNOT be made by rotating the cube arrangement shown?</span>")
    display(question)
    time.sleep(1)
    
    fig_q, ax_q = plt.subplots(subplot_kw={'projection': '3d', 'proj_type': 'ortho', 'box_aspect': (4, 4, 4)}, figsize = (3, 3))
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

def get_details():
    """
    Accepts user input for their details to be used for in research. 
    
    This function simply takes a number of details inputted by the user,
    including an anonymised ID, their age, gender, occupation, alcohol
    consumption, and smoking. The text_input function is used to allow
    the user to input their information.
    
    Returns
    -------
    str
        Returns strings representing the user's inpuuted name, age, gender,
        occupation, alcohol consumption, and smoking information. 
    
    See Also
    --------
    run_spatial_reasoning_test : Loops through each question in the test.
    """
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

#function to create consent button- user can select either 'yes' or 'no'
def consent_button():
    """
    Creates consent buttons.
    
    This function creates two buttons in a panel to allow the user to input
    whether or not they agree to let their details be used as part of 
    experimental research. The register_event function is assigned to when
    the user clicks a button so that the information is uploaded to the 
    events_info dictionary. After the panel is displayed, the wait_for_event
    function is called so that the loop runs until the user clicks a button. 
    The function then returns the event_info dictionary.
    
    Returns
    -------
    dic
        A dictionary called event_info which contains information on the event-
        clicking the button.
    
    See Also
    --------
    register_event : Registers event for button input.
    
    wait_for_event : Waits for an event to take place with the option to set timeout.
    
    run_spatial_reasoning_test : Loops through each question in the test.
    """
    display(HTML("<span style='font-size: 20px;'> <b>DATA CONSENT INFORMATION<b> </span>"))
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
    """
    Creates button user can click when they are ready to begin.
    
    This function displays text asking the user if they are ready to begin the test.
    It then displays a button and assigns the register_event function to when the user
    clicks the button so the information of the event is assigned to the events_info
    dictionary. The button is then displayed and the wait_for_event function is called.
    When the user clicks the button, the output is cleared.
    
    See Also:
    --------
    register_event : Registers event for button input.
    
    wait_for_event : Waits for an event to take place with the option to set timeout.
    
    run_spatial_reasoning_test : Loops through each question in the test.
    """
    display(HTML("<span style='font-size: 20px;'> Are you ready to begin the test? </span>"))
    button = widgets.Button(description = 'Start the test', button_style = 'primary')
    button.on_click(register_event)
    display(button)
    wait_for_event()
    clear_output()
    pass

def comparison(average_time):
    """
    Compares user data to data used in research.
    
    This function reads in the excel document for the spatial reasoning results obtained
    and then creates a box plot that compares the average scores of other users to the
    user that has just completed the test. It then calculates the percentile rank of
    the user in comparison to the other users and personalises a message based on how
    well they did. 
    
    Parameters
    ---------
    average_time : float
        A float calculated as the average time the user took on each question.
    """
    spatial_data = pd.read_excel('Spatial_reasoning.xlsx')
    fig, ax = plt.subplots()

    plt.boxplot(spatial_data['average'], patch_artist=True, notch=True, 
            boxprops=dict(facecolor='lightblue', color='darkblue'), 
            whiskerprops=dict(color='darkblue'), 
            capprops=dict(color='darkblue'), 
            medianprops=dict(color='darkblue'))
    plt.scatter(1, average_time, color='red', label='Your average time', zorder=3, s=100, marker='+') 
    plt.ylabel('Average time taken', fontsize=14, fontweight='bold')
    plt.yticks(fontsize=12)
    ax.set_xticklabels("")
    plt.gca().set_facecolor('lightgray')
    plt.grid(True)
    plt.tight_layout()

    plt.legend()

    plt.show()

    percentile = stats.percentileofscore(spatial_data['average'], average_time)
    display(HTML(f"<span style='font-size: 20px;'> You're in the top <b>{100 - percentile:.2f}% </b>of users that have taken the spatial reasoning test.</span>"))

    if percentile <= 10:
        display(HTML("<span style='font-size: 15px;'> Congratulations! You're in the top 10% of users. Well done!</span>"))
    elif percentile > 10 and percentile <= 25:
        display(HTML("<span style='font-size: 15px;'> Great work! Your spatial reasoning is considerably above average!</span>"))
    elif percentile > 25 and percentile <= 50:
        display(HTML("<span style='font-size: 15px;'> Nice job, you performed better than half the users.</span>"))
    elif percentile > 50 and percentile <= 75:
        display(HTML("<span style='font-size: 15px;'> You're in the bottom half of users. Maybe next time?</span>"))
    elif percentile > 75 and percentile <= 90:
        display(HTML("<span style='font-size: 15px;'> At least you're not in the bottom 10%.</span>"))
    else:
        display(HTML("<span style='font-size: 15px;'> Spatial reasoning probably isn't your thing.</span>"))

#function for the actual running of the test
def run_spatial_reasoning_test(game_qs, seed_list):
    """
    Runs the spatial reasoning test.
    
    This function conducts the spatial reasoning test. It starts by displaying the opening information
    and then asks for the user's consent. If the user consents to input their details, the get_details()
    function is used to retrieve user details. If they do not consent, the details will be set to N/A 
    and the user will still be able to play the test. The initialise_test function is called so that the
    test stalls until the user is ready to start. A progress bar is also created for when the game starts.
    The function then loops through each question in the game_qs dictionary and each seed in the seed_list, 
    drawing each question and cube arrangements until every question has been completed. The average time, 
    total time, and total number of incorrect inputs is then calculated and displayed to the user  and then
    the comparison function is called to show the user how they compare to the data used in our research 
    before the data retrieved is uploaded to the google form. 
    
    Parameters
    ----------
    game_qs : dic of numpy.ndarray and list of str
        A dictionary containing the 3D numpy arrays for the correct and incorrect cube arrangements in
        each question and the list of rotations that each cube arrangement can take. 
    seed_list : list of str
        A list of strings containing the seeds used in each question to randomly shuffle the order of
        cube arrangements.
    """
    display(HTML("<h1 align = 'center'> Welcome to the spatial reasoning test.</h1>"))
    print("")
    time.sleep(1)
    display(HTML("<span style='font-size: 15px;'> You will be shown a 3D arrangement of coloured cubes and asked to identify which of four 2D plans is not a plan of the 3D cube arrangement you are being shown. </span>"))
    display(HTML("<span style='font-size: 15px;'> There will be <b>13 questions</b> in total. </span>"))
    time.sleep(2)
    print("")
    consent = consent_button()
    if consent['description'] == 'Yes':
        clear_output()
        display(HTML("<span style='font-size: 15px;'> Thank you for your participation. </span>"))
        display(HTML("<span style='font-size: 15px;'> Please contact a.fedorec@ucl.ac.uk if you have any questions or concerns regarding the stored results.</span>"))
        time.sleep(1)
        display(HTML("<span style='font-size: 20px;'> Please enter some details about yourself. </span>"))
        print("")
        name, age, gender, occupation, alcohol, smoking = get_details()
    else:
         display(HTML("<span style='font-size: 20px;'> Okay. Your details will not be used in our research. </span>"))
         name, age, gender, occupation, alcohol, smoking = 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A'
    initialise_test()
    
    progress_bar = widgets.IntProgress(
        value=0,
        min=0,
        max=13,
        description='Progress:',
        bar_style='',
        style={'bar_color': 'lightblue'},
        orientation='horizontal'
    )
    #loops through each key and value in game_qs dictionary, and each seed in seed_list
    for (key, value), seed in zip(game_qs.items(), seed_list):
        display(progress_bar)
        #prints the question number
        qu = key.title()
        qu_main = qu.split("_")
        display(HTML(f"<span style='font-size: 30px;'>{qu_main[0]} {qu_main[1]}/13:</span>"))
        #creates variable for the 'correct' cube arrangement by retrieving from game_qs
        cube_correct = assign_operations(value["correct"]["cubes"], value["correct"]["operations"])
        #creates variables for 'incorrect' cube arrangment by retrieving from game_qs
        cube_wrong = assign_operations(value["incorrect"]["cubes"], value["incorrect"]["operations"])
        #draws question
        draw_question(cube_correct, cube_wrong, value["view"], seed)
        #appends the time taken in that question to time_list
        time_list.append(total_time)
        progress_bar.value += 1
    
    #calculates average time when test is over
    average_time = Average(time_list)
    full_time = sum(time_list)
    
    display(HTML(f"<span style='font-size: 30px;'> Thank you for taking the spatial reasoning test.</span>"))
    time.sleep(1)
    display(HTML(f"<span style='font-size: 20px'> You got <b>{incorrect_input}</b> question/s wrong overall. </span>"))
    display(HTML(f"<span style='font-size: 20px'> Your average time was <b>{average_time:.2f}</b> seconds.</span>"))
    display(HTML(f"<span style='font-size: 20px'> Your total time was <b>{full_time:.2f}</b> seconds.</span>"))
    time.sleep(1)
    
    comparison(average_time)
    
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
