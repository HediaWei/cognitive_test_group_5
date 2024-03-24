from IPython.display import display, Image, clear_output, HTML
import time
import random
import requests
from bs4 import BeautifulSoup
import json

import ipywidgets as widgets
from jupyter_ui_poll import ui_events

'''
I acknowledge the use of AI tools (ChatGPT3.5) by OpenAI to help with fixing issues in my code and debugging. 
URL: hhtps://chat.openai.com/

'''



### Functions for includng buttons

## Define event info for buttons functions

event_info = {
    'type': '',
    'description': '',
    'time': -1
}

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


#function to allow buttons to register events when clicked
#function taken from Button demo code.ipynb

def register_btn_event(btn):
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
    event_info['type'] = "button click"
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
    event = wait_for_event(timeout=10)
    text_input.disabled = True
    return event['description']


#function to print buttons panel - will accept whether answer is correct or incorrect

def buttons(question_list, answer):
    '''
    Prints buttons panel for each possible question answer and accepts user input. 
    
    This function creates an ipywidgets button for each possible answer and then
    creates a HBox panel on which they will be layed out. It then assigns the 
    register_event function to be used when a button is clicked. If the button clicked
    is correct, it adds 1 to the score counter, if incorrect, no score is added. 

    Parameters
    ------------
    question_list : list of strings
        List of different possible answers displayed in the 4 buttons

    answer : dict of lists of strings
        dictionary containing the question lists, plus the correct answer. 

    Returns
    ---------
    integer
        The total score 

    See Also
    --------
    register_event : Registers event for button input.
    
    wait_for_event : Waits for an event to take place with the option to set timeout.
    '''
    score_q = 0
    a = widgets.Button(description = question_list[0])
    b = widgets.Button(description = question_list[1])
    c = widgets.Button(description = question_list[2])
    d = widgets.Button(description = question_list[3])
    panel = widgets.HBox([a, b, c, d])

    a.on_click(register_btn_event)
    b.on_click(register_btn_event)
    c.on_click(register_btn_event)
    d.on_click(register_btn_event)

    display(panel)

    event = wait_for_event()
    if event['description'] == answer:
        score_q = score_q + 1
        
    return score_q
    
#function to create consent button- user can selection either 'yes' or 'no'

def consent_button():
    '''
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
    '''
    display(HTML("<span style='font-size: 20px;'> DATA CONSENT INFORMATION </span>"))
    time.sleep(1)
    display(HTML("<span style='font-size: 15px;'> We wish to record your response data to an anonymised public data repository. Your data will be used for educational teaching purposespractising data analysis and visualisation.</span>"))
    display(HTML("<span style='font-size: 20px;'> Do you consent to your data being uploaded? </span>"))
    consent_yes = widgets.Button(description = "Yes", button_style = 'success')
    consent_no = widgets.Button(description = "No", button_style = 'danger')
    consent_panel = widgets.HBox([consent_yes, consent_no])
    
    consent_yes.on_click(register_btn_event)
    consent_no.on_click(register_btn_event)
    display(consent_panel)
    user_consent = wait_for_event()
    return user_consent



# function for sending user input data to google forms
#function code taken from Reaction_Timer.ipynb

def send_to_google_form(data_dict, form_url):
    '''
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




#function for retrieving user details if they consent

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

    # return all the different varibles within this function to be stored in a dict in the main game
    return name, age, gender, occupation, alcohol, smoking



# reading images used for the test in

image1= Image("image1.png", width = 700)
#display(image1)

image2= Image("image2.png", width = 700)
#display(image2)

image3= Image("image3.png", width = 700)
#display(image4)




#game loop  - runs through a set of questions and corresponding answers for a particular grid
#used inside memory game loop multiple times

scores = []

def game_loop(image, questions, answers):
    '''
    Runs the game for one image

    This function displays the image for a 20 second interval, then disappears. 
    The function then loops through each question in the questions list, and displays 
    4 possible answers as buttons underneath each question. When the user clicks an 
    answer, the score is updated and the loop moves onto the next question until 
    there are no more. The user is imformed of their score at the end. 

    Parameters
    -----------
    image : Image of the grid of shapes
        The grid shows differnt coloured shapes taht the user has to memorise and
        answer questions on later
    questions : List of strings
        List of strings of questions corresponding to the image printed
    answers : Dict of lists of strings
        Contains a question_list of all the possible answers for the user to choose, 
        plus the correct answer. 

    Returns
    ---------
    integer
        Returns the score for the game for the single image
    '''
    score = 0
    display(image) # displays the grid for 20 seconds for the user to memorise
    time.sleep(25)
    clear_output(wait = False)
    
    for (i, key) in zip(questions, answers): #use zip funciton to loop i through questions and key through answers
        # asking question
        display(HTML(i))
        print('')
        print('')
        print('')
        print('')
        q_list = answers[key]["question_list"]
        answer = answers[key]["answer"]
        score_q = buttons(q_list, answer)
        score = score + score_q
        time.sleep(1)
        clear_output(wait=False)

        # Update score and prepare for next question
    (f"Score: {score}")

    scores.append(score)
    display(HTML(f'Your score for this round is {score}'))
    time.sleep(3)
    return score #returns score for this round




#running the whole game in a game loop

name = []
age = []

def memory_game():
    '''
    Runs the Memory Game.

    This function conducts the entire memory game. It begins by displaying the opening information
    and then asks for the user's consent. If the user consents to input their details, the get_details()
    function is used to retrieve user details. If they do not consent, the details will be set to N/A 
    and the user will still be able to play the test. The function then runs through the game_loop three 
    times (once for each grid) before totalling the scores and displaying the final score. The user's details,
    scores for each round and total score is then retrieved and uploaded to the google form. 
    '''
    
    totalscore = 0

    
    questions1 = ["<span style = 'font-size:30px;'> What colour was the triangle? </span>", 
                  "<span style = 'font-size:30px;'>How many sides did the purple shape have?</span>", 
                  "<span style = 'font-size:30px;'>What colour was the shape to the right of the yellow shape?</span>", 
                  "<span style = 'font-size:30px;'>What colour was the circle?</span>", 
                  "<span style = 'font-size:30px;'>What colour was above the red?</span>"]

    #creating lists in dictionaries containg my questions and answers
    answers1 = {
        "q1" : {
            "question_list": ['Red', 'Purple', 'Yellow', 'Pink'],
            "answer": "Red"},
        "q2" : {
            "question_list": ['2', '3', '4', '5'],
            "answer": "5"},
        "q3" : {
            "question_list": ['Red', 'Purple', 'Blue', 'Pink'],
            "answer": "Blue"},
        "q4" : {
            "question_list": ['Blue', 'Purple', 'Yellow', 'Green'],
            "answer": "Green"},
        "q5" : {
            "question_list": ['Red', 'Purple', 'Yellow', 'Pink'],
            "answer": "Pink"}
    }

    questions2 = ["<span style = 'font-size:30px;'>What was the yellow shape?</span>", 
                  "<span style = 'font-size:30px;'>How many arrows on the grid?</span>", 
                  "<span style = 'font-size:30px;'>What colour was the cross</span>", 
                  "<span style = 'font-size:30px;'>What colour was to the left of the dark blue shape?</span>"]

    answers2 = {
        "q1" : {
            "question_list": ['Circle', 'Star', 'Square', 'Triangle'],
            "answer": "Star"},
        "q2" : {
            "question_list": ['1', '2', '3', '4'],
            "answer": "2"},
        "q3" : {
            "question_list": ['Red', 'Purple', 'Blue', 'Pink'],
            "answer": "Blue"},
        "q4" : {
            "question_list": ['Blue', 'Purple', 'Yellow', 'Green'],
            "answer": "Green"}
    }


    questions3 = ["<span style = 'font-size:30px;'>How many colours were shown in the grid?</span>", 
                  "<span style = 'font-size:30px;'>What was the centre shape?</span>",
                  "<span style = 'font-size:30px;'>What colour was the plus sign</span>",
                  "<span style = 'font-size:30px;'>What was inside the blue square</span>", 
                  "<span style = 'font-size:30px;'>What colour was the star</span>",
                  "<span style = 'font-size:30px;'>What colour was above the star</span>",
                  "<span style = 'font-size:30px;'>What was above the middle square</span>"]

    answers3 = {
        "q1" : {
            "question_list": ['8', '9', '10', '12'],
            "answer": "10"},
        "q2" : {
            "question_list": ['Bolt', 'Cross', 'Circle', 'Sun'],
            "answer": "Sun"},
        "q3" : {
            "question_list": ['Red', 'Purple', 'Blue', 'Pink'],
            "answer": "Purple"},
        "q4" : {
            "question_list": ['Red Circle', 'Green Circle', 'Yellow Cross', 'Pink Triangle'],
            "answer": "Red Circle"},
        "q5" : {
            "question_list": ['Green', 'Purple', 'Yellow', 'Pink'],
            "answer": "Green"}, 
        "q6" : {
            "question_list": ['Orange', 'Purple', 'Yellow', 'Pink'],
            "answer": "Orange"},
        "q7" : {
            "question_list": ['Red Circle', 'Green Circle', 'Yellow Cross', 'Pink Triangle'],
            "answer": "Yellow Cross"}     
    }
    
                  

    display(HTML("<h1 align = 'center'>Welcome to the memory game!</h1>"))
    time.sleep(2)

    #getting consent
    consent = consent_button()
    if consent['description'] == 'Yes':
        clear_output()
        display(HTML("<span style='font-size: 15px;'> Thank you for your participation. </span>"))
        display(HTML("<span style='font-size: 15px;'> Please contact a.fedorec@ucl.ac.uk if you have any questions or concerns regarding the stored results.</span>"))
        time.sleep(3)
        display(HTML("<span style='font-size: 20px;'> Please enter some details about yourself. </span>"))
        name, age, gender, occupation, alcohol, smoking = get_details()
    else:
         display(HTML("<span style='font-size: 20px;'> Okay. Your details will not be used in our research. </span>"))
         name, age, gender, occupation, alcohol, smoking = 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A'
        


    clear_output(wait=False)
    
    display(HTML("<span style = 'font-size:20px;'>A grid will show up showing coloured shapes for a short period of time</span>"))
    time.sleep(2)
    display(HTML("<span style = 'font-size:20px;'>When the grid disappears, you will be asked questions to test your memory of the grid</span>"))
    time.sleep(3)
    display(HTML("<span style = 'font-size:20px;'>There will be 3 grids in total. Good luck!!</span>"))
    time.sleep(6)
    clear_output(wait=False)


    #first grid
    display(HTML("<span style = 'font-size:20px;'>Here is the First Grid</span>"))
    time.sleep(3)
    clear_output(wait=False)

    score1 = game_loop(image1, questions1, answers1)
    totalscore += score1
    

    #second grid
    display(HTML("<span style = 'font-size:30px;'>Here is the Second Grid</span>"))
    time.sleep(3)
    clear_output(wait=False)

    score2 = game_loop(image2, questions2, answers2)
    totalscore += score2


    #third grid
    display(HTML("<span style = 'font-size:30px;'>Here is the Third Grid</span>"))
    time.sleep(3)
    clear_output(wait=False)

    score3 = game_loop(image3, questions3, answers3)
    totalscore += score3
    
    display(HTML("<span style = 'font-size:30px;'>The game is now over, well done!!</span>"))
    time.sleep(3)

    
    display(HTML(f"<span style = 'font-size:30px;'>Your final score was {totalscore}!</span>"))
    
    
    time.sleep(5)

    data_dict = {
        'Name': name,
        'Age': age,
        'Gender' : gender,
        'Occupation' : occupation,
        'Alcohol': alcohol,
        'Smoking': smoking,
        'Score 1': score1,
        'Score 2': score2,
        'Score 3': score3, 
        'Total Score' : totalscore,
        }


    form_url = 'https://docs.google.com/forms/d/e/1FAIpQLScT70tgqmdGZKBrb_hoCDTcXlwkkzPb5QDaTHd5K-KvGpPo9g/viewform?usp=sf_link'
    send_to_google_form(data_dict, form_url)

    return 

if __name__ == '__main__':
    memory_game()



