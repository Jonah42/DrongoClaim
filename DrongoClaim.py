from kivy.app import App
from kivy.base import runTouchApp
from kivy.lang import Builder
from kivy.properties import ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.core.text import LabelBase
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.clock import Clock

from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.properties import StringProperty, DictProperty, ListProperty

from functools import partial

import time
import random
import pickle
import re
import submit_hours

class WelcomeScreen(Screen):
    # def loadData(data, *largs):
    #     print(data)

    # Clock.schedule_once(partial(loadData, 'self.manager.data'))
    pass

class ClaimScreen(Screen):
    pass

class DrongoLabel(Label):
    pass

class DrongoButton(Button):
    regular_normal = [0x38/255,0xb6/255,0xff/255,1]
    regular_pressed = [0x52/255,0x71/255,0xff/255,1]
    submit_normal = [0x3c/255,0xb0/255,0x4c/255,1]
    submit_pressed = [0x00/255,0x80/255,0x37/255,1]
    normal = regular_normal
    pressed = regular_pressed
    button_color = ListProperty(normal)
    def load_colours(self, normalColour, pressedColour):
        self.normal = normalColour
        self.pressed = pressedColour
        self.button_color = self.normal

class DropDownButton(Button):
    pass

class DateDropDown(BoxLayout):
    pass

class TimeDropDown(BoxLayout):
    pass

class InputWrapper(BoxLayout):
    pass

class DrongoInput(TextInput):
    pass

class SubjectList(BoxLayout):
    def addSubject(self):
        self.add_widget(Subject(), 1)
    def removeSubject(self, child):
        self.remove_widget(child)
    def loadData(self, data):
        for course in reversed(data['courses']):
            newSubject = Subject()
            newSubject.courseHeader.course.text = course['code']
            newSubject.courseHeader.lecturer.text = course['lecturer']
            for slot in reversed(course['slots']):
                newSlot = ClaimSlot()
                # print(newSlot.children)
                newSlot.day.text = slot['day']
                newSlot.date.date.text = slot['date']
                newSlot.date.month.text = slot['month']
                newSlot.startTime.hour.text = slot['startHour']
                newSlot.startTime.minute.text = slot['startMin']
                newSlot.endTime.hour.text = slot['endHour']
                newSlot.endTime.minute.text = slot['endMin']
                newSlot.duty.text = slot['duty']
                newSlot.note.text = slot['note']
                newSubject.add_widget(newSlot, 1)
            self.add_widget(newSubject, 1)

class Subject(BoxLayout):
    def addSlot(self):
        self.add_widget(ClaimSlot(), 1)
    def removeSlot(self, child):
        self.remove_widget(child)

class ClaimSlot(BoxLayout):
    pass

class MyScreenManager(ScreenManager):
    data = DictProperty({
        'firstName': '',
        'lastName': '',
        'zid': '',
        'courses': []
    })
    try:
        with open('data.txt', 'rb') as f:
            data = pickle.load(f)
    except FileNotFoundError:
        pass
    def new_colour_screen(self):
        name = str(time.time())
        s = ColourScreen(name=name,
                         colour=[random.random() for _ in range(3)] + [1])
        self.add_widget(s)
        self.current = name
    def saveDetails(self, zid, firstName, lastName):
        # TODO: additional parsing to ensure correctness of zid and names
        res = re.search("z\d{7}", zid)
        popupContent = BoxLayout(orientation='vertical')
        popupLabel = DrongoLabel()
        popupButton = DrongoButton(text='Ok', size_hint=(0.5,0.25), pos_hint={'center_x': 0.5})
        popupContent.add_widget(popupLabel)
        popupContent.add_widget(popupButton)
        popup = Popup(title='Zut!', content=popupContent, size_hint=(0.5,0.5), title_font='open-sans', background='white.png', title_color=(0,0,0,1))
        popupButton.bind(on_release=popup.dismiss)
        res and print(res[0])
        if res == None or len(zid) != 8:
            popupLabel.text = 'Incorrect zID. Must be of the form zXXXXXXX'
            popup.open()
        elif firstName == '':
            popupLabel.text = 'Please enter a first name'
            popup.open()
        elif lastName == '':
            popupLabel.text = 'Please enter a last name'
            popup.open()
        else:
            self.data['zid'] = zid
            self.data['firstName'] = firstName
            self.data['lastName'] = lastName
            self.current = 'claim-screen'
    def saveData(self, subjectList):
        self.data['courses'] = extractData(subjectList, False)
        try:
            with open('data.txt', 'wb') as f:
                pickle.dump(dict(self.data), f)
            popupContent = BoxLayout(orientation='vertical')
            popupLabel = DrongoLabel(text='Successfully saved!')
            popupButton = DrongoButton(text='Muy bien!!', size_hint=(0.5,0.25), pos_hint={'center_x': 0.5})
            popupContent.add_widget(popupLabel)
            popupContent.add_widget(popupButton)
            popup = Popup(title='Info', content=popupContent, size_hint=(0.5,0.5), title_font='open-sans', background='white.png', title_color=(0,0,0,1))
            popupButton.bind(on_release=popup.dismiss)
            popup.open()
        except Exception as e:
            popupContent = BoxLayout(orientation='vertical')
            popupLabel = DrongoLabel(text='Error saving :-(')
            popupButton = DrongoButton(text='Ok', size_hint=(0.5,0.25), pos_hint={'center_x': 0.5})
            popupContent.add_widget(popupLabel)
            popupContent.add_widget(popupButton)
            popup = Popup(title='Zut!', content=popupContent, size_hint=(0.5,0.5), title_font='open-sans', background='white.png', title_color=(0,0,0,1))
            popupButton.bind(on_release=popup.dismiss)
            popup.open()
    def submitClaims(self, subjectList):
        # button.my_color = [0x3c/255,0xb0/255,0x4c/255,1]
        try:
            self.data['courses'] = extractData(subjectList, True)
            submit_hours.submit(self.data)
            popupContent = BoxLayout(orientation='vertical')
            popupLabel = DrongoLabel(text='Successfully submitted!')
            popupButton = DrongoButton(text='Muy bien!!', size_hint=(0.5,0.25), pos_hint={'center_x': 0.5})
            popupContent.add_widget(popupLabel)
            popupContent.add_widget(popupButton)
            popup = Popup(title='Info', content=popupContent, size_hint=(0.5,0.5), title_font='open-sans', background='white.png', title_color=(0,0,0,1))
            popupButton.bind(on_release=popup.dismiss)
            popup.open()
        except Exception as e:
            popupContent = BoxLayout(orientation='vertical')
            popupLabel = DrongoLabel(text=e.args[0], size_hint=(1,0.75))
            popupLabel.bind(width=lambda *x: popupLabel.setter('text_size')(popupLabel, (popupLabel.width, None)), texture_size=lambda *x: popupLabel.setter('height')(popupLabel, popupLabel.texture_size[1]))
            popupButton = DrongoButton(text='Ok', size_hint=(0.5,0.25), pos_hint={'center_x': 0.5})
            popupContent.add_widget(popupLabel)
            popupContent.add_widget(popupButton)
            popup = Popup(title='Zut!', content=popupContent, size_hint=(0.5,0.5), title_font='open-sans', background='white.png', title_color=(0,0,0,1))
            popupButton.bind(on_release=popup.dismiss)
            popup.open()

class DrongoClaimApp(App):
    def build(self):
        return MyScreenManager()

def extractData(subjectList, check):
    submittedTimes = []
    try:
        with open('submitted.txt', 'rb') as f:
            submittedTimes = pickle.load(f)
    except FileNotFoundError:
        pass
    newCourses = []
    for i in range(1, len(subjectList.children)):
        newCourse = {
            'code': subjectList.children[i].courseHeader.course.text,
            'lecturer': subjectList.children[i].courseHeader.lecturer.text,
            'slots': []
        }
        if check:
            if newCourse['code'] == 'Course':
                raise Exception('Course code missing! Please select a course')
            if newCourse['lecturer'] == 'Lecturer':
                raise Exception('Lecturer missing! Please select a lecturer')
        for j in range(1, len(subjectList.children[i].children)-1):
            newSlot = {
                'day': subjectList.children[i].children[j].day.text,
                'date': subjectList.children[i].children[j].date.date.text,
                'month': subjectList.children[i].children[j].date.month.text,
                'startHour': subjectList.children[i].children[j].startTime.hour.text,
                'startMin': subjectList.children[i].children[j].startTime.minute.text,
                'endHour': subjectList.children[i].children[j].endTime.hour.text,
                'endMin': subjectList.children[i].children[j].endTime.minute.text,
                'duty': subjectList.children[i].children[j].duty.text,
                'note': subjectList.children[i].children[j].note.text
            }
            if check:
                # Check user has filled out all required fields
                if newSlot['day'] == 'Day':
                    raise Exception('Day missing! Please select a day')
                if newSlot['date'] == 'DD' or newSlot['month'] == 'MM':
                    raise Exception('Date incomplete! Please select a date')
                if newSlot['startHour'] == 'hh' or newSlot['startMin'] == 'mm':
                    raise Exception('Start time incomplete! Please select a start time')
                if newSlot['endHour'] == 'hh' or newSlot['endMin'] == 'mm':
                    raise Exception('End time incomplete! Please select an end time')
                if newSlot['duty'] == 'Duty':
                    raise Exception('Duty missing! Please select a duty')
                if int(newSlot['startHour']) > int(newSlot['endHour']):
                    raise Exception('Slot ends before it starts. Please fix the start and end times')
                # Check that user has not yet submitted a claim for this particular time
                newTime = newSlot['date']+newSlot['month']+newSlot['startHour']+newSlot['startMin']+newSlot['endHour']+newSlot['endMin']
                if newTime in submittedTimes:
                    raise Exception(f"Detected you've already submitted a claim for {newSlot['date']}/{newSlot['month']} from {newSlot['startHour']}:{newSlot['startMin']} to {newSlot['endHour']}:{newSlot['endMin']}. Please check you have not submitted this. To override this warning (and erase your submission history) delete submitted.txt in the root directory of DrongoClaim")
            newCourse['slots'].append(newSlot)
        newCourses.append(newCourse)
    return newCourses

LabelBase.register(name='open-sans', fn_regular='./OpenSans/OpenSans-Light.ttf') 

DrongoClaimApp().run()
