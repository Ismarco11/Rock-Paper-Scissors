import pygame
from kivy.uix import screenmanager
from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition

from game import Game
from network import Network

from game_screen import ClientScreen

screen_helper = """
ScreenManager:
    MenuScreen:
    WaitingScreen:
    GameScreen:
<MenuScreen>:
    name: 'menu'
    MDRectangleFlatButton:
        text: 'Click to Play!'
        pos_hint: {'center_x':0.5,'center_y':0.6} 
        on_press: 
            root.manager.current = 'wait'
        
            
                   

<WaitingScreen>:
    name: 'wait'
    
    MDLabel:
        text: 'Waiting for a player ...!'
        halign: 'center'
        font_size: '50sp'


    MDIconButton:
        name: 'k'
        icon: "rock.png"
        user_font_size: "60sp"
        size_hint: None, None
        pos_hint: {"center_x": .25, "center_y": .35}
        on_press: root.manager.current = 'game'


<GameScreen>:
    name: 'game'
    MDLabel:
        text: 'Your Move!'
        pos_hint: {"center_x": 0.5, "center_y": .8}
        halign: 'center'

    MDLabel:
        id: mymove
        text: 'Waiting...'
        pos_hint: {"center_x": 0.5, "center_y": .7}
        halign: 'center'

    MDLabel:
        id: omove
        text: 'Opponent Move!'
        pos_hint: {"center_x": 0.5, "center_y": .6}
        halign: 'center'

    MDLabel:
        id: yourmove
        text: 'Waiting...'
        pos_hint: {"center_x": 0.5, "center_y": .5}
        halign: 'center'

    MDIconButton:
        icon: "rock.png"
        user_font_size: "60sp"
        size_hint: None, None
        pos_hint: {"center_x": .25, "center_y": .35}
        on_press: 
            root.LockedIn("Rock")
            text = 'good'

    MDIconButton:
        icon: "cut.png"
        user_font_size: "60sp"
        size_hint: None, None
        pos_hint: {"center_x": .5, "center_y": .25}
        on_press: root.LockedIn("Scissors")

    MDIconButton:
        icon: "paper.png"
        user_font_size: "60sp"
        size_hint: None, None
        pos_hint: {"center_x": .75, "center_y": .35}
        on_press: root.LockedIn("Paper")

    MDRectangleFlatButton:
        text: 'Back'
        pos_hint: {'center_x':0.5,'center_y':0.1}
        on_press: root.manager.current = 'menu'

"""


class MenuScreen(Screen):
    run = True
    clock = pygame.time.Clock()


def redrawWindow(sm, game, p):
    if not (game.connected()):
        sm.current = 'wait'
    else:
        sm.current = 'game'

        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)


class WaitingScreen(Screen):
    def switch_next(self, *args):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = self.manager.next()

    def on_enter(self, **kwargs):
        print(self.manager.next())
        print('hello')
        n = Network()
        player = int(n.getP())
        print("You are player", player)
        run = True
        clock = pygame.time.Clock()
        while run:
            clock.tick(60)
            try:
                game = n.send("get")
            except:
                # run = False
                print("Couldn't get game")
                break

            if game.bothWent():
                print("ddtr")
                if not (game.connected()):
                    print("ff")
                else:
                    print("well done")
                    self.manager.current = 'game'
                # redrawWindow(sm, game, player)
                pygame.time.delay(500)
                try:
                    game = n.send(("reset"))
                except:
                    run = False
                    print("Couldn't get game")
                    break
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()

                    if GameScreen.ids["mymove"].text in ["Rock", "Paper", "cut"] and game.connected():
                        if player == 0:
                            if not game.p1Went:
                                n.send(GameScreen.ids["mymove"].text)
                        else:
                            if not game.p2Went:
                                n.send(GameScreen.ids["yourmove"].text)

            if not (game.connected()):
                print("ff")
                # self.manager.current = 'wait'
            else:
                print("well done")
                if player == 1:
                    self.manager.current = 'game'
                else:
                    self.manager.current = 'game'


class GameScreen(Screen):
    def LockedIn(self, text):
        self.ids["mymove"].text = text


# Create the screen manager

sm = ScreenManager()
sm.add_widget(MenuScreen(name='menu'))
# sm.add_widget(WaitingScreen())
sm.add_widget(WaitingScreen(name='wait'))
sm.add_widget(GameScreen(name='game'))


def change_screen(k):
    sm.current = k


class DemoApp(MDApp):

    def build(self):
        screen = Builder.load_string(screen_helper)
        return screen


if __name__ == '__main__':
    DemoApp().run()
