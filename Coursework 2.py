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

vector = pg.math.Vector2

#Player Properties

PLAYER_ACC = 0.7
PLAYER_FRICTION = -0.15
GRAVITY = 0.4

#player sprite
class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((50,50))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2,0)
        self.pos = vector(WIDTH/2,0)
        self.vel = vector(0,0)
        self.acc = vector(0,0)
                          

    def update(self):
       self.acc = vector(0,GRAVITY)
       #self.vel = vector(0,0)
       keystate = pg.key.get_pressed()
       if keystate[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
       if keystate[pg.K_RIGHT]:
            self.acc.x= PLAYER_ACC
      # if keystate[pg.K_UP]:
        #   self.vel.y = -5
       #if keystate[pg.K_DOWN]:
        #   self.vel.y = 5
        
      #equations of motion
       self.acc.x += self.vel.x * PLAYER_FRICTION  
       self.vel += self.acc
       self.pos += self.vel + (0.5 * self.acc)

       self.rect.midbottom = self.pos

       
       
       if self.pos.x > WIDTH:
          self.pos.x = 0
       if self.pos.x <0:
          self.pos.x = WIDTH

class Platform(pg.sprite.Sprite):
    def __init__(self,x,y,width,height):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((width,height))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

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
        self.platforms = pg.sprite.Group()
        self.player = Player()
        self.all_sprites.add(self.player)
        platform1 = Platform(0,HEIGHT - 30, WIDTH, 30)
        self.all_sprites.add(platform1)
        self.platforms.add(platform1)
        platform2 = Platform(WIDTH/2,HEIGHT/2,150,30)
        self.platforms.add(platform2)
        self.all_sprites.add(platform2)
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
        contacts = pg.sprite.spritecollide(self.player,self.platforms,False)
        if contacts:
            self.player.pos.y = contacts[0].rect.top + 1
            self.player.vel.y = 0
    
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


          

g = Game()
"""player = Player()
all_sprites.add(player)"""
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()
    

pg.quit()


       




