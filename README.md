# Cognitive test repository Group 5

This repository contains four cognitive tests used to examine variation in cognitive behaviours. The data obtained using these tests will be used for scientific analyses. The repository includes details on each cognitive test, the method of installation, method of usage, and any changes made to the V.2.0.0 code.

## Cognitive Tests

### ANS Test
On each trial of this task, two dot arrays ranging in numerosity from 9 to 21 were presented for 750 ms on each side of a central fixation cross, after which only the fixation cross remained on the screen. Participants were asked to judge which side contained more dots as quickly and as accurately as possible by a manual (left or right index fingers) button press. The response was accepted from stimulus onset until 3 s after the stimulus onset, which was followed by an intertrial interval of 1.5 s before the onset of the following trial. 

### Memory Test
This test asks users to observe a grid of coloured shapes for 25 seconds, then answer around 5 questions testing their memory of the grid. The users will be tested on 3 grids each containing different shapes and colours. At the end of the test, users' details information, score for each grid and total score will be recorded and uploaded to a google form. The test can also be performed even without user consent, and no personal data will be recorded. Users will also know their results at the end of the test, as well as their scores after each round. 

### Spatial Reasoning Test
This test requires the user to compare a 3D arrangement of coloured cubes to four possible 2D plans of different orientations and determine which is not possible. At the end of the test, average time, total time, and number of incorrect inputs will be recorded. The user will also be given the option to provide data about themselves so that their results can be used in our analyses, however the test can be performed even without user consent, and no personal data will be recorded.

### Mathematical Ability Test
Insert description of test

## Installation
To play the tests, users will need to have the most current version of Jupyter lab/notebook installed, as these tests make use of Jupyter-specific packages. They will also need to install all V.2.0.0 files in the repository. Without all of these, the test will not be able to run. Users should make sure that all files are saved to their current Jupyter working directory.

Users should also ensure they have all the packages required for the tests to run. These are listed in the requirements.txt file.

## Usage
To run the tests, users simply need to play the code chunk in the user interface ipynb files through Jupyter lab/notebook. 

## Changelog
### [2.0.0] - 2024-03-21

### ANS Test
Added
* Add a much clearer description of the user interface
* Added a 3s time wait between button clicks and questions pops out to allow a responce time
* Add a logic to check consent before test start

Changed
* Moved the consent check from the end to the begining of the test

Removed
*the consent check at the end of the test

Fixed
* Improve the logic of the Main function and willingness_check so now willingness_check retutn a boolean variable

### Memory Test
Added
* Doc strings to each function to allow the marker/anyone reading the code to understand it easier
* Buttons instead of typing out the answers - making it more accessible to non-native speaking users and prevents the test
  from being too long
* Spaces between the questions and the answer buttons to enhance the program's presentation
* A consent button, coloured red for no and green for yes, to be as clear as possible for the user
  
Changed
* Images were made bigger, as when they were small it was much more difficult to memorise
* Format of code so that all code is imported from a .py file and users only have to run one code chunk in an ipynb file
* Increased size of the text, mainly the questions
* Increased time that the grid is shown before disappearing 
  
Removed
* One image/grid as the test took users too long with 4 different grids
  
Fixed
* Buttons added mean there is no uncertaincy in correct wording for answers
* Sending data about smoking, drinking and occupation to the google forms
* CLearing output of certain bits of data before printing the next so the user does not get confused


### Spatial Reasoning Test
Added
* Docstrings to each function to make code more readable/ understandable
* Progress bar so users are able to identify how far through the test they are
* Box plots and statistics so users can compare their results to previous data
* Small spaces/gaps between certain lines to make program more visually appealing

Changed
* Format of code so that all code is imported from a .py file and users only have to run one code chunk in an ipynb file
* Text at beginning of each question so that it emphasises that the user is choosing the plan that is not a rotation of the 3D arrangement

Fixed
* Issue with window not snapping back to the top after clear_output() is called

### Mathematical Ability Test
Changed
* Format of code so that all code is imported from a .py file and users only have to run one code cell in an ipynb file
* Interface change: the introdcution content, questions to collect user details is centered.
  
Fixed
* the 'def type_check' function for recognize if characters users enter is int or float, if not, users' answer would be recognize as inccorrect.
