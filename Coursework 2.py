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
    def__init(self):
        #intialises game window etc
        pygame.init()
        screen = pygame.display.set_mode(size)
        pygame.display.set_caption(TITLE)
        clock = pygame.time.Clock()
        self.running = True
        
    def run(self):
        #game loop
        pass
    def update(self):
        #game loop - update
        pass
    def events(self):
        #game loop - events
        pass
    def draw(self):
        #game loop - draw
        pass
    def show_start_screen(self):
        #game start screen
        pass
    def show_go_screen(self)
        #game over or continue
        pass

g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()

#player sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50,50))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (25,HEIGHT - 25)

    def update(self):
       self.speedx = 0
       self.speedy = 0
       keystate = pygame.key.get_pressed()
       if keystate[pygame.K_LEFT]:
            self.speedx = -5
       if keystate[pygame.K_RIGHT]:
            self.speedx= 5
       if keystate[pygame.K_UP]:
           self.speedy = -5
       if keystate[pygame.K_DOWN]:
           self.speedy = 5

       self.rect.y += self.speedy     
       self.rect.x += self.speedx
       
       if self.rect.right > WIDTH:
          self.rect.right = WIDTH
       if self.rect.left <0:
          self.rect.left = 0
          
       

# Open a new window
size = (1024, 500)

all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)


# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates

# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    #Update
    all_sprites.update()
   
   
 
    # --- Drawing code 
    screen.fill(WHITE)
    all_sprites.draw(screen)
   
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
    # --- Limit to 60 frames per second
    clock.tick(60)
 
pygame.quit()
