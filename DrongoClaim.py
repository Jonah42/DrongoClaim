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
from kivy.properties import StringProperty, DictProperty

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
    pass

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
        popupButton.bind(on_press=popup.dismiss)
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
        # Do much more checking :grimace:
        self.data['courses'] = extractData(subjectList)
        with open('data.txt', 'wb') as f:
            pickle.dump(dict(self.data), f)
    def submitClaims(self, subjectList):
        # Do much more checking :grimace:

        self.data['courses'] = extractData(subjectList)
        submit_hours.submit(self.data)

class DrongoClaimApp(App):
    def build(self):
        return MyScreenManager()

def extractData(subjectList):
    newCourses = []
    for i in range(1, len(subjectList.children)):
        newCourse = {
            'code': subjectList.children[i].courseHeader.course.text,
            'lecturer': subjectList.children[i].courseHeader.lecturer.text,
            'slots': []
        }
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
            newCourse['slots'].append(newSlot)
        newCourses.append(newCourse)
    return newCourses

LabelBase.register(name='open-sans', fn_regular='./OpenSans/OpenSans-Light.ttf') 

DrongoClaimApp().run()
