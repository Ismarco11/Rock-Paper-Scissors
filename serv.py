from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

from network import Network

Builder.load_string("""
<WaitingScreen>:
    name: 'wait'
    MDLabel:
        text: 'Waiting for a player ...!'
        halign: 'center'
        font_size: '50sp'


    MDIconButton:
        icon: "rock.png"
        user_font_size: "60sp"
        size_hint: None, None
        pos_hint: {"center_x": .25, "center_y": .35}
        on_press: root.manager.current = 'game'

""")

class WaitingScreen(Screen):
    def co(self):
        n = Network()
        player = int(n.getP())
        print("You are player", player)


