##
## There was discussion of having a moving starry background.
##

import pygame, random
pygame.init()

invisibleKey = [ 255,   0, 255 ]  # Bright Magenta will be made transparent.

class Star(pygame.sprite.Sprite):
    xvel = 0
    yvel = 0
    factor = float(1) #controls size
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        # Load a sprite image in.
        self.image = pygame.image.load('assets\\art\star.png').convert()
        self.image.set_colorkey(invisibleKey)
        
        # Get image dimensions into the rect object
        self.rect = self.image.get_rect()
        
    def transform(self):
        center = self.rect.center
        self.image =  pygame.transform.scale(self.image,
                                             [int(self.rect.width*self.factor),
                                              int(self.rect.height*self.factor)])
        self.rect = self.image.get_rect()
        self.rect.center = center
        
    def update(self):
        global screen
        self.rect.x += self.xvel
        self.rect.y += self.yvel

        sWidth = screen.get_width()
        sHeight = screen.get_height()
        # Check if gone off right side
        if self.rect.x > screen.get_width():
            self.rect.x = random.randrange((0-self.rect.width*10),
                                           (0-self.rect.width*1))
            #print ("off right")
        # check if gone off left side
        if self.rect.x + self.rect.width < 0:
            self.rect.x = random.randrange(screen.get_width(),
                                           screen.get_width()*5)
            #print ("off left")
        # check if gone off bottom
        if self.rect.y + self.rect.height > screen.get_height():
            self.rect.y = random.randrange((0-self.rect.height*10),
                                           (0-self.rect.height*1))
            #print ("off bottom")

        #
        # This block makes stars stay off of the viewport completely
        # Whoops!
        #
        #check if gone off top
        #if self.rect.y - self.rect.height < 0:
        #    self.rect.y = random.randrange(screen.get_height(),
        #                                   screen.get_height()*5)
        #    print ("off top")
            
            

# Define screen
screen_width = 450
screen_height = 700
screen  = pygame.display.set_mode([screen_width, screen_height])

# Building the starfield
starField = pygame.sprite.Group()

# number in range is how many stars will be in the star field
for i in range(100):
    star = Star()

    star.rect.x = random.randrange(screen_width)
    star.rect.y = random.randrange(screen_height)
    #star.xvel = random.randrange(-2,2)*10
    star.xvel = 0
    star.yvel = random.randrange(1,4)*5
    star.factor = (1/8)*(star.yvel/5)
    star.transform()
    starField.add(star)


clock = pygame.time.Clock()
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    starField .update()

    screen.fill([0,0,0])
    starField.draw(screen)
    pygame.display.flip()

    clock.tick(20)

pygame.quit()
