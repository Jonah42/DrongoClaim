# DrongoClaim

v1.1

A tool to make UNSW elec payclaims simpler

## What am I?

Submitting elec payclaims is tedious and there is a lot of redundancy in the Microsoft Form. DrongoClaim is a tool that fills out the Microsoft Form for you. It does this by creating a new Chrome user on your computer, and then controlling an instance of Chrome using Selenium. DrongoClaim has a UI developed with Kivy, and allows you to enter your payclaims and save them so that every week you can simply change the dates and submit again.

## Checking your pay submissions

Currently DrongoClaim does some checking of what you are submitting. It will ensure that your zID and names are valid, that you've filled in all required fields for each course and timeslot (which is all of them apart from `notes`), that your start hour <= end hour, and will keep a history of submitted timeslots so you don't accidentally submit the same claim twice. It's up to you to ensure that you've provided valid dates however (as in the date 31/02 doesn't exist but DrongoSim doesn't check this).

## Installation

If you have issues installing it is recommended that you use a virtual environment so you can avoid issues with package versions. See below on how to do this.

### Python

Python 3 is required, I recommend installing 3.7.9 but any recent version should work. You can check the version by running `python --version` in a terminal. If this returns Python 2, try `python3 --version`

### Python Virtual Environment (optional)

A virtual environment serves to give you another python environment which is completely isolated from your global installation. It affects your terminal, not a folder. To make a virtual environment, create a new directory as follows (note you'll need to use python v3 for this, so you may need to use `python3` instead):

`python -m venv drongo`

This creates the directory `drongo` with some folders used to maintain the virtual environment. Navigate into the directory:

`cd drongo`

Now we need to start the virtual environment. In Windows:

`Scripts\activate`

On Mac/Linux:

`source bin/activate`

You should now see `(drongo)` appear to the left of your terminal. Now you should be able to just use `python` (as the venv only knows about python 3).

If you want you can deactivate the virtual environment (although this is probs only useful if you want to use the same terminal to access your global python installation, after using DrongoClaim (I personally cannot think of a reason why you'd do this though - just make a new terminal)):

`deactivate`

You'll need to activate the venv each time you start a terminal. (Maybe writing a shell script/batch file would help but ceebs)

### Clone/Download this repo

Pretty self explanatory, chuck it wherever you'd like (just remember you'll need to activate the virtual environment so maybe put it somewhere near that)

### Python Libraries

To install all the dependencies (except Kivy, covered in the next section) simply run:

`pip install -r requirements.txt`

### Kivy

Kivy is the UI framework used in DrongoClaim.

You will need to install the kivy pre release version (needed for windows scroll fix). Run the following commands in a terminal:

`python -m pip install kivy --pre --no-deps --index-url  https://kivy.org/downloads/simple/`

`python -m pip install kivy[base] --pre --extra-index-url https://kivy.org/downloads/simple/`

### Chrome

DrongoClaim uses Chrome to submit your payclaims. Make sure you have installed Chrome and it is up to date (there will be an update button at the top-right of Chrome if you need to update). 

Note that DrongoClaim uses a ChromeDriver in order to control Chrome. This ChromeDriver is specific to a version of Chrome. You can find out your version of Chrome by going to `chrome://version/` in Chrome. If for some reason you need to use a different version of the ChromeDriver, you can find all versions here `https://chromedriver.chromium.org/downloads`. Note that the ChromeDriver is different for Mac/Windows/Linux, it can be found under `driver/<OS>`. DrongoClaim automatically detects which OS you are on and uses the appropriate driver. Hopefully the existing driver in the repo will work for you though.

## Usage

To start DrongoClaim, from a terminal in the `DrongoClaim` folder, run:

`python DrongoClaim.py`

The first time you run DrongoClaim you will be asked to enter your zID and name. Please get this right, at the moment there is no way to update this information (coming soon though!).

In DrongoClaim you'll be able to add courses (and specify the course + lecturer), add slots within each course (1 per lab slot, you can have as many per day as you like), and save this information. Make sure you fill out every field (apart from the `Note` field, which is optional). When you hit submit, the info shown on DrongoClaim is sent to a backend process that starts up a Chrome instance (which you'll see). This instance is new, and as such you'll be prompted to login to Microsoft in order to access the Microsoft Form. Hit `Yes` for Microsoft to remember you so DrongoClaim doesn't have to try log in everytime (Chrome stores your deets, not DrongoClaim). From there, DrongoClaim takes the wheel and you can sit back and relax as your payclaims are submitted. Chrome will close when its finished.

By default you are sent an email with your responses for each payclaim so you have a record of what DrongoClaim has done. (DrongoClaim history is a todo)

If you are submitting a one-off payclaim it is suggested you don't save it, rather ask DrongoClaim to save your regular hours so the only thing you have to do is change the date


## Troubleshooting

Please note this has not been tested on Mac - it should work though. If you use DrongoClaim on a Mac please let me know how it goes!

At this point the best way to work out what is going wrong is to email me with the error message from the terminal/DrongoClaim and any relevant screenshots/context. Most errors should be appropriately handled by DrongoClaim.

## Contact

Let me know if you have any suggestions or feedback! (And of course if you find a bug) :-)

`jmeggs@outlook.com.au`

## Changelog

v1.2: Added Inma for 1111 peeps :-). Also venv explanation.
v1.1: Added feedback to buttons, implemented better data checking and submission history management, and added better error handling so it shouldn't crash to the terminal

## TODO

 - Better size management on mac
 - Access readable history