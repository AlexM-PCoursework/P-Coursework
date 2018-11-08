# Import the pygame library and initialise the game engine
import pygame as pg
import random
from pygame import *
from os import path
from random import randrange


#settings
# Define some colors (for now)
BLACK = ( 0, 0, 0)
WHITE = ( 255, 255, 255)
GREEN = ( 0, 255, 0)
RED = ( 255, 0, 0)
BLUE = (0,0,255)
WATERM = 253,91,120
BG_COLOUR = 48,191,191
GOLD = 255,215,0

WIDTH = 1024
HEIGHT = 500

TITLE="Game"
FONT_NAME ="arial"

hs_file = "hs.txt"

vector = pg.math.Vector2

#Player Properties

PLAYER_ACC = 0.9
PLAYER_FRICTION = -0.15
GRAVITY = 0.4
PLAYER_JUMP = 9

#Starting Platforms



#player sprite
class Player(pg.sprite.Sprite):
    def __init__(self,game):
        self.groups=game.all_sprites
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.image = pg.Surface((30,30))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (800,100)
        self.pos = vector(800.2,100)
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
       if abs(self.vel.x) < 0.1:
           self.vel.x = 0
       self.pos += self.vel + (0.5 * self.acc)

       self.rect.midbottom = self.pos

       
       
       if self.pos.x > WIDTH:
          self.pos.x = 0
       if self.pos.x <0:
          self.pos.x = WIDTH

class Platform(pg.sprite.Sprite):
    def __init__(self,game,x,y,width,height):
        self.groups = game.all_sprites,game.platforms
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.image = pg.Surface((width,height))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        if randrange (100) < 15:
            Coin(self.game,self)

class Coin(pg.sprite.Sprite):
    def __init__(self,game,plat):
        self.groups = game.all_sprites, game.coins
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.plat = plat
        self.image = pg.Surface((15,15))
        self.image.fill(GOLD)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx
        self.rect.bottom = self.plat.rect.top - 5

    def update(self):
     self.rect.bottom = self.plat.rect.top - 5
       

class Game:
    def __init__(self):
        #intialises game window etc
        pg.init()
        self.screen = pg.display.set_mode((WIDTH,HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.data()

    def data(self):
        #load highest Round
        self.dir = path.dirname(__file__)
        with open(path.join(self.dir,hs_file),'w') as file:
            try:
                self.highscore = int(file.read())
            except:
                self.highscore = 0

    def new(self):
        #starts new game
        self.score = 0
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        self.round = 1

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
                Platform(self,x,y,50,40)
                
            x += 50
          y += 40
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
                lowest = contacts[0]
                for contact in contacts:
                    if contact.rect.bottom > lowest.rect.bottom:
                        lowest = contact
                    
                if self.player.pos.y < lowest.rect.centery:
                  self.player.pos.y = lowest.rect.top + 1
                  self.player.vel.y = 0
                
        # Vertical Scroll
        if self.player.rect.top <= (HEIGHT / 8):
            self.player.pos.y -= self.player.vel.y
            for plat in self.platforms:
                plat.rect.y -= self.player.vel.y
            for coin in self.coins:
                coin.rect.y -=self.player.vel.y
            


        if self.player.rect.bottom >= (HEIGHT *3/8):
            self.player.pos.y -= self.player.vel.y
            for plat in self.platforms:
                plat.rect.y -= self.player.vel.y
            for coin in self.coins:
                coin.rect.y -=self.player.vel.y

        # check if player hits coins

        coin_contact = pg.sprite.spritecollide(self.player,self.coins,True)
        for coin in coin_contact:
            self.score += 1
            


        #horizontal scroll

        if self.player.rect.left <= (WIDTH/ 4):
            self.player.pos.x -= self.player.vel.x
            for plat in self.platforms:
                plat.rect.x -= self.player.vel.x
            for coin in self.coins:
                coin.rect.x -=self.player.vel.x
            

        if self.player.rect.right >= (WIDTH *3/4):
            self.player.pos.x -= self.player.vel.x
            for plat in self.platforms:
                plat.rect.x -= self.player.vel.x
            for coin in self.coins:
                coin.rect.x -=self.player.vel.x

   
            


        

        
            

        
            
    
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
         self.draw_text(str(self.score),50,RED,30,30)
         self.draw_text("ROUND: "+str(self.round),30,BLACK,WIDTH - 150 ,20)
         #Flip display after drawing
         pg.display.flip()
    def show_start_screen(self):
        #game start screen
        self.screen.fill(BG_COLOUR)
        self.draw_text(TITLE,50,RED,WIDTH/2,HEIGHT/3)
        self.draw_text("Use arrows to move, UP arrow to jump",30, RED,WIDTH/3,HEIGHT/2)
        self.draw_text("Press any key to play",20,GREEN, WIDTH/2,HEIGHT* 2/3)
        self.draw_text("Highest Round: " + str(self.highscore),20,RED, WIDTH/3,HEIGHT *3/4)
        pg.display.flip()
        self.key_press()
    
    def show_go_screen(self):
        #game over or continue
        if not self.running:
            return
        self.screen.fill(BG_COLOUR)
        self.draw_text("GAME OVER",50,RED,WIDTH/2,HEIGHT/3)
        self.draw_text("You got to round " + str(self.round),30, RED,WIDTH/3,HEIGHT/2)
        self.draw_text("Press any key to play again",20,GREEN, WIDTH/2,HEIGHT* 2/3)
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("NEW HIGH ROUND!", 30, WHITE, WIDTH/2,HEIGHT/4)
            with open(path.join(self.dir,hs_file),'w') as file:
                file.write(str(self.score))
        else:
           self.draw_text("Highest Round: " + str(self.highscore),20,RED, WIDTH/3,HEIGHT *3/4)
        pg.display.flip()
        self.key_press()

    def draw_text(self,text,size,colour,x,y):
        font = pg.font.Font(self.font_name,size)
        text_surface = font.render(text,True,colour)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x,y)
        self.screen.blit(text_surface,text_rect)

    def key_press(self):
        not_pressed = True
        while not_pressed:
            self.clock.tick(60)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    not_pressed = False
                    self.running = False
                if event.type == pg.KEYUP:
                    not_pressed = False
        
    


          

g = Game()
"""player = Player()
all_sprites.add(player)"""
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()
    

pg.quit()


       




