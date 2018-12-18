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
HEIGHT = 720

TITLE="Game"
FONT_NAME ="arial"

hs_file = "hs.txt"

vector = pg.math.Vector2

#Player Properties

PLAYER_ACC = 1.2
PLAYER_FRICTION = -0.25
GRAVITY = 0.5
PLAYER_JUMP = 12

BULLET_SPEED = 40
BULLET_LIFETIME = 1000
BULLET_RATE = 150

ENEMY_1_IMG = 'ghost.png'
ENEMY1_SPEED = 0.03
ENEMY1_FRICTION = -0.02

class Bullet(pg.sprite.Sprite):
    def __init__(self,game,pos,dir):
        self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self,self.groups)
        self.image = pg.Surface((10,10))
        self.game = game
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.pos = pos
        self.vel = dir * BULLET_SPEED
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        self.pos += self.vel
        self.rect.center = self.pos
        if pg.sprite.spritecollideany(self,self.game.walls):
            self.kill()
        if pg.sprite.spritecollideany(self,self.game.platforms):
            self.kill()
        if pg.time.get_ticks() - self.spawn_time > BULLET_LIFETIME:
            self.kill()


#player sprite
class Player(pg.sprite.Sprite):
    def __init__(self,game):
        self.groups=game.all_sprites
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.image = pg.Surface((30,30))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2,100)
        self.pos = vector(WIDTH/2,100)
        self.vel = vector(0,0)
        self.acc = vector(0,0)
        self.last_shot = 0
        self.aim_dir = "RIGHT"


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
            self.aim_dir = "LEFT"
       if keystate[pg.K_RIGHT]:
            self.acc.x= PLAYER_ACC
            self.aim_dir = "RIGHT"
       if keystate[pg.K_SPACE]:
           now = pg.time.get_ticks()
           if now - self.last_shot > BULLET_RATE:
               self.last_shot = now
               if self.aim_dir == "RIGHT":
                    dir = vector(1,0)
               else:
                    dir = vector(-1,0)
               Bullet(self.game,self.pos - (0,15),dir)


      #equations of motion
       
       self.acc.x += self.vel.x * PLAYER_FRICTION
       self.vel += self.acc
       if abs(self.vel.x) < 0.1:
           self.vel.x = 0
       self.pos += self.vel + (0.5 * self.acc)

       self.rect.midbottom = self.pos

       

class Enemy_1 (pg.sprite.Sprite):
    def __init__ (self,game,x,y):
        self.groups = game.all_sprites, game.enemy1s
        pg.sprite.Sprite.__init__(self,self.groups)
        self.image = game.enemy1_img
        self.game = game
        self.rect = self.image.get_rect()
        self.pos = vector(x,y)
        self.rect.center = self.pos
        self.rot = 0
        self.vel = vector(0,0)
        self.acc = vector(0,0)


    def update(self):
        self.rot = (self.game.player.pos - self.pos).angle_to(vector(1,0))
        self.image = pg.transform.rotate(self.game.enemy1_img,self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.acc = vector(ENEMY1_SPEED, 0).rotate(-self.rot)
        self.acc += self.vel * ENEMY1_FRICTION
        self.vel += self.acc
        self.pos += self.vel + (0.5 * self.acc)
class Camera:
    def __init__(self,width,height):
        self.camera = pg.Rect(0,0,width,height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self,target):
        x = -target.rect.x + int(WIDTH/2)
        y = -target.rect.y + int(HEIGHT/2)
        x = min (0,x)
        y = min(0,y)
        x = max(-( WIDTH + 3360),x)
        y = max(-(HEIGHT+550), y)
        self.camera = pg.Rect(x,y,self.width,self.height)

class Wall(pg.sprite.Sprite):
    def __init__(self,game,x,y,width,height):
        self.groups = game.all_sprites,game.walls
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.image = pg.Surface((width,height))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


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
        img_folder = path.join(self.dir,'img')
        self.enemy1_img = pg.image.load(path.join(img_folder, ENEMY_1_IMG)).convert_alpha()
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
        self.walls = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.enemy1s = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        self.round = 1

        self.enemy1s = Enemy_1(self,100,100)

        x = y = 0

        PLATFORM_LIST =[
            "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
            "W            W                               W                                                             P",
            "W            W                               WPPPPPPPPPPPPPPPPPP                                           P",
            "W    PPPPPPPPWPP                             W                                                             P",
            "W                                            W                                                             P",
            "W   P        PPPPPPPPPPPPPP                  W                PPPPPP                      PPPPP            P",
            "W            W                                                                               W             P",
            "W            W              PPPP                                                             W             P",
            "W            W                      PPPP                               PPPPPP                W             P",
            "W            W                PPPP      PPPP                                PPPPPPPPP        W             P",
            "W            W                                   PPPPPPPPPPPP                                W             P",
            "W            W                         PPPPPPPPP                                             W             P",
            "WPPPPPPPPPPP WPPPP    PPPPPPPPPP                                                             W             P",
            "W            W        W                PPPPPPPP                                              W             P",
            "W PPPPPPPPPPPP        W        PPPP                    PPPPPPPPPPPPPPPPPPPPPPP               W             P",
            "W            W        W             PPPPPP                                                     W           P",
            "W       PPPPPW        W   PPPPPPPPPPP                  PPPPPPPPPPPPPPPPPPPPPPP   P             W           P",
            "W            W        W                                                      P   P             W           P",
            "W            W    PPPPPPPPPP      PPPPPPPPPPPP              PPPPPPPPPPPP     P   P             W           P",
            "W            W                                              P                P   P             W           P",
            "W            W     PPPPPPPPP                                PPPPPPPPP   PPPPPP   PPPPPPPPPPP   W           P",
            "W            W                                                                                             P",
            "W            W              PPPPPP      P    P                                                             P",
            "W            W                           P    P                 PPPPPP   PPPPPP       PPPPPPPPPPPP         P",
            "W            P                           P    P                                                            P",
            "W                 PPPPPPPPPPPPPPPPPPPPPP    PPPPPPPPPPPPPP         PPPPPPPP                 P              P",
            "W            P                                                                               P             P",
            "W   PP PP P  W                                                               PPPPPPPPP                     P",
            "W            WPPPPPPPPPPPPPPP    W    PPPPPPPP                                               P             P",
            "W            W                   W    W      PPPPP            PPPPPPPPP                      P             P",
            "WPPPPPPP     W                   W    W  W         PPPP                                       P            P",
            "W            W        PPPP       W    W  W             PPPP                 PPPPPPP           P            P",
            "W       PPPPPWPPPP               W    W  W                PPPP                                             P",
            "W          W           PPPPP     W    W  W                        PPPPPPPP                                 P",
            "WPPPPPPP   W   W                 W    W  W   PPPPPPPPPP                                PPPPP               P",
            "W          W   W   PPPPPP        W    W  W      W                                    PPPP   P              P",
            "W    PPPPPPP   W                                W  W            PPPPPPPPPPPPPPPPPP  PPP                    P",
            "W              W                      PPP          W                             W  P                      P",
            "WPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP", ]

        for row in PLATFORM_LIST:
          for col in row:
            if col =="P":
                Platform(self,x,y,50,40)
            if col =="W":
                Wall(self,x,y,50,40)
                
            x += 50
          y += 40
          x = 0

        self.camera = Camera(0, 0)
            
            
       
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
        self.camera.update(self.player)
        # Check if player hits platform iff falling
        block_hit_list = pg.sprite.spritecollide(self.player, self.platforms, False)
        for block in block_hit_list:
            if self.player.vel.y > 0:
                if self.player.pos.y < block.rect.centery:
                    self.player.pos.y = block.rect.top + 1
            #
                    self.player.vel.y = 0
            if self.player.vel.x > 0 and self.player.vel.y != 0:
                if self.player.pos.x < block.rect.left:
                    self.player.pos.x = block.rect.left - 15
                    self.player.vel.x = 0
            if self.player.vel.x < 0 and self.player.vel.y != 0:
                if self.player.pos.x > block.rect.right:
                    self.player.pos.x = block.rect.right + 15
                    self.player.vel.x = 0
            if self.player.vel.y < 0:
                if self.player.pos.y - 30 > block.rect.bottom:
                    self.player.pos.y = block.rect.bottom + 30
                #
                self.player.vel.y = 0




        block_hit_list = pg.sprite.spritecollide(self.player, self.walls, False)
        for block in block_hit_list:
            if self.player.vel.x > 0:
                if self.player.pos.x < block.rect.left:
                    self.player.pos.x = block.rect.left - 15
                    self.player.vel.x = 0


            if self.player.vel.x < 0:
                if self.player.pos.x > block.rect.right:
                    self.player.pos.x = block.rect.right + 15
                    self.player.vel.x = 0

        block_hit_list = pg.sprite.spritecollide(self.enemy1s, self.platforms, False)
        for block in block_hit_list:
            if self.enemy1s.vel.y > 0:
                if self.enemy1s.pos.y < block.rect.centery:
                    self.enemy1s.pos.y = block.rect.top + 1

                    self.enemy1s.vel.y = 0
            if self.enemy1s.vel.x > 0 and self.enemy1s.vel.y != 0:
                if self.enemy1s.pos.x < block.rect.left:
                    self.enemy1s.pos.x = block.rect.left - 15
                    self.enemy1s.vel.x = 0
            if self.enemy1s.vel.x < 0 and self.enemy1s.vel.y != 0:
                if self.enemy1s.pos.x > block.rect.right:
                    self.enemy1s.pos.x = block.rect.right + 15
                    self.enemy1s.vel.x = 0
            if self.enemy1s.vel.y < 0:
                if self.enemy1s.pos.y - 30 > block.rect.bottom:
                    self.enemy1s.pos.y = block.rect.bottom + 30
                #
                self.enemy1s.vel.y = 0

        block_hit_list = pg.sprite.spritecollide(self.enemy1s, self.walls, False)
        for block in block_hit_list:
            if self.enemy1s.vel.x > 0:
                if self.enemy1s.pos.x < block.rect.left:
                    self.enemy1s.pos.x = block.rect.left - 15
                    self.enemy1s.vel.x = 0

            if self.enemy1s.vel.x < 0:
                if self.enemy1s.pos.x > block.rect.right:
                    self.enemy1s.pos.x = block.rect.right + 15
                    self.enemy1s.vel.x = 0

        # check if player hits coins

        coin_contact = pg.sprite.spritecollide(self.player,self.coins,True)
        for coin in coin_contact:
            self.score += 1


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
         pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))

         for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
         self.draw_text("BANK: " + str(self.score),20,GOLD,20,20)
         self.draw_text("ROUND: "+str(self.round),30,BLACK,WIDTH - 150 ,20)
         #Flip display after drawing
         pg.display.flip()
    def show_start_screen(self):
        #game start screen
        self.screen.fill(BLACK)
        self.draw_text(TITLE,50,RED,WIDTH/2 - 60,HEIGHT/3)
        self.draw_text("Use arrows to move, UP arrow to jump",30, RED,WIDTH/2 - 200,HEIGHT/2)
        self.draw_text("Press any key to play",20,GREEN, WIDTH/2 - 80,HEIGHT* 2/3)
        self.draw_text("Highest Round: " + str(self.highscore),20,RED, WIDTH/2 - 60,HEIGHT *3/4)
        pg.display.flip()
        self.key_press()
    
    def show_go_screen(self):
        #game over or continue
        if not self.running:
            return
        self.screen.fill(BG_COLOUR)
        self.draw_text("GAME OVER",50,RED,WIDTH/2 - 25,HEIGHT/3)
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


       




