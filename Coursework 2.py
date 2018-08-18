# Import the pygame library and initialise the game engine
import pygame as pg
import random


#settings
# Define some colors (for now)
BLACK = ( 0, 0, 0)
WHITE = ( 255, 255, 255)
GREEN = ( 0, 255, 0)
RED = ( 255, 0, 0)
BLUE = (0,0,255)

WIDTH = 1024
HEIGHT = 500

TITLE="Game"

class Game:
    def __init__(self):
        #intialises game window etc
        pg.init()
        self.screen = pg.display.set_mode((WIDTH,HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True

    def new(self):
        #starts new game
        self.all_sprites = pg.sprite.Group()
        self.run()
        
    def run(self):
        #game loop
        self.playing = True
        while self.playing:
         self.clock.tick(60)
         self.events()
         self.update()
         self.draw()
        
         
    def update(self):
        #game loop - update
        self.all_sprites.update()
    
    def events(self):
        #game loop - events
        for event in pg.event.get():
         if event.type == pg.QUIT:
            if self.playing:
                self.playing = False
            self.running = False
             
    def draw(self):
        #game loop - draw
         self.screen.fill(WHITE)
         self.all_sprites.draw(self.screen)
         #Flip display after drawing
         pg.display.flip()
    def show_start_screen(self):
        #game start screen
        pass
    def show_go_screen(self):
        #game over or continue
        pass

#player sprite
"""class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((50,50))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (25,HEIGHT - 25)

    def update(self):
       self.speedx = 0
       self.speedy = 0
       keystate = pg.key.get_pressed()
       if keystate[pg.K_LEFT]:
            self.speedx = -5
       if keystate[pg.K_RIGHT]:
            self.speedx= 5
       if keystate[pg.K_UP]:
           self.speedy = -5
       if keystate[pg.K_DOWN]:
           self.speedy = 5

       self.rect.y += self.speedy     
       self.rect.x += self.speedx
       
       if self.rect.right > WIDTH:
          self.rect.right = WIDTH
       if self.rect.left <0:
          self.rect.left = 0 """
          

g = Game()
"""player = Player()
all_sprites.add(player)"""
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()
    

pg.quit()


       




