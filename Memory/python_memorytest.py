from IPython.display import display, Image, clear_output, HTML
import time
import random
import requests
from bs4 import BeautifulSoup
import json

import ipywidgets as widgets
from jupyter_ui_poll import ui_events




# function for sending data to google forms

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




#function for retrieving user details if they consent
def get_details():
    display(HTML("<b> Generate your anonymised ID <b>"))
    display(HTML("To generate an anonymous 4-letter unique user identifier please enter:"))
    display(HTML("   -two letters based on the initials (first name and last name) of a childhood best friend"))
    display(HTML("   -two letters based on the initials (first name and last name) of a favourite actor/actress"))
    display(HTML("e.g. if your friend was called Charlie Brown and film star was Tom Cruise then your unique identifier would be CBTC"))
    time.sleep(0.5)
    name = input('ID:')
    
    display(HTML("What is your age?"))
    time.sleep(0.5)
    age = input('Age:')
    
    display(HTML("What is your gender?"))
    time.sleep(0.5)
    gender = input('Gender:')
    
    display(HTML("What is your occupation?"))
    time.sleep(0.5)
    occupation = input('Occupation:')
    
    display(HTML("Do you drink alcohol (Y/N)?"))
    time.sleep(0.5)
    alcohol = input('Alcohol consumption:')
    
    display(HTML("Do you/ have you ever smoked (Y/N)?"))
    time.sleep(0.5)
    smoking = input('Smoking:')

    # return all the different varibles within this function to be stored in a dict in the main game
    return name, age, gender, occupation, alcohol, smoking



# reading images in

image1= Image("image1.png", width = 300)
#display(image1)

image2= Image("image2.png", width = 300)
#display(image2)

image3= Image("image3.png", width = 300)
#display(image3)

image4= Image("image4.png", width = 300)
#display(image4)



# questions and answers stored as lists 

questions1 = ['What colour was the shape with 3 sides?', 
              'How many sides did the purple shape have?', 
              'What colour was the shape to the right of the yellow shape?', 
              'What colour was the circle?', 
              'What colour was above the red?']

answers1 = ['red', ['5', 'five'], 'blue', 'green', 'pink']

len(questions1)

questions2 = ['What was the yellow shape?', 
              'How many arrows on the grid?', 
              'What colour was the cross', 
              'What colour was to the left of the dark blue shape?']

answers2 = ['star', ['two', '2'], ['light blue', 'blue', 'cyan'], ['green', 'dark green']]

questions3 =  ['What was the yellow shape?',
              'What colour is the triangle?', 
              'What colour was the cross', 
              'What colour was to the left of the dark blue shape?', 
              'What colour was above orange?']

answers3 = ['pentagon', 'purple', 'red', 'pink', ['green', 'dark green']]

questions4 = ['How many colours were shown in the grid?', 
              'What was the centre shape?',
              'What colour was the plus sign',
              'What was inside the blue square (answer should be written as: colour shape)', 
              'What colour was the star',
              'What colour was above the star',
              'What was above the middle square (colour shape)']

answers4 = [['ten', '10'], 'sun', 'purple', 'red circle', ['light green', 'green'], 'orange', 'yellow cross']




#game loop  - runs through a set of questions and corresponding answers for a particular grid
#used inside memory game loop multiple times

scores = []

def game_loop(image, questions, answers):
    score = 0
    display(image)
    time.sleep(20)
    clear_output(wait = False)
    
    for i in range(len(questions)):
        
        # asking question
        print(questions[i])
        answer = input("Your answer: ")  
        # Check answer
        if answer.lower() == answers[i].lower():
            print("Correct!")
            time.sleep(2)
            score += 1
        else:
            print(f"Wrong! The correct answer was '{answers[i]}'.")
            time.sleep(2)
        clear_output(wait=False)

        # Update score and prepare for next question
        (f"Score: {score}")

        scores.append(score)
    print(f'Your score for this round is', score)
    time.sleep(3)
    return score #returns score for this round




#running the whole game

name = []
age = []

def memory_game():

    totalscore = 0
    
    questions1 = ['What colour was the triangle?', 
                  'How many sides did the purple shape have?', 
                  'What colour was the shape to the right of the yellow shape?', 
                  'What colour was the circle?', 
                  'What colour was above the red?']

    answers1 = ['red', '5', 'blue', 'green', 'pink']

    questions2 = ['What was the yellow shape?', 
                  'How many arrows on the grid?', 
                  'What colour was the cross', 
                  'What colour was to the left of the dark blue shape?']

    answers2 = ['star', '2', 'blue', 'green']

    questions3 =  ['What was the yellow shape?',
                  'What colour is the triangle?', 
                  'What colour was the cross', 
                  'What colour was to the left of the dark blue shape?', 
                  'What colour was above orange?']

    answers3 = ['pentagon', 'purple', 'red', 'pink', 'green']

    questions4 = ['How many colours were shown in the grid?', 
                  'What was the centre shape?',
                  'What colour was the plus sign',
                  'What was inside the blue square (answer should be written as: colour shape)', 
                  'What colour was the star',
                  'What colour was above the star',
                  'What was above the middle square (colour shape)']

    answers4 = ['10', 'sun', 'purple', 'red circle', 'green', 'orange', 'yellow cross']
    
                  

    display(HTML("<h1>Welcome to the memory game!</h1>"))
    time.sleep(2)


    display(HTML("<span style = font-size:30px;'>DATA CONSENT INFORMATION</span style>"))
    time.sleep(2)
    
    display(HTML("Please read: We wish to record your response data to an anonymised public data repository."))
    display(HTML("Your data will be used for educational teaching purposes practising data analysis and visualisation."))
    display(HTML("Please type yes if you consent to the upload"))
    cont = input(">")

    if cont == 'yes':
        display(HTML("Thanks for your participation."))
        display(HTML("Please contact a.fedorec@ucl.ac.uk"))
        display(HTML("if you have any questions or concerns"))
        display(HTML("regarding the stored results"))
        time.sleep(5)

    else:
        raise(Exception("User did not consent to continue test."))


    clear_output(wait=False)
    
    # gathering information on the player
    name, age, gender, occupation, alcohol, smoking = get_details()
    
    display(HTML("<span style = 'font-size:20px;'>A grid will show up showing coloured shapes for a short period of time</span>"))
    time.sleep(2)
    display(HTML("<span style = 'font-size:20px;'>When the grid disappears, you will be asked questions to test your memory of the grid</span>"))
    time.sleep(3)
    display(HTML("<span style = 'font-size:20px;'>There will be 4 grids in total. Good luck!!</span>"))
    time.sleep(6)
    clear_output(wait=False)


    #first grid
    display(HTML("<span style = 'font-size:20px;'>Here is the first grid</span>"))
    time.sleep(3)
    clear_output(wait=False)

    score1 = game_loop(image1, questions1, answers1)
    totalscore += score1
    

    #second grid
    display(HTML("<span style = 'font-size:30px;'>Here is the second grid</span>"))
    time.sleep(3)
    clear_output(wait=False)

    score2 = game_loop(image2, questions2, answers2)
    totalscore += score2


    #third grid
    display(HTML("<span style = 'font-size:30px;'>Here is the third grid</span>"))
    time.sleep(3)
    clear_output(wait=False)

    score3 = game_loop(image3, questions3, answers3)
    totalscore += score3


    #fourth grid
    display(HTML("<span style = 'font-size:30px;'>Here is the fourth grid</span>"))
    time.sleep(3)
    clear_output(wait=False)

    score4 = game_loop(image4, questions4, answers4)
    totalscore += score4
    
    display(HTML("<span style = 'font-size:30px;'>The game is now over, well done!!</span>"))
    time.sleep(3)

    
    display(HTML(f"<span style = 'font-size:30px;'>'Your final score was' {totalscore}</span>"))
    
    
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
        'Score 4': score4, 
        'Total Score' : totalscore,
        }


    form_url = 'https://docs.google.com/forms/d/e/1FAIpQLScT70tgqmdGZKBrb_hoCDTcXlwkkzPb5QDaTHd5K-KvGpPo9g/viewform?usp=sf_link'
    send_to_google_form(data_dict, form_url)

    return 

if __name__ == '__main__':
    memory_game()

