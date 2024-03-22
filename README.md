# Cognitive test repository Group 5

This repository contains four cognitive tests used to examine variation in cognitive behaviours. The data obtained using these tests will be used for scientific analyses. The repository includes details on each cognitive test, the method of installation, method of usage, and any changes made to the V.2.0.0 code.

## Cognitive Tests

### ANS Test
Insert description of test

### Memory Test
Insert description of test

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
*
*
*
Changed
*
*
*
Removed
*
*
*
Fixed
*
*
*

### Memory Test
Added
*
*
*
Changed
*
*
*
Removed
*
*
*
Fixed
*
*
*

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
Added
*
*
*
Changed
*
*
*
Removed
*
*
*
Fixed
*
*
*
