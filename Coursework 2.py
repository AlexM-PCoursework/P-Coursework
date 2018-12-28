# Import the pygame library and initialise the game engine
import pygame as pg
import random
from pygame import *
from os import path
from random import randrange, uniform, choice
import math


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
BLOOD_RED = 166,16,30
BROWN = 165,93,53

WIDTH = 1024
HEIGHT = 720

TITLE="Enclosed"
FONT_NAME ="arial"

hs_file = "hs.txt"

vector = pg.math.Vector2

#Player Properties

PLAYER_ACC = 0.8
PLAYER_FRICTION = -0.25
GRAVITY = 0.5
PLAYER_JUMP = 10
PLAYER_HEALTH = 100
PLAYER_HIT_RECT = pg.Rect(0,0,30,40)
LIGHTING_RAD = (200,200)

# using weapon'l' as convention for referencing
WEAPONS ={}
WEAPONS['uzil']={'bullet_speed':40,
                   'bullet_lifetime': 1000,
                   'rate':150,
                   'damage':10,
                   'spread':0,
                   'bullet_size':'small',
                   'bullet_count':1}
WEAPONS['pistoll']={'bullet_speed':20,
                   'bullet_lifetime': 500,
                   'rate':600,
                   'damage':10,
                   'spread':0,
                   'bullet_size':'large',
                   'bullet_count':1}
WEAPONS['shotgunl']={'bullet_speed':20,
                   'bullet_lifetime': 300,
                   'rate':1300,
                   'damage':6,
                   'spread':10,
                   'bullet_size':'small',
                   'bullet_count':8}

WEAPON_SOUNDS = {'pistoll': ['pistol.wav'],
                 'uzil': ['uzi.wav'],
                 'shotgunl':['shotgun.wav']}

# items

ITEM_IMAGES = {'health':'health.png',
               'uzir':'uzir.png',
               'uzil':'uzil.png',
               'pistol':'pistol.png',
               'pistoll':'pistoll.png',
               'shotgunr':'shotgunr.png',
               'shotgunl':'shotgunl.png'}

TOGGLEBAR_IMAGES = {'PISTOL':'pistolt.png',
                    'UZI':'uzilt.png',
                    'SHOTGUN':'shotgunlt.png'}

HEALTH_POWERUP = 50

BULLET_OFFSET = vector(-30,-40)
ENEMY_1_IMG = 'ghost.png'
ENEMY1_SPEED = 0.03
ENEMY1_FRICTION = -0.02
ENEMY1_DAMAGE = 10
KNOCKBACK = 6
AVOID_RAD = 50

BACKGROUND_LAYER = 0
WALL_LAYER = 1
PLAYER_LAYER = 2
BULLET_LAYER = 3
ENEMY_LAYER = 2
WEAPON_LAYER = 3
EFFECTS_LAYER = 4

WEAPON_ROT = 2

WALL_IMG ='wall.png'
BACKGROUND_IMG = 'bg3.png'
COIN_IMG ='coin.png'
PLAYER_IMG ='player3.png'

WEAPON1_WIDTH = 20

def draw_player_health(surf,x,y,pct):
    if pct< 0:
        pct = 0
    BAR_LENGTH = 150
    BAR_HEIGHT = 10
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x,y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x,y,fill,BAR_HEIGHT)
    if pct > 0.6:
        colour = GREEN
    elif pct > 0.3:
        colour = GOLD
    else:
        colour = RED
    pg.draw.rect(surf,colour,fill_rect)
    pg.draw.rect(surf,WHITE,outline_rect,2)

class Item(pg.sprite.Sprite):
    def __init__(self,game, pos, type,plat):
        self._layer = EFFECTS_LAYER
        self.groups = game.all_sprites, game.items
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.plat = plat
        self.image = game.item_images[type]
        self.rect = self.image.get_rect()
        self.type = type
        self.rect.centerx = self.plat.rect.centerx


    def update(self):
        self.rect.bottom = self.plat.rect.top - 5

class Bullet(pg.sprite.Sprite):
    def __init__(self,game,pos,dir):
        self._layer = BULLET_LAYER
        self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.image = self.game.bullet_images[WEAPONS[self.game.player.weaponl]['bullet_size']]
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.pos = pos + vector(0,-5)
        self.vel = dir * WEAPONS[self.game.player.weaponl]['bullet_speed']
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        self.pos += self.vel
        self.rect.center = self.pos
        if pg.sprite.spritecollideany(self,self.game.walls):
            self.kill()
        if pg.sprite.spritecollideany(self,self.game.platforms):
            self.kill()
        if pg.time.get_ticks() - self.spawn_time > WEAPONS[self.game.player.weaponl]['bullet_lifetime']:
            self.kill()
        self.image = pg.transform.rotate(self.game.bullet_images[WEAPONS[self.game.player.weaponl]['bullet_size']], self.game.weapon.rot)


def collide_hit_rect(one,two):
    return one.hit_rect.colliderect(two.rect)
#player sprite

class Weapon(pg.sprite.Sprite):
    def __init__(self,game,image):
        self._layer = EFFECTS_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.image = game.item_images['pistol']
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2,100)
        self.pos = vector(WIDTH/2,100)
        self.vel = vector(0,0)
        self.acc = vector(0,0)
        self.aim_dir = "LEFT"
        self.rot = 0


    def update(self):
        self.vel = self.game.player.vel
        self.acc = self.game.player.acc
        self.rot_speed = 0
        keystate = pg.key.get_pressed()
        if keystate[ord('a')]:
            self.rot_speed += WEAPON_ROT
        if keystate[ord('d')]:
            self.rot_speed -= WEAPON_ROT
        self.rot = (self.rot + self.rot_speed) % 360
        if self.rot >= 45 and self.rot < 180:
            self.rot = 45
        if self.rot <= 315 and self.rot > 180:
            self.rot = 315

        if self.game.player.inventory[self.game.current] == 'UZI':
            self.game.player.weaponl = 'uzil'
            self.game.player.weaponr = 'uzir'
            if self.game.player.aim_dir == 'LEFT':
                self.image = self.game.item_images['uzil']
            else:
                self.image = self.game.item_images['uzir']

        if self.game.player.inventory[self.game.current] == 'SHOTGUN':
            self.game.player.weaponl = 'shotgunl'
            self.game.player.weaponr = 'shotgunr'
            if self.game.player.aim_dir == 'LEFT':
                self.image = self.game.item_images['shotgunl']
            else:
                self.image = self.game.item_images['shotgunr']

        if self.game.player.inventory[self.game.current] == 'PISTOL':
            self.game.player.weaponl = 'pistoll'
            self.game.player.weaponr = 'pistol'
            if self.game.player.aim_dir == 'LEFT':
                self.image = self.game.item_images['pistoll']
            else:
                self.image = self.game.item_images['pistol']


        if self.game.player.aim_dir == "LEFT":
            self.pos = self.game.player.pos + (-18, -23)
            self.image = pg.transform.rotate(self.game.item_images[self.game.player.weaponl], self.rot)


        else:
            self.pos = self.game.player.pos + (18, -23)
            self.image = pg.transform.rotate(self.game.item_images[self.game.player.weaponr], self.rot)




        self.rect = self.image.get_rect()
        self.rect.center = self.pos


class Player(pg.sprite.Sprite):
    def __init__(self,game):
        self._layer = PLAYER_LAYER
        self.groups=game.all_sprites
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.image = game.player_imgl
        self.rect = self.image.get_rect()
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.rect.center = (WIDTH/2,100)
        self.pos = vector(WIDTH/2,100)
        self.vel = vector(0,0)
        self.acc = vector(0,0)
        self.last_shot = 0
        self.aim_dir = "LEFT"
        self.weaponl = 'pistoll'
        self.weaponr ='pistol'
        self.health = PLAYER_HEALTH
        self.damaged = False
        self.rot = 0
        self.inventory = ['PISTOL']


    def hit(self):
        self.damaged = True


    def jump(self):
        #Jump allowed if on a platform
        contacts = pg.sprite.spritecollide(self,self.game.platforms,False)
        if contacts:

            self.vel.y = -PLAYER_JUMP

        contacts = pg.sprite.spritecollide(self, self.game.trapdoors, False)
        if contacts:
            self.vel.y = -PLAYER_JUMP


    def add_health(self,amount):
        self.health += amount
        if self.health > PLAYER_HEALTH:
            self.health = PLAYER_HEALTH

        
                          

    def update(self):
       self.acc = vector(0,GRAVITY)
       self.rot_speed = 0
       #self.vel = vector(0,0)
       keystate = pg.key.get_pressed()
       if keystate[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
            self.aim_dir = "LEFT"
            self.image = self.game.player_imgl
        #    self.game.weapon.image = self.game.item_images[self.weaponl]
       if keystate[pg.K_RIGHT]:
            self.acc.x= PLAYER_ACC
            self.aim_dir = "RIGHT"
            self.image = self.game.player_imgr
        #    self.game.weapon.image = self.game.item_images[self.weaponr]

       if keystate[pg.K_SPACE]:
           self.shoot()

       self.acc.x += self.vel.x * PLAYER_FRICTION
       self.vel += self.acc
       if abs(self.vel.x) < 0.1:
           self.vel.x = 0
       self.pos += self.vel + (0.5 * self.acc)




       self.hit_rect.midbottom = self.pos
       self.rect.center = self.hit_rect.center




    def shoot(self):
           now = pg.time.get_ticks()
           if now - self.last_shot > WEAPONS[self.weaponl]['rate']:
               self.last_shot = now
               pos = self.pos + BULLET_OFFSET
               for i in range(WEAPONS[self.weaponl]['bullet_count']):
                   spread = uniform(-WEAPONS[self.weaponl]['spread'],WEAPONS[self.weaponl]['spread'])
                   if self.aim_dir == "RIGHT":
                        dirv = vector(1,0).rotate(360 - self.game.weapon.rot + spread)
                        Bullet(self.game, self.game.weapon.rect.center , dirv)
                   else:
                        dirv = vector(-1, 0).rotate(360 - self.game.weapon.rot +spread)
                        Bullet(self.game, self.game.weapon.rect.center, dirv)
                   choice(self.game.weapon_sounds[self.weaponl]).play()




      #equations of motion
       

       

class Enemy_1 (pg.sprite.Sprite):
    def __init__ (self,game,x,y):
        self._layer = ENEMY_LAYER
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
        self.health = 40

    def avoid_enemies(self):
        for enemy1 in self.game.enemy1s:
            if enemy1 != self:
                dist = self.pos - enemy1.pos
                if 0 < dist.length() < AVOID_RAD:
                    self.acc += dist.normalize()

    def draw_health(self):
        if self.health > 20:
            colour = GREEN
        elif self.health > 10:
            colour = GOLD
        else:
            colour = RED
        width = int(self.rect.width * self.health/100)
        self.health_bar = pg.Rect(0,0,width,5)
        if self.health < 40:
            pg.draw.rect(self.image, colour, self.health_bar)


    def update(self):
        self.rot = (self.game.player.pos - self.pos).angle_to(vector(1,0))
        self.image = pg.transform.rotate(self.game.enemy1_img,self.rot)
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.pos
        self.acc = vector(1, 0).rotate(-self.rot)
        self.avoid_enemies()
        self.acc.scale_to_length(ENEMY1_SPEED)
        self.acc += self.vel * ENEMY1_FRICTION
        self.vel += self.acc
        self.pos += self.vel + (0.5 * self.acc)
        if self.health <= 0:
            self.kill()


        block_hit_list = pg.sprite.spritecollide(self, self.game.platforms, False)
        for block in block_hit_list:
            if self.vel.y > 0:
                if self.pos.y < block.rect.centery:
                    self.pos.y = block.rect.top + 1

                    self.vel.y = 0
            if self.vel.x > 0 and self.vel.y != 0:
                if self.pos.x < block.rect.left:
                    self.pos.x = block.rect.left - self.rect.width/2
                    self.vel.x = 0
            if self.vel.x < 0 and self.vel.y != 0:
                if self.pos.x > block.rect.right:
                    self.pos.x = block.rect.right + self.rect.width/2
                    self.vel.x = 0
            if self.vel.y < 0:
                if self.pos.y - self.rect.height > block.rect.centery:
                    self.pos.y = block.rect.bottom + self.rect.height -1

                    self.vel.y = 0

        block_hit_list = pg.sprite.spritecollide(self, self.game.walls, False)
        for block in block_hit_list:
            if self.vel.x > 0:
                if self.pos.x < block.rect.left:
                    self.pos.x = block.rect.left - self.rect.width/2
                    self.vel.x = 0

            if self.vel.x < 0:
                if self.pos.x > block.rect.right:
                    self.pos.x = block.rect.right + self.rect.width/2
                    self.vel.x = 0

            if self.vel.y < 0:
                if self.pos.y - self.rect.height > block.rect.centery:
                    self.pos.y = block.rect.bottom + self.rect.height - 1

                    self.vel.y = 0

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
        y = max(-(HEIGHT+150), y)
        self.camera = pg.Rect(x,y,self.width,self.height)

class Wall(pg.sprite.Sprite):
    def __init__(self,game,x,y,width,height):
        self._layer = WALL_LAYER
        self.groups = game.all_sprites,game.walls
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.image = game.wall_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Platform(pg.sprite.Sprite):
    def __init__(self,game,x,y,width,height):
        self._layer = WALL_LAYER
        self.groups = game.all_sprites,game.platforms
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.image = game.wall_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        if randrange (100) < 15:
            Coin(self.game,self)
        if randrange (1000) < 2:
            Item(self.game, (x,y),'health',self)
        if randrange (100) < 5:
            Item(self.game, (x,y),'uzil',self)
        if randrange(100) <5:
            Item(self.game, (x,y),'shotgunl',self)

class Door(pg.sprite.Sprite):
    def __init__(self,game,x,y):
        self. _layer = WALL_LAYER
        self.groups = game.all_sprites, game.doors
        pg.sprite.Sprite. __init__(self,self.groups)
        self.game = game
        self.image = self.game.door_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y




class Trapdoor(pg.sprite.Sprite):
    def __init__(self,game,x,y):
        self. _layer = WALL_LAYER
        self.groups = game.all_sprites, game.trapdoors
        pg.sprite.Sprite. __init__(self,self.groups)
        self.game = game
        self.image = self.game.trapdoor_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Coin(pg.sprite.Sprite):
    def __init__(self,game,plat):
        self._layer = EFFECTS_LAYER
        self.groups = game.all_sprites, game.coins
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.plat = plat
        self.image = game.coin_img
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx
        self.rect.bottom = self.plat.rect.top - 5

    def update(self):
        self.rect.bottom = self.plat.rect.top - 5

'''
class ToggleRect(pg.sprite.Sprite):
    def __init__(self,game):
        self. _layer = 10
        self.groups = game.all_sprites, game.togglerect
        pg.sprite.Sprite. __init__(self,self.groups)
        self.game = game
        toggle_height = 200
        border_spacing = 10
      #  self.image = pg.draw.rect(self.game.screen, GOLD, pg.Rect(0 - border_spacing, HEIGHT - toggle_height + 60, 60 + 2 * border_spacing, toggle_height - 120), 3)
        self.image = Surface((10,10))
        self.image.fill(GOLD)
        self.rect = self.image.get_rect()
        self.game.togglebar_img.blit(self.image,[200,HEIGHT-50])
        #self.rect.center = (100-border_spacing + 30,HEIGHT - toggle_height )

'''
       

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
        self.sound_folder = path.join(self.dir,'sound')
        self.title_font = path.join(img_folder, 'font.ttf')
        self.header_font = path.join(img_folder,'zombified.ttf')
        self.old_font = path.join(img_folder, 'Ginga.ttf')
        self.bullet_images = {}
        self.bullet_images['large'] = pg.image.load(path.join(img_folder,'bullet.png')).convert_alpha()
        self.bullet_images['small']= pg.transform.scale(self.bullet_images['large'],(4,8))
        self.door_image = pg.transform.scale(pg.image.load(path.join(img_folder,'door.png')).convert_alpha(),(25,40))
        self.togglebar_img = pg.transform.scale(pg.image.load(path.join(img_folder, 'paper.png')).convert_alpha(), (WIDTH, 200))
        self.trapdoor_image = pg.image.load(path.join(img_folder,'trapdoor.png')).convert_alpha()
        self.body_font = path.join(img_folder,'arial.ttf')
        self.enemy1_img = pg.image.load(path.join(img_folder, ENEMY_1_IMG)).convert_alpha()
        self.player_imgr = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()
        self.player_imgl = pg.image.load(path.join(img_folder,'playerl.png')).convert_alpha()
        self.wall_img = pg.transform.scale(pg.image.load(path.join(img_folder,WALL_IMG)).convert_alpha(),(41,41))
        self.border_img = pg.image.load(path.join(img_folder,'border.png')).convert_alpha()

        self.coin_img = pg.image.load(path.join(img_folder,COIN_IMG)).convert_alpha()
        self.background_img = pg.image.load(path.join(img_folder,BACKGROUND_IMG)).convert_alpha()
        #torch effect
        self.fog = pg.Surface((WIDTH,HEIGHT))
        self.fog.fill((20,20,20))
        self.light = pg.image.load(path.join(img_folder,'light.png')).convert_alpha()
        self.light = pg.transform.scale(self.light,LIGHTING_RAD)
        self.light_rect = self.light.get_rect()
        self.weapon_sounds ={}
        for weapon in WEAPON_SOUNDS:
            self.weapon_sounds[weapon] = []
            for sound in WEAPON_SOUNDS[weapon]:
                s = pg.mixer.Sound(path.join(self.sound_folder, sound))
                s.set_volume(0.15)
                self.weapon_sounds[weapon].append(s)

        with open(path.join(self.dir,hs_file),'w') as file:
            try:
                self.highscore = int(file.read())
            except:
                self.highscore = 0
        self.item_images ={}
        for item in ITEM_IMAGES:
            self.item_images[item]=pg.image.load(path.join(img_folder,ITEM_IMAGES[item])).convert_alpha()
        self.togglebar_images = {}
        for image in TOGGLEBAR_IMAGES:
            self.togglebar_images[image] = pg.image.load(path.join(img_folder,TOGGLEBAR_IMAGES[image])).convert_alpha()


    def new(self):
        #starts new game

        self.score = 0
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.trapdoors = pg.sprite.Group()
        self.doors = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.togglebar = pg.sprite.Group()
 #       self.togglerect = pg.sprite.Group()
        self.items = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.enemy1s = pg.sprite.Group()
        self.weapon = Weapon(self,'pistol')
        self.bullets = pg.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        self.all_sprites.add(self.weapon)
        self.round = 1
        self.paused = False
        self.toggle = False
        self.mover = True
        self.night = False
        self.border_count = 0
        self.current = 0



        Enemy_1(self,100,100)
        Enemy_1(self,100,500)


        x = y = 0

        PLATFORM_LIST =[
            "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
            "W                                            D                                                             P",
            "W                                           PPPPPPPPPPPPPPPPPPPP                                           P",
            "WPPPPPP    PPPPPPPPP        PPPPPPP  PPPPPPPPW                                                             P",
            "WP                                           W                                                             P",
            "W    PPP  PPP       PPPPP       PPPP     PPPPW              PPPPPP                      PPPPP              P",
            "WP              PPP                          W                                                W            P",
            "W      PPPPPPPPP           PPPP       PPP   PW                                               W             P",
            "W                 PPP                        W                         PPPPPP                W             P",
            "WPPPP                  PPPPPPPP        PPP   W                              PPPPPPPPP        W             P",
            "W     PP PPPP                     PP         W   PPPPPPPPPPPP                                W             P",
            "W                     PPPPPPPPPP             W                                               W             P",
            "WPPPPPPPPPPPTPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPTW                                              W              P",
            "W            W        W                                                                      W             P",
            "W  PPPPPPPPPPP        W        PPPP      PPPPPP        PPPPPPPPPPPPPPPPPPPPPPP               W             P",
            "W            W        W             PPPPPP                                                     W           P",
            "W       PPPPPW        W   PPPPPPPPPPP                  PPPPPPPPPPPPPPPPPPPPPPP   P             W           P",
            "W            W        W                                                      P   P             W           P",
            "WPPPPPPPPP   W    PPPPPPPPPP      PPPPPPPPPPPP              PPPPPPPPPPPP     P   P             W           P",
            "W        W   W                                              P                P   P             W           P",
            "WPPPPP   W   W     PPPPPPPPP                                PPPPPPPPP   PPPPPP   PPPPPPPPPPP   W           P",
            "W        W   W                                                                                             P",
            "WP       WPP W              PPPPPP      P    P                                                             P",
            "WWP      W   W                           P    P                 PPPPPP   PPPPPP       PPPPPPPPPPPP         P",
            "WWWP     W  PW                           P    P                                                            P",
            "WWWWP    W         PPPPPPPPPPPPPPPPPPPPPP    PPPPPPPPPPPPPP         PPPPPPPP                 P              P",
            "WWWWWP       P                                                                               P             P",
            "W   WW PP P  W                                                               PPPPPPPPP                     P",
            "W            WPPPPPPPPPPPPPPP    W    PPPPPPPP                                               P             P",
            "W   PP       W                   W    W      PPPPP            PPPPPPPPP                      P             P",
            "WPPPPPPP     W                   W    W  W         PPPP                                       P            P",
            "W            W        PPPP       W    W  W             PPPP                 PPPPPPP           P            P",
            "W       PPPPPWPPPP               W    W  W                PPPP                                             P",
            "W          W           PPPPP     W    W  W                        PPPPPPPP                                 P",
            "WPPPPPPP   W   W                 W    W  W   PPPPPPPPPP                                PPPPP               P",
            "W          W   W   PPPPPP        W    W  W      W                                    PPPP   P              P",
            "W    PPPPPPW   W                                W  W            PPPPPPPPPPPPPPPPPP  PPP                    P",
            "W              W                      PPP          W                             W  P                      P",
            "WPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP", ]

        for row in PLATFORM_LIST:
          for col in row:
            if col =="P":
                Platform(self,x,y,50,50)
            if col =="W":
                Wall(self,x,y,50,50)
            if col == "D":
                Door(self,x,y)
            if col == "T":
                Trapdoor(self,x,y)

                
            x += 41
          y += 41
          x = 0

        self.camera = Camera(0, 0)
            
            
       
        self.run()
        
    def run(self):
        #game loop

        self.playing = True
        while self.playing:
         self.clock.tick(60)
         self.events()
         if not self.paused:
            self.update()
         self.draw()
        pg.mixer.music.fadeout(100)
        
         
    def update(self):
        #game loop - update

        self.all_sprites.update()
        self.camera.update(self.player)


        background = self.background_img
        self.screen.blit(background, [0, 0])

        keystate = pg.key.get_pressed()

  #      pg.draw.rect(self.screen, WHITE, self.player.hit_rect, 2)





        #enemy hits player

        for door in self.doors:
            dist = door.rect.center - self.player.pos
            if 0 < dist.length() < 100:
                self.draw_text("2(Q",12,WHITE,door.rect.x,door.rect.y)
     #           self.draw_texty("2 (Q)", self.body_font, 12, WHITE, door.rect.x + 45 , door.rect.y +20, align="center")
                if 0 < dist.length() < 40 and self.score >= 2 and keystate[ord('q')]:
                    pg.mixer.Sound(path.join(self.sound_folder, 'door.wav')).play()
                    self.score -= 2
                    door.kill()


        for trapdoor in self.trapdoors:
            dist = trapdoor.rect.center - self.player.pos
            if 0 < dist.length() < 100:
                self.draw_texty("2 (Q)", self.body_font, 12, WHITE, trapdoor.rect.x + 20, trapdoor.rect.y + 30, align="center")
                if self.score >= 2 and keystate[ord('q')]:
                    pg.mixer.Sound(path.join(self.sound_folder, 'door.wav')).play()
                    self.score -= 2
                    trapdoor.kill()

        hits = pg.sprite.spritecollide(self.player, self.enemy1s, False)
        for hit in hits:
            self.player.health -= ENEMY1_DAMAGE
            hit.vel = vector(0,0)
            if self.player.health <= 0:
                self.playing = False
        if hits:

            self.player.vel += vector(KNOCKBACK,0).rotate(-hits[0].rot)

        hits = pg.sprite.spritecollide(self.player,self.items, False)
        for hit in hits:
            if hit.type =='health' and self.player.health < PLAYER_HEALTH:
                hit.kill()
                self.player.add_health(HEALTH_POWERUP)


            if hit.type =='uzil':
                hit.kill()
                if 'UZI' not in self.player.inventory:
                    self.player.inventory.append('UZI')

            if hit.type =='shotgunl':
                hit.kill()
                if 'SHOTGUN' not in self.player.inventory:
                    self.player.inventory.append('SHOTGUN')

        hits = pg.sprite.groupcollide(self.enemy1s,self.bullets,False,True)
        for hit in hits:
            hit.health -= WEAPONS[self.player.weaponl]['damage'] * len(hits[hit])

        block_hit_list = pg.sprite.spritecollide(self.player, self.platforms, False,collide_hit_rect)
        for block in block_hit_list:
            if self.player.vel.y > 0:
                if self.player.pos.y < block.rect.centery:
                    self.player.pos.y = block.rect.top +1
            #
                    self.player.vel.y = 0
            if self.player.vel.x > 0 and self.player.vel.y != 0:
                if self.player.pos.x < block.rect.left:
                    self.player.pos.x = block.rect.left - self.player.hit_rect.width/2
                    self.player.vel.x = 0
            if self.player.vel.x < 0 and self.player.vel.y != 0:
                if self.player.pos.x > block.rect.right:
                    self.player.pos.x = block.rect.right + self.player.hit_rect.width/2
                    self.player.vel.x = 0
            if self.player.vel.y < 0:
                if self.player.pos.y - self.player.hit_rect.height > block.rect.bottom:
                    self.player.pos.y = block.rect.bottom + self.player.hit_rect.height
                #
                self.player.vel.y = 0

        block_hit_list = pg.sprite.spritecollide(self.player, self.trapdoors, False, collide_hit_rect)
        for block in block_hit_list:
            if self.player.vel.y > 0:
                if self.player.pos.y < block.rect.centery:
                    self.player.pos.y = block.rect.top + 1
                    #
                    self.player.vel.y = 0
            if self.player.vel.x > 0 and self.player.vel.y != 0:
                if self.player.pos.x < block.rect.left:
                    self.player.pos.x = block.rect.left - self.player.hit_rect.width / 2
                    self.player.vel.x = 0
            if self.player.vel.x < 0 and self.player.vel.y != 0:
                if self.player.pos.x > block.rect.right:
                    self.player.pos.x = block.rect.right + self.player.hit_rect.width / 2
                    self.player.vel.x = 0
            if self.player.vel.y < 0:
                if self.player.pos.y - self.player.hit_rect.height > block.rect.bottom:
                    self.player.pos.y = block.rect.bottom + self.player.hit_rect.height
                #
                self.player.vel.y = 0

        block_hit_list = pg.sprite.spritecollide(self.player, self.doors, False, collide_hit_rect)
        for block in block_hit_list:
            if self.player.vel.x > 0:
                if self.player.pos.x < block.rect.left:
                    self.player.pos.x = block.rect.left - self.player.hit_rect.width / 2
                    self.player.vel.x = 0

            if self.player.vel.y < 0:
                if self.player.pos.y - self.player.hit_rect.height > block.rect.bottom:
                    self.player.pos.y = block.rect.bottom + self.player.hit_rect.height
                #
                self.player.vel.y = 0

            if self.player.vel.x < 0:
                if self.player.pos.x > block.rect.right:
                    self.player.pos.x = block.rect.right + self.player.hit_rect.width / 2
                    self.player.vel.x = 0



        block_hit_list = pg.sprite.spritecollide(self.player, self.walls, False,collide_hit_rect)
        for block in block_hit_list:
            if self.player.vel.x > 0:
                if self.player.pos.x < block.rect.left:
                    self.player.pos.x = block.rect.left - self.player.hit_rect.width/2
                    self.player.vel.x = 0

            if self.player.vel.y < 0:
                if self.player.pos.y - self.player.hit_rect.height > block.rect.bottom:
                    self.player.pos.y = block.rect.bottom + self.player.hit_rect.height
                #
                self.player.vel.y = 0


            if self.player.vel.x < 0:
                if self.player.pos.x > block.rect.right:
                    self.player.pos.x = block.rect.right + self.player.hit_rect.width/2
                    self.player.vel.x = 0

        # check if player hits coins

        coin_contact = pg.sprite.spritecollide(self.player,self.coins,True)
        for coin in coin_contact:
            self.score += 1

        border_spacing = 10
        toggle_height = 200
     #   keystate = pg.key.get_pressed

    def right(self):
        border_spacing = 10
        toggle_height = 200
        if len(self.player.inventory) > self.current + 1:
            self.border_count += 100
            pg.draw.rect(self.screen, GOLD, pg.Rect(self.border_count - border_spacing, HEIGHT - toggle_height + 60,
                                                    60 + 2 * border_spacing, toggle_height - 120), 3)
            self.current += 1

    def left(self):
        border_spacing = 10
        toggle_height = 200
        if self.current > 0:
            self.border_count -= 100
            pg.draw.rect(self.screen, GOLD, pg.Rect(self.border_count - border_spacing, HEIGHT - toggle_height + 60,
                                                    60 + 2 * border_spacing, toggle_height - 120), 3)
            self.current -= 1



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
             if event.key ==pg.K_p:
                 self.paused = not self.paused
             if event.key ==pg.K_t:
                 self.toggle = not self.toggle
             if event.key ==pg.K_e:
                 self.right()
             if event.key ==pg.K_q:
                 self.left()
             if event.key == pg.K_n:
                 self.night = not self.night

    def draw_texty(self,text,font_name,size,colour,x,y,align ="center"):
        font = pg.font.Font(font_name,size)
        text_surface = font.render(text,True,colour)
        text_rect = text_surface.get_rect()
        if align == "center":
            text_rect.center = (x,y)
        self.screen.blit(text_surface, text_rect)




    def draw_togglebar(self):


        border_spacing = 10
        toggle_height = 200
        self.image = self.togglebar_img
        # draws paper texture and title
        self.screen.blit(self.image, (0, HEIGHT - toggle_height))
        self.draw_texty("INVENTORY", self.body_font, 20, GOLD, WIDTH / 2, HEIGHT - toggle_height - 10)
        self.draw_texty("USE Q AND E TO CHANGE WEAPONS", self.body_font, 15, GOLD, WIDTH/2, HEIGHT - toggle_height + 10 )
        count = 100
      #  border_count = border_count2
          #  if len(self.player.inventory) > 1:


        for i in range(len(self.player.inventory)):
                    self.image = self.togglebar_images[self.player.inventory[i]]
                    self.rect = self.image.get_rect()
                    self.screen.blit(self.image, (count, HEIGHT - toggle_height / 2 - self.rect.height / 2))
                    self.draw_texty(self.player.inventory[i], self.body_font, 20, BLACK,
                                    count - border_spacing + self.rect.width / 2 + 5, HEIGHT - toggle_height + 40)

                    #       pg.draw.rect(self.screen, GOLD, pg.Rect(count - border_spacing,HEIGHT - toggle_height + 40, 60 + 2*border_spacing,toggle_height - 80), 3)
                    border = pg.transform.scale(self.border_img, (60 + 2 * border_spacing, toggle_height - 120))
                    self.screen.blit(border, (count - border_spacing, HEIGHT - toggle_height + 60))
                    count += 100



        



        


    def display_fog(self):

        self.fog.fill((20,20,20))
        self.light_rect.center = self.camera.apply(self.player).center
        self.fog.blit(self.light,self.light_rect)
        self.screen.blit(self.fog,(0,0),special_flags = pg.BLEND_MULT)






             
    def draw(self):
        #game loop - draw


         pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))


         for sprite in self.all_sprites:
            if isinstance(sprite,Enemy_1):
                sprite.draw_health()
            self.screen.blit(sprite.image, self.camera.apply(sprite))

         if self.night:
             self.display_fog()

         self.draw_text("BANK: " + str(self.score),20,GOLD,20,20)
         self.draw_text("ROUND: "+str(self.round),30,BLOOD_RED,WIDTH - 150 ,20)
         draw_player_health(self.screen, 430,10,self.player.health/ PLAYER_HEALTH)
         if self.paused:
             self.draw_texty("Paused",self.title_font,120,BLOOD_RED,WIDTH/2,HEIGHT/2,align="center")


         if self.toggle:
             self.draw_togglebar()






         #Flip display after drawing
         pg.display.flip()

    def show_start_screen(self):
        #game start screen
        self.screen.fill(BLACK)
        pg.mixer.music.load(path.join(self.sound_folder, 'background.mp3'))
        pg.mixer.music.play(loops=-1)

        self.draw_texty(TITLE,self.title_font,150,RED,WIDTH/2,HEIGHT*1/4,align="center")
        self.draw_texty("Use arrows to move, UP arrow to jump",self.header_font, 50, RED, WIDTH/2,HEIGHT/2,align = "center")
        self.draw_texty("Press Any Key to Play",self.body_font, 20,WHITE, WIDTH/2 ,HEIGHT* 2/3, align="center")
        self.draw_texty("Highest Round: " + str(self.highscore),self.body_font,20,RED, WIDTH/2 ,HEIGHT *3/4)
        pg.display.flip()
        self.key_press()

    
    def show_go_screen(self):
        #game over or continue
        if not self.running:
            return
        self.screen.fill(BLACK)
        self.draw_texty("GAME OVER",self.title_font, 150,RED,WIDTH/2,HEIGHT/4)
        self.draw_texty("You got to round " + str(self.round),self.header_font, 50, RED,WIDTH/2,HEIGHT *2/3 - 20)
        self.draw_texty("Press any key to play again",self.header_font,50,GOLD, WIDTH/2 ,HEIGHT* 3/4)
        if self.round > self.highscore:
            self.highscore = self.round
            self.draw_texty("NEW HIGH ROUND",self.header_font, 40, WHITE, WIDTH/2,HEIGHT /2, align="center")
            with open(path.join(self.dir,hs_file),'w') as file:
                file.write(str(self.round))
        else:
           self.draw_texty("Highest Round: " + str(self.highscore),self.body_font, 20,RED, WIDTH/2,HEIGHT /2)
        pg.display.flip()
        self.key_press2()

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


    def key_press2(self):
        pg.mixer.music.load(path.join(self.sound_folder, 'game_over.mp3'))
        pg.mixer.music.play(loops=-1)
        not_pressed = True
        while not_pressed:
            self.clock.tick(60)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    not_pressed = False
                    self.running = False
                if event.type == pg.KEYUP:
                    pg.mixer.music.load(path.join(self.sound_folder, 'background.mp3'))
                    pg.mixer.music.play(loops=-1)
                    not_pressed = False


          

g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()
    

pg.quit()


       




