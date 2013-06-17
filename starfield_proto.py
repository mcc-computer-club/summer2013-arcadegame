##
## There was discussion of having a moving starry background.
##

import pygame, random

invisibleKey = [ 255,   0, 255 ]  # Bright Magenta will be made transparent.


class Star(pygame.sprite.Sprite):
    xvel = 0
    yvel = 0
    rotVel = 1
    rotAngle = 0
    factor = float(1) #controls size
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # Load a sprite image in.
        self.image = pygame.image.load('assets\\art\star.png').convert()
        self.image.set_colorkey(invisibleKey)
        # Get image dimensions into the rect object and set X,Y coords.
        self.rect = self.image.get_rect()
        self.rotAngle = 0
        
        
    def transform(self):
        center = self.rect.center
        self.origWidth = self.image.get_width()
        self.origHeight = self.image.get_height()
        self.image =  pygame.transform.scale(self.image,
                                             [int(self.rect.width*self.factor),
                                              int(self.rect.height*self.factor)])
        self.rect = self.image.get_rect()
        self.rect.center = center

    def reset_vars(self):
        # Set X, Y coords and velocity.
        self.rect.x = random.randrange(screen.get_width())
        self.rect.y = random.randrange((0-self.rect.height*2),
                                       (0-self.rect.height*1) , 1)
        
        
    def update(self):
        global screen       #seems easier to extend scope of screen.
        self.rect.x += self.xvel
        self.rect.y += self.yvel
        # check if gone off bottom
        if self.rect.y - self.rect.height > screen.get_height():
            self.reset_vars()

        # rotate
        #self.rotAngle += self.rotVel
        #if self.rotAngle > 360-self.rotVel:
        #    self.rotAngle = 0
        #self.image = pygame.transform.rotozoom(self.image, self.rotVel, 1)
            
        
pygame.init()

# Define screen at 450x800 (700 height is being used for testing
#   since my screen at least is short)
screen_width = 450
screen_height = 500
screen  = pygame.display.set_mode([screen_width, screen_height])

# Building the starfield
starField = pygame.sprite.Group()
for i in range(100): # Only handle 50 star sprites in starfield
    star = Star()

    # Set X, Y coords and velocity.
    star.rect.x = random.randrange(screen_width)
    star.rect.y = random.randrange(screen_height)
    #star.xvel = random.randrange(-2,2)*10
    star.xvel = 0
    star.yvel = random.randrange(1,7)*1

    # Adjust opacity
    star.image.set_alpha((star.yvel/1)*(255/6))

    # Scaling code
    star.factor = (1/6)*(star.yvel/1)
    star.transform()
    starField.add(star)


clock = pygame.time.Clock()
done = False
while not done:
# Events section
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

# update section
    starField.update()

# draw section
    screen.fill([0,0,0])
    starField.draw(screen)
    pygame.display.flip()

    clock.tick(20)

pygame.quit()
