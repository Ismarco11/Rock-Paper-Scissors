import pygame
from kivy.properties import ObjectProperty
from kivy.uix import screenmanager
from kivy.uix.button import Button
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
        id: po
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
        id: rock
        icon: "rock.png"
        user_font_size: "60sp"
        size_hint: None, None
        pos_hint: {"center_x": .25, "center_y": .35}
        on_press: 
            root.setlast("Rock")

    MDIconButton:
        icon: "cut.png"
        user_font_size: "60sp"
        size_hint: None, None
        pos_hint: {"center_x": .5, "center_y": .25}
        on_press: 
            root.on_press("Scissors")
            root.setlast("Scissors")

            
    MDIconButton:
        icon: "paper.png"
        user_font_size: "60sp"
        size_hint: None, None
        pos_hint: {"center_x": .75, "center_y": .35}
        on_press:  
            root.on_press("Paper")
            root.setlast("Paper")

            
    MDRectangleFlatButton:
        text: 'Connect'
        pos_hint: {'center_x':0.5,'center_y':0.1}
        on_press: 
            root.on_press("Connect")
            
    

        
"""


class MenuScreen(Screen):
    pass


class GameScreen(Screen):
    c = 0

    def setlast(self, k=0):
        if k == 'Rock':
            self.c = 1
        elif k == 'Scissors':
            self.c = 2
        elif k == 'Paper':
            self.c = 3

    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.getP())
    print("You are player", player)

    def redrawWindow(self, game, p, n):
        if not (game.connected()):
            print("nooooo")
        else:
            move1 = game.get_player_move(0)
            move2 = game.get_player_move(1)
            if game.bothWent():

                if (game.winner() == 1 and p == 1) or (game.winner() == 0 and p == 0):
                    self.ids['po'].text = "YOU WON !!!!!!"
                    return False
                elif game.winner() == -1:
                    self.LockedIn("TIE GAME !!!!!!", sep="po")
                    return False
                else:
                    self.ids['po'].text = "YOU LOST !!!!!!"
                    return False

            else:

                if game.p1Went and p == 0:
                    print(move1)
                    self.LockedIn(move1)
                elif game.p1Went:
                    self.LockedIn("Locked In", sep = 'yourmove')

                if game.p2Went and p == 1:
                    print(move2)
                    self.LockedIn(move2)
                elif game.p2Went:
                    self.LockedIn("Locked In", sep = 'yourmove')



    def se(self, player, game, n):
        if player == 0:
            if not game.p1Went:
                n.send("reset")
        else:
            if not game.p2Went:
                n.send(GameScreen.ids["mymove"].text)

    def start(self, n, player, *largs):

        try:
            game = n.send("get")
        except:
            print("Couldn't get game")
            return None

        if self.c == 0:
            pass
        else:
            if self.c != 0 and game.connected():
                if player == 0:
                    if not game.p1Went:
                        if self.c == 1:
                            n.send("Rock")
                            self.LockedIn("Rock")
                        elif self.c == 2:
                            n.send("Scissors")
                            self.LockedIn("Scissors")

                        elif self.c == 3:
                            n.send("Paper")
                            self.LockedIn("Paper")

                        if game.bothWent():
                            print("d")

                            if (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):
                                self.ids['po'].text = "YOU WON !!!!!!"
                                return False
                            elif game.winner() == -1:
                                self.ids['po'].text = "TIE GAME !!!!!!"
                                return False
                            else:
                                self.ids['po'].text = "YOU LOST !!!!!!"
                                return False



                else:
                    if not game.p2Went:
                        if self.c == 1:
                            n.send("Rock")
                            self.LockedIn("Rock")

                        elif self.c == 2:
                            n.send("Scissors")
                            self.LockedIn("Scissors")

                        elif self.c == 3:
                            n.send("Paper")
                            self.LockedIn("Paper")

                        if game.bothWent():
                            print("d")

                            if (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):
                                self.ids["po"].text = "YOU WON !!!!!!"
                                return False
                            elif game.winner() == -1:
                                self.ids["po"].text = "TIE GAME !!!!!!"
                                return False
                            else:
                                self.ids["po"].text = "YOU LOST !!!!!!"
                                return False


        self.redrawWindow(game, player, n)

    def on_touch_down(self, touch):
        if super(GameScreen, self).on_touch_down(touch):
            return True
        if not self.collide_point(touch.x, touch.y):
            return False
        print((touch.pos))
        return True

    def LockedIn(self, text, sep="mymove"):

        if sep == "po":
            self.ids["po"].text = text
        elif sep == "yourmove":
            self.ids["yourmove"].text = text
        elif sep == "omove":
            self.ids["omove"].text = text
        else:
            self.ids["mymove"].text = text

    def on_press(self, index):
        flash_display_screen = self.manager.get_screen('game')
        setattr(flash_display_screen, 'index', index)
        self.manager.current = 'game'
        if index == "Connect":
            Clock.schedule_interval(partial(self.start, self.n, self.player), 0.5)



sm = ScreenManager()
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(GameScreen(name='game'))


class DemoApp(MDApp):

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

    def build(self):
        screen = Builder.load_string(screen_helper)
        return screen


if __name__ == '__main__':
    DemoApp().run()
