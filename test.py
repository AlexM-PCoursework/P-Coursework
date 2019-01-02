# Import the pygame library and initialise the game engine
import pygame as pg
import random
from pygame import *
from os import path
from random import randrange, uniform, choice
import math
import time
from collections import deque
import threading

# settings
# Define some colors (for now)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WATERM = 253, 91, 120
BG_COLOUR = 48, 191, 191
GOLD = 255, 215, 0
BLOOD_RED = 166, 16, 30
BROWN = 165, 93, 53
NIGHT = (14, 14, 14)

WIDTH = 1024
HEIGHT = 720




vector = pg.math.Vector2

# Player Properties

PLAYER_ACC = 0.8
PLAYER_FRICTION = -0.25
GRAVITY = 0.5
PLAYER_JUMP = 10
PLAYER_HEALTH = 100
PLAYER_HIT_RECT = pg.Rect(0, 0, 30, 40)
LIGHTING_RAD = (600, 600)

# using weapon'l' as convention for referencing

# items



HEALTH_POWERUP = 50

BULLET_OFFSET = vector(-30, -40)
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



WALL_IMG = 'wall.png'


PLAYER_IMG = 'player3.png'

WEAPON1_WIDTH = 20


class SquareGrid:
    def __init__(self, game, width, height):
        self.game = game
        self.width = width
        self.height = height
        self.walls = []
        self.platforms = []
        wall_dim = 41
        for wall in self.game.walls:
            self.walls.append(vector(wall.rect.x, wall.rect.y))
        for platform in self.game.platforms:
            self.walls.append(vector(platform.rect.x, platform.rect.y))
        self.connections = [vector(wall_dim, 0), vector(-wall_dim, 0), vector(0, wall_dim), vector(0, -wall_dim)]

    def in_bounds(self, node):
        return 0 <= node.x < self.width and 0 <= node.y < self.height

    def passable(self, node):
        return node not in self.walls

    def find_neighbours(self, node):
        neighbours = [node + connection for connection in self.connections]
        if (node.x + node.y) % 2:
            neighbours.reverse()
        neighbours = filter(self.in_bounds, neighbours)
        neighbours = filter(self.passable, neighbours)
        #     reference = [x / 41 for x in neighbours]
        #      print(list(reference))
        return neighbours

    def draw_grid(self):
        for x in range(0, WIDTH, 41):
            pg.draw.line(self.game.screen, WHITE, (x, 0), (x, 1024))
        for y in range(0, HEIGHT, 41):
            pg.draw.line(self.game.screen, WHITE, (0, y), (720, y))

def player_tile(pos):

    x = int((pos.x) / 41) * 41
    y = int((pos.y - 30) / 41) * 41
    tile = x, y


    return tile


def vector_conv(vec):
    return (int(vec.x), int(vec.y))


def breadth_first_search(graph, start, end):
    frontier = deque()
    frontier.append(start)
    path = {}
    path[vector_conv(start)] = None
    while len(frontier) > 0:
        current = frontier.popleft()
        if current == end:
            break
        for x in graph.find_neighbours(current):
            if vector_conv(x) not in path:
                frontier.append(x)
                path[vector_conv(x)] = current - x


    return path







class Player(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_imgl
        self.rect = self.image.get_rect()
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.rect.center = (WIDTH / 2, 100)
        self.pos = vector(WIDTH / 2, 100)
        self.vel = vector(0, 0)
        self.acc = vector(0, 0)
        self.last_shot = 0
        self.aim_dir = "LEFT"

        self.health = PLAYER_HEALTH
        self.damaged = False
        self.rot = 0


    def hit(self):
        self.damaged = True

    def jump(self):
        # Jump allowed if on a platform
        contacts = pg.sprite.spritecollide(self, self.game.platforms, False)
        if contacts:
            self.vel.y = -PLAYER_JUMP

        contacts = pg.sprite.spritecollide(self, self.game.trapdoors, False)
        if contacts:
            self.vel.y = -PLAYER_JUMP



    def update(self):
        self.acc = vector(0, GRAVITY)
        self.rot_speed = 0
        # self.vel = vector(0,0)
        keystate = pg.key.get_pressed()
        if keystate[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
            self.aim_dir = "LEFT"
            self.image = self.game.player_imgl
        #    self.game.weapon.image = self.game.item_images[self.weaponl]
        if keystate[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC
            self.aim_dir = "RIGHT"
            self.image = self.game.player_imgr
        #    self.game.weapon.image = self.game.item_images[self.weaponr]


        self.acc.x += self.vel.x * PLAYER_FRICTION
        self.vel += self.acc
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        self.pos += self.vel + (0.5 * self.acc)

        self.hit_rect.midbottom = self.pos
        self.rect.center = self.hit_rect.center




class Enemy_1(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = ENEMY_LAYER
        self.groups = game.all_sprites, game.enemy1s
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = game.enemy1_img
        self.game = game
        self.rect = self.image.get_rect()
        self.pos = vector(x, y)
        self.rect.center = self.pos
        self.rot = 0
        self.vel = vector(0, 0)
        self.acc = vector(0, 0)
        self.health = 40

    def avoid_enemies(self):
        for enemy1 in self.game.enemy1s:
            if enemy1 != self:
                dist = self.pos - enemy1.pos
                if 0 < dist.length() < AVOID_RAD:
                    self.acc += dist.normalize()


    def update(self):
   #     self.rot = (self.game.player.pos - self.pos).angle_to(vector(1, 0))
        self.image = pg.transform.rotate(self.game.enemy1_img, self.rot)
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.pos
        self.acc = vector(1, 0).rotate(-self.rot)
    #    self.avoid_enemies()
        self.acc.scale_to_length(ENEMY1_SPEED)
        self.acc += self.vel * ENEMY1_FRICTION
        self.vel += self.acc
        self.pos += self.vel + (0.5 * self.acc)
        if self.health <= 0:
            self.kill()

        dist = (self.pos - self.game.player.pos).length()
        if dist < 800:
            block_hit_list = pg.sprite.spritecollide(self, self.game.platforms, False)
            for block in block_hit_list:
                if self.vel.y > 0:
                    if self.pos.y < block.rect.centery:
                        self.pos.y = block.rect.top + 1

                        self.vel.y = 0
                if self.vel.x > 0 and self.vel.y != 0:
                    if self.pos.x < block.rect.left:
                        self.pos.x = block.rect.left - self.rect.width / 2
                        self.vel.x = 0
                if self.vel.x < 0 and self.vel.y != 0:
                    if self.pos.x > block.rect.right:
                        self.pos.x = block.rect.right + self.rect.width / 2
                        self.vel.x = 0
                if self.vel.y < 0:
                    if self.pos.y - self.rect.height > block.rect.centery:
                        self.pos.y = block.rect.bottom + self.rect.height - 1

                        self.vel.y = 0

            block_hit_list = pg.sprite.spritecollide(self, self.game.walls, False)
            for block in block_hit_list:
                if self.vel.x > 0:
                    if self.pos.x < block.rect.left:
                        self.pos.x = block.rect.left - self.rect.width / 2
                        self.vel.x = 0

                if self.vel.x < 0:
                    if self.pos.x > block.rect.right:
                        self.pos.x = block.rect.right + self.rect.width / 2
                        self.vel.x = 0

                if self.vel.y < 0:
                    if self.pos.y - self.rect.height > block.rect.centery:
                        self.pos.y = block.rect.bottom + self.rect.height - 1

                        self.vel.y = 0


class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.x + int(WIDTH / 2)
        y = -target.rect.y + int(HEIGHT / 2)
        x = min(0, x)
        y = min(0, y)
        x = max(-(WIDTH + 3360), x)
        y = max(-(HEIGHT + 150), y)
        self.camera = pg.Rect(x, y, self.width, self.height)


class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y, width, height):
        self._layer = WALL_LAYER
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.wall_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Platform(pg.sprite.Sprite):
    def __init__(self, game, x, y, width, height):
        self._layer = WALL_LAYER
        self.groups = game.all_sprites, game.platforms
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.wall_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Door(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = WALL_LAYER
        self.groups = game.all_sprites, game.doors
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.door_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Trapdoor(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = WALL_LAYER
        self.groups = game.all_sprites, game.trapdoors
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.trapdoor_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y





class Game:
    def __init__(self):
        # intialises game window etc
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption('Hello')
        self.clock = pg.time.Clock()
        self.running = True

        self.data()

    def data(self):
        # load highest Round
        self.dir = path.dirname(__file__)
        img_folder = path.join(self.dir, 'img')

        self.door_image = pg.transform.scale(pg.image.load(path.join(img_folder, 'door.png')).convert_alpha(), (25, 40))

        self.trapdoor_image = pg.image.load(path.join(img_folder, 'trapdoor.png')).convert_alpha()

        self.enemy1_img = pg.image.load(path.join(img_folder, ENEMY_1_IMG)).convert_alpha()
        self.player_imgr = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()
        self.player_imgl = pg.image.load(path.join(img_folder, 'playerl.png')).convert_alpha()
        self.wall_img = pg.transform.scale(pg.image.load(path.join(img_folder, WALL_IMG)).convert_alpha(), (41, 41))






        icon_dir = path.join(path.dirname(__file__), 'icons')
        self.arrow_img = pg.image.load(path.join(icon_dir, 'arrow_right.png')).convert_alpha()

    def new(self):
        # starts new game

        self.score = 0
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.trapdoors = pg.sprite.Group()
        self.doors = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.drawpath = False
        self.time = 0








        self.walls = pg.sprite.Group()

        self.enemy1s = pg.sprite.Group()

      #  for enemy in self.enemy1s:
        #    timer = threading.timer(2, self.pathfind(enemy))
      #      timer.start()

        self.player = Player(self)
        self.all_sprites.add(self.player)

        self.round = 0
        self.paused = False
        self.wall_dim = 41

        self.variables = []
        self.clockt = pg.time.Clock()




        self.current = 0
        self.enemy_count = 0

        x = y = 0

        self.PLATFORM_LIST = [
            "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
            "W                                            D                                                             P",
            "W                                           PPPPPPPPPPPPPPPPPPPP                                           P",
            "WPPPPPP    PPPPPPPPP        PPPPPPP  PPPPPPPPW                                                             P",
            "W                                            W                                                             P",
            "W                          PPPP              W                                                             P",
            "W         PPPP                       PPP     W                                                             P",
            "W                              PPPP          W                                                             P",
            "W               PPPP                 PPPP    W                                                             P",
            "W     PPPP                                   W                                                             P",
            "W                PPPP                        W                                                             P",
            "W       PPPP           PPP    PPPPPPPP       W                                                             P",
            "W                                            W                                                             P",
            "W    PPPP          PPPP         PPPP         W                                                             P",
            "W                      PPPP                  W                                                             P",
            "W        PPPP                                W                                                             P",
            "W                           PPPP             W                                                             P",
            "WPPPPPPPPPPPTPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPTW                                              W              P",
            "W    PPP  PP        PPPPP       PPPP     PP  W              PPPPPP                      PPPPP              P",
            "WP              PPP                          W                                                W            P",
            "W      PPPPPPPPP           PPPP       PPP   PW                                               W             P",
            "W                 PPP                        W                         PPPPPP                W             P",
            "WPPPP                  PPPPPPPP        PPP   W                              PPPPPPPPP        W             P",
            "W     PP PPPP                     PP         W   PPPPPPPPPPPP                                W             P",
            "W                     PPPPPPPPPP             W                                               W             P",
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

        for row in self.PLATFORM_LIST:
            for col in row:
                if col == "P":
                    Platform(self, x, y, 50, 50)
                if col == "W":
                    Wall(self, x, y, 50, 50)
                if col == "D":
                    Door(self, x, y)
                if col == "T":
                    Trapdoor(self, x, y)

                x += 41
            y += 41
            x = 0

        self.camera = Camera(0, 0)

        self.map_width = len(self.PLATFORM_LIST[0]) * 41
        self.map_height = len(self.PLATFORM_LIST) * 41

        self.grid = SquareGrid(self, self.map_width, self.map_height)

        self.run()

    def run(self):
        # game loop

        self.playing = True
        while self.playing:
            self.clock.tick(60)

            self.events()
            if not self.paused:
                self.update()
            self.draw()
        pg.mixer.music.fadeout(100)

    def spawn(self):

        # increment enemy total by 2
        self.enemy_count += 1
        currentcount = 0
        while currentcount != self.enemy_count:
            x = randrange(100,  500)
            y = randrange(100, 500)
            pos = vector(x, y)
            if (self.player.pos - pos).length() > 400:
                Enemy_1(self, x, y)
                currentcount += 1

    def pathfind(self, enemy):

        start = vector(player_tile(self.player.pos))


        goal = vector(player_tile(enemy.pos))

        path = breadth_first_search(self.grid,goal,start)

        self.variables.append(start)
        self.variables.append(goal)
        self.variables.append(path)





    def update(self):
        # game loop - update

        self.all_sprites.update()
        self.camera.update(self.player)

        self.screen.fill(BLUE)
        dt = self.clockt.tick()
        self.time += dt




        keystate = pg.key.get_pressed()

        #      pg.draw.rect(self.screen, WHITE, self.player.hit_rect, 2)

        # enemy hits player

        for door in self.doors:
            dist = door.rect.center - self.player.pos
            if 0 < dist.length() < 100:
                self.draw_text("2(Q", 12, WHITE, door.rect.x, door.rect.y)
                #           self.draw_texty("2 (Q)", self.body_font, 12, WHITE, door.rect.x + 45 , door.rect.y +20, align="center")
                if 0 < dist.length() < 40 and self.score >= 2 and keystate[ord('q')]:
                    pg.mixer.Sound(path.join(self.sound_folder, 'door.wav')).play()
                    self.score -= 2
                    door.kill()

        for trapdoor in self.trapdoors:
            dist = trapdoor.rect.center - self.player.pos
            if 0 < dist.length() < 100:
#                self.draw_texty("2 (Q)", self.body_font, 12, WHITE, trapdoor.rect.x + 20, trapdoor.rect.y + 30,
          #                      align="center")
                if self.score >= 2 and keystate[ord('q')]:
                    pg.mixer.Sound(path.join(self.sound_folder, 'door.wav')).play()
                    self.score -= 2
                    trapdoor.kill()

        hits = pg.sprite.spritecollide(self.player, self.enemy1s, False)
        for hit in hits:
            self.player.health -= ENEMY1_DAMAGE
            hit.vel = vector(0, 0)
            if self.player.health <= 0:
                self.playing = False
        if hits:
            self.player.vel += vector(KNOCKBACK, 0).rotate(-hits[0].rot)





        block_hit_list = pg.sprite.spritecollide(self.player, self.platforms, False, )
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

        block_hit_list = pg.sprite.spritecollide(self.player, self.trapdoors, False, )
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

        block_hit_list = pg.sprite.spritecollide(self.player, self.doors, False, )
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

        block_hit_list = pg.sprite.spritecollide(self.player, self.walls, False, )
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



            # check if player hits coins

        if pg.mixer.Channel(0).get_busy() == False:
            pg.mixer.music.set_volume(1)

        if len(self.enemy1s) == 0:
            pg.mixer.music.set_volume(0.6)
            self.round += 1
            self.player.health = 100
            self.spawn()
        for enemy in self.enemy1s:
#            timer = threading.timer(2, self.pathfind(enemy))
        #    timer.start()
            if 0 < self.time < 200 or self.time > 3000:
                self.pathfind(enemy)

        w = 41

        arrows = {}

        self.arrow_img = pg.transform.scale(self.arrow_img, (41, 41))
        for dir in [(41, 0), (0, 41), (-41, 0), (0, -41)]:
            arrows[dir] = pg.transform.rotate(self.arrow_img, vector(dir).angle_to(vector(1, 0)))

        self.grid.draw_grid()

  #      path = breadth_first_search(self.grid, goal, start)
       # print(list(self.variables))
        # draw path from start to goal
        for enemy in self.enemy1s:
            start = self.variables[0]
            goal = self.variables[1]
            path = self.variables[2]
            current = start + path[vector_conv(start)]
            while current != goal:
                x = current.x + 41 / 2

                y = current.y + 41 / 2
                img = arrows[vector_conv(path[current.x, current.y])]
                enemy.rot = (vector(path[current.x, current.y]).angle_to(vector(1, 0))) - 180

                r = img.get_rect(center=(x, y))
                self.screen.blit(img, r)
                current = current + path[vector_conv(current)]



    def events(self):
        # game loop - events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    self.player.jump()
                if event.key == pg.K_p:
                    self.paused = not self.paused

      #  self.drawpath = True

    def draw_texty(self, text, font_name, size, colour, x, y, align="center"):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, colour)
        text_rect = text_surface.get_rect()
        if align == "center":
            text_rect.center = (x, y)

        self.screen.blit(text_surface, text_rect)




    def draw(self):
        # game loop - draw

        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))

        for sprite in self.all_sprites:


            self.screen.blit(sprite.image, self.camera.apply(sprite))





        if self.paused:
            pg.mixer.music.pause()
            self.draw_texty("Paused", self.title_font, 120, BLOOD_RED, WIDTH / 2, HEIGHT / 2, align="center")

        else:
            pg.mixer.music.unpause()




        # Flip display after drawing
        pg.display.flip()

    def show_start_screen(self):
        # game start screen
        self.screen.fill(BLACK)



        pg.display.flip()
        self.key_press()

    def show_go_screen(self):
        # game over or continue
        if not self.running:
            return
        self.screen.fill(BLACK)
        self.draw_texty("GAME OVER", self.title_font, 150, RED, WIDTH / 2, HEIGHT / 4)
        self.draw_texty("You got to round " + str(self.round), self.header_font, 50, RED, WIDTH / 2,
                        HEIGHT * 2 / 3 - 20)
        self.draw_texty("Press any key to play again", self.header_font, 50, GOLD, WIDTH / 2, HEIGHT * 3 / 4)
        if self.round > self.highscore:
            self.highscore = self.round
            self.draw_texty("NEW HIGH ROUND", self.header_font, 40, WHITE, WIDTH / 2, HEIGHT / 2, align="center")
            with open(path.join(self.dir, hs_file), 'w') as file:
                file.write(str(self.round))
        else:
            self.draw_texty("Highest Round: " + str(self.highscore), self.body_font, 20, RED, WIDTH / 2, HEIGHT / 2)
        pg.display.flip()
        self.key_press2()

    def draw_text(self, text, size, colour, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, colour)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y)
        self.screen.blit(text_surface, text_rect)

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




    pg.display.update()
# grid.find_neighbours((5*w,4*w))


pg.quit()







