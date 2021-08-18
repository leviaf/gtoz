import os

from bs4 import BeautifulSoup
import requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image, AsyncImage
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.stacklayout import StackLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.factory import Factory
from kivy.core.window import Window

url = 'https://gdz.ru/class-9/algebra/kolyagin/'

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Mobile Safari/537.36',
    'accept': '*/*'}
predmets = None


def reqwest(url):
    global HEADERS
    rq = requests.get(url, headers=HEADERS, params=None)
    return rq


parametrs = {}


class Ypr(Screen):
    def clear(self):
        if self.ids['scroll'].children:
            self.ids['scroll'].remove_widget(self.ids['scroll'].children[0])


    def clear_button(self):
        if len(self.ids['main_button'].children) == 2:
            self.ids['main_button'].remove_widget(self.ids['main_button'].children[0])


class MyPopup(Popup):
    def lbl(self, text):

        if self.ids.labels.text == 'error':
            self.ids.labels.text = ''
            self.ids['labels'].text = self.ids['labels'].text + text
        else:
            self.ids['labels'].text = self.ids['labels'].text + text

    def del_one_element_label(self):
        if self.ids['labels'].text == 'error':
            self.ids['labels'].text = ''
        else:
            self.ids['labels'].text = (self.ids['labels'].text)[:-1:]

    def clear(self):
        self.ids['labels'].text = ''

    def otveti(self, namber):
        display = App.get_running_app().root.get_screen('ypr')

        if type(namber) == type('str'):
            namber = namber
        else:

            if namber.text == 'предыдуший номер':
                if namber.text == '1':
                    namber = '1'
                else:
                    namber = str(int(self.ids['labels'].text) - 1)
                    self.ids['labels'].text = str(int(self.ids['labels'].text) - 1)
            else:
                namber = str(int(self.ids['labels'].text) + 1)
                self.ids['labels'].text = str(int(self.ids['labels'].text) + 1)
            display.clear()

        global url

        self.bxlr = BoxLayout(orientation='vertical', size_hint=(1, None), spacing=50, padding=(0, 5, 0, 0))
        self.bxlr.bind(minimum_height=self.bxlr.setter('height'))
        self.boxlayout = BoxLayout(orientation='horizontal', size_hint=(1, .1))


        rq = reqwest(url + namber + '-nom/')
        if rq.status_code == 200:
            html = BeautifulSoup(rq.text, 'html.parser')
            for j in html.find_all('div', class_="with-overtask"):
                img = 'https:' + j.find('img').get("src")

                im = AsyncImage(source=img, size=(Window.width, Window.height - 100), size_hint=(None, None), pos_hint={'center_x': 0.5}, )
                self.bxlr.add_widget(im)

            if len(display.ids['main_button'].children) != 2:
                self.boxlayout.add_widget(Button(text='предыдуший номер', on_press=self.otveti, font_size=25))
                self.boxlayout.add_widget(Button(text='следующий номер', on_press=self.otveti, font_size=25))
                display.ids['main_button'].add_widget(self.boxlayout)

            display.ids['scroll'].add_widget(self.bxlr)
            self.dismiss()
        else:
            self.ids['labels'].text = 'error'


class Subjects(Screen):
    pass


class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(Subjects(name='predmets'))
        sm.add_widget(Ypr(name='ypr'))
        return sm


if __name__ == '__main__':
    MyApp().run()
