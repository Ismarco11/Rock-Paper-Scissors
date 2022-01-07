from kivy.properties import StringProperty
from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

import socket

Builder.load_string("""
<ClientScreen>:
    id: c_screen
    name: 'Client Screen'
""")


class ClientScreen(Screen):
    ip = StringProperty("")

    def __init__(self, *args, **kwargs):
        super(ClientScreen.self).__init__(*args, **kwargs)

        self.ip = socket.gethostbyname(socket.gethostname())
        print(self.ip)
