# Import the pygame library and initialise the game engine
import pygame
pygame.init()

# Define some colors (for now)
BLACK = ( 0, 0, 0)
WHITE = ( 255, 255, 255)
GREEN = ( 0, 255, 0)
RED = ( 255, 0, 0)
BLUE = (0,0,255)

WIDTH = 1024
HEIGHT = 500


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
       keystate = pygame.key.get_pressed()
       if keystate[pygame.K_LEFT]:
            self.speedx = -5
       if keystate[pygame.K_RIGHT]:
            self.speedx= 5
       self.rect.x += self.speedx
       if self.rect.right > WIDTH:
          self.rect.right = WIDTH
       if self.rect.left <0:
          self.rect.left = 0
       

# Open a new window
size = (1024, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("GAME")

all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)


# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

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
 
# Close the window and quit.
pygame.quit()
