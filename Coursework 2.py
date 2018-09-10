# Import the pygame library and initialise the game engine
import pygame as pg
import random
from pygame import *


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
FONT_NAME ="arial"

vector = pg.math.Vector2

#Player Properties

PLAYER_ACC = 0.9
PLAYER_FRICTION = -0.15
GRAVITY = 0.4
PLAYER_JUMP = 12

#Starting Platforms



#player sprite
class Player(pg.sprite.Sprite):
    def __init__(self,game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface((30,30))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (800,100)
        self.pos = vector(800,100)
        self.vel = vector(0,0)
        self.acc = vector(0,0)

    def jump(self):
        #Jump allowed if on a platform
        contacts = pg.sprite.spritecollide(self,self.game.platforms,False)
        if contacts:

            self.vel.y = -PLAYER_JUMP
        
                          

    def update(self):
       self.acc = vector(0,GRAVITY)
       #self.vel = vector(0,0)
       keystate = pg.key.get_pressed()
       if keystate[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
       if keystate[pg.K_RIGHT]:
            self.acc.x= PLAYER_ACC

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
        self.font_name = pg.font.match_font(FONT_NAME)

    def new(self):
        #starts new game
        self.score = 0
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)

        x = y = 0

        PLATFORM_LIST =[
      "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
    "P                                            P                                                           P",
    "P                                            PPPPPPPPPPPPPPPPPPP                                          P",
    "P                                            P                                                           P",
    "P                                            P                                                            P",
    "P            PPPPPPPPPPPPP                   P                PPPPPP                      PPPPP           P",
    "P            P                                                                               P           P",
    "P            P              PPPP                                                             P           P",
    "P            P                      PPPP                               PPPPPP                P           P",
    "P            P                PPPP      PPPP                                PPPPPPPPP        P           P",
    "P            P                                   PPPPPPPPPPPP                                P           P",
    "P            P                         PPPPPPPPP                                                     P           P",
    "PPPPPP       P     PPPPP     PPPPPPPPP                                                            P           P",
    "P            P        P                PPPPPPPP                                           P           P",
    "P      PPPPP P        P        PPPP                    PPPPPPPPPPPPPPPPPPPPPPP   P             P           P",
    "P            P        P             PPPPPP                                             P             P           P",
    "P       PPPPPP        P   PPPPPPPPPPP                  PPPPPPPPPPPPPPPPPPPPPPP   P             P           P",
    "P            P        P                                                      P   P             P           P",
    "P            P    PPPPPPPPPP      PPPPPPPPPPPP              PPPPPPPPPPPP     P   P             P           P",
    "P            P                                              P                P   P             P          P",
    "P            P     PPPPPPPPP                                PPPPPPPPP   PPPPPP   PPPPPPPPPPP   P          P",
    "P            P                                                                                           P",
    "P                           PPPPPP      P    P                                                           P",
    "P                                       P    P                 PPPPPP   PPPPPP       PPPPPPPPPPPP        P",
    "P                                       P    P                                                           P",
    "P            P     PPPPPPPPPPPPPPPPPPPPPP    PPPPPPPPPPPPPP         PPPPPPPP                 P           P",
    "P            P                                                                               P           P",
    "P            P                                                               PPPPPPPPP                   P",
    "P            PPPPPPPPPPPPPPPP    p    PPPPPPPP                                               P           P",
    "P            P                   P    P      PPPPP            PPPPPPPPP                      P           P",
    "PPPPPPPP     P                   P    P  P         PPPP                                       P           P",
    "P            P        PPPP       P    P  P             PPPP                 PPPPPPP           P           P",
    "P       PPPPPPPPPP               P    P  P                PPPP                                            P",
    "P          P           PPPPP     P    P  P                        PPPPPPPP                                P",
    "PPPPPPPP   P   P                 P    P  P   PPPPPPPPPP                                PPPPP               P",
    "P          P   P   PPPPPP        P    P  P      P                                    PPPP   P              P",
    "P    PPPPPPP   P                                P  P            PPPPPPPPPPPPPPPPPP  PPP                    P",
    "P              P                      PPP          P                             P  P                      P",
    "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",]
        map_length = len(PLATFORM_LIST[0]) * 20
        map_width = len(PLATFORM_LIST) * 20
        for row in PLATFORM_LIST:
          for col in row:
            if col =="P":
                P = Platform(x,y,50,50)
                self.all_sprites.add(P)
                self.platforms.add(P)
            x += 50
          y += 50
          x = 0
        
        

        
        """(-5*WIDTH,HEIGHT - 30, WIDTH*10, 30),
                 (WIDTH/2,HEIGHT/2,150,30),
                 (40,HEIGHT *3/4,50,30),
                 (300,HEIGHT - 150,90,30),
                 (900,HEIGHT-400,200,30),"""


        """ for plat in PLATFORM_LIST:
            platf = Platform(*plat)
            self.all_sprites.add(platf)
            self.platforms.add(platf) """
            
            
       
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
        # Check if player hits platform iff falling
        if self.player.vel.y > 0:
            contacts = pg.sprite.spritecollide(self.player,self.platforms,False)
            if contacts:
                self.player.pos.y = contacts[0].rect.top + 1
                self.player.vel.y = 0
                
        # Vertical Scroll
        if self.player.rect.top <= (HEIGHT / 8):
            self.player.pos.y += abs(self.player.vel.y)
            for plat in self.platforms:
                plat.rect.y += abs(self.player.vel.y)              

        if self.player.rect.bottom >= (HEIGHT *3/8):
            self.player.pos.y -= self.player.vel.y
            for plat in self.platforms:
                plat.rect.y -= self.player.vel.y

        #horizontal scroll

        if self.player.rect.left <= (WIDTH/ 4):
            self.player.pos.x -= self.player.vel.x
            for plat in self.platforms:
                plat.rect.x -= self.player.vel.x

        if self.player.rect.right >= (WIDTH *3/4):
            self.player.pos.x -= self.player.vel.x
            for plat in self.platforms:
                plat.rect.x -= self.player.vel.x
            

        
            
    
    def events(self):
        #game loop - events
        for event in pg.event.get():
         if event.type == pg.QUIT:
            if self.playing:
                self.playing = False
            self.running = False
         if event.type ==pg.KEYDOWN:
             if event.key == pg.K_UP:
                 self.player.jump()
            
             
    def draw(self):
        #game loop - draw
         self.screen.fill(WHITE)
         self.all_sprites.draw(self.screen)
         self.draw_text(str(self.score),20,BLACK,30,30)
         #Flip display after drawing
         pg.display.flip()
    def show_start_screen(self):
        #game start screen
        pass
    def show_go_screen(self):
        #game over or continue
        pass

    def draw_text(self,text,size,colour,x,y):
        font = pg.font.Font(self.font_name,size)
        text_surface = font.render(text,True,colour)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x,y)
        self.screen.blit(text_surface,text_rect)
    


          

g = Game()
"""player = Player()
all_sprites.add(player)"""
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()
    

pg.quit()


       




