# basic trace statistics
## Table of contents
* [Introduction](#introduction)
* [Technologies](#technologies)
* [Functionalities](#functionalities)
* [Setup](#setup)
## Introduction
The project concerns the analysis of the basic parameters for data derived from the motion of an undefined particle. It could be useful for example in biotechnology or space industry. Software is prepared to generate basic statistics of drawn trace. The tool includes appropriate class for data analysis, documentation and unit tests. 
## Technologies
Project is created with Python 3.7 and:
- **Pandas 1.3.2**, **Matplotlib 3.4.3** libraries for data analysis and visualization of results
- **unittest** for implementing unit tests
Other necessary information about libraries used and their versions can be found in the *requirements.txt* file.
## Functionalities
Based on coordinates (x,y) from input data, methods allow to obtain:
- processing of the signal into a necessary sampling rate,
- conversion into different unit systems and reference frame,
- calculation of the mean velocity, center of mass(COM) and distance between COM and predefined points,
- visualisation of the trace, center of mass and predefined points.
## Setup
To run this project install it locally by copy repository. To use the tool, please run the *class_trace.py* script. The test implementation and the necessary test data are available in the *tests* folder. Graphs obtained by running the program are saved in the *reports* folder. The paths to the input data and reports are included in the file *settings.py*.
