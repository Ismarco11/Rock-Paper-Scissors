import pygame
from kivy.uix import screenmanager
from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.clock import Clock
from functools import partial
from game import Game
from network import Network

screen_helper = """
ScreenManager:
    MenuScreen:
    GameScreen:
<MenuScreen>:
    name: 'menu'
    MDRectangleFlatButton:
        text: 'Click to Play!'
        pos_hint: {'center_x':0.5,'center_y':0.6} 
        on_release:
            root.manager.current = 'game' 
            
        
            
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
        on_press: 
            root.LockedIn("Scissors")
            
            
    MDIconButton:
        icon: "paper.png"
        user_font_size: "60sp"
        size_hint: None, None
        pos_hint: {"center_x": .75, "center_y": .35}
        on_press:  
            root.LockedIn("Paper")
            
    MDRectangleFlatButton:
        text: 'Connect'
        pos_hint: {'center_x':0.5,'center_y':0.1}
        on_press: 
            app.main()
    

        
"""


class MenuScreen(Screen):
    pass


def redrawWindow(game, p):
    if not (game.connected()):
        print("nooooo")
    else:
        print("connected")

        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)
        if game.bothWent():
            pass
        # PROBLEM HERE!!!!!!!!!!
        else:
            if game.p1Went and p == 0:
                GameScreen.LockedIn(move1)
            elif game.p1Went:
                GameScreen.LockedIn("Locked In")
            else:
                GameScreen.LockedIn("Waiting...")

            if game.p2Went and p == 1:
                GameScreen.LockedIn(move2)
            elif game.p2Went:
                GameScreen.LockedIn("Locked In")
            else:
                GameScreen.LockedIn("Waiting...")

    # ScreenManager.current = 'game'


class GameScreen(Screen):
    def LockedIn(self, text):
        self.ids["mymove"].text = text


sm = ScreenManager()
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(GameScreen(name='game'))


def start(n, player, *largs):
    try:
        game = n.send("get")
    except:
        print("Couldn't get game")
        return None

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()

    redrawWindow(game, player)


class DemoApp(MDApp):

    def se(self, n, p, game):
        if p == 0:
            if not game.p1Went:
                n.send(GameScreen.ids["mymove"].text)
        else:
            if not game.p2Went:
                n.send(GameScreen.ids["mymove"].text)

    def con(self):
        run = True
        clock = pygame.time.Clock()
        while run:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    run = False

    def main(self):
        run = True
        clock = pygame.time.Clock()
        n = Network()
        player = int(n.getP())
        print("You are player", player)

        # Clock.schedule_interval(start, 0.5)
        Clock.schedule_interval(partial(start, n, player), 0.5)

    def build(self):
        screen = Builder.load_string(screen_helper)
        return screen


if __name__ == '__main__':
    DemoApp().run()
