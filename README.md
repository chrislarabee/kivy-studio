# KivyHelper

A suite of pre-built widgets and helper scripts to facilitate building a 
Kivy-based app. 

## Setup

Create and activate a virtual environment:
```
python -m venv venv
venv/Scripts/activate
```

Install the requirements:
```
pip install -r requirements.txt
```

## Configuring Aseprite CLI

To configure the Aseprite CLI so that the tests can run, or in order to
import KivyHelper and make use of the ```build_assets``` script:

For Windows:
* Search for Environment Variables in Windows Search.
* On the System Properties dialogue, click Environment Variables... 
toward the bottom.
* Add a new System variable, name it ```aseprite```, and supply the path
to your Aseprite application folder (not the application itself).
* Click OK to close the Environment Variables dialogue and then the 
System Properties dialogue.
* You can then enter ```aseprite --version``` in a new CLI to make sure 
it works.  
