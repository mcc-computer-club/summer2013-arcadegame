# Main game file
# currently had a test object for the AnimatedSprite class.

import pygame, random, time

# Constants
ARTPATH = 'assets\\art\\'


class AnimatedSprite(pygame.sprite.Sprite):
    x=0
    y=0
    images = []
    frameIndex = 0
    frameDelay = 0
    lastFlip = time.time()
    rect = pygame.Rect(0,0,0,0)
    def __init__(self, imageFile, frames, frameDelay=.1):
        pygame.sprite.Sprite.__init__(self)
        self.frameDelay = frameDelay
        # Load frames into self.images array of surface objects.
        for i in range(frames):
            try:
                # file name is such: "path\to\file\Xsprite.png" Where x is frame number.
                img = pygame.image.load(ARTPATH + imageFile + str(i) + ".png").convert_alpha()
                img.set_colorkey([255, 0, 255])
            except:
                #terminal error
                # Change Error messages after release.
                print("Someone used the wrong filename, or doesn't have the files.")
                print("Quitting now, bye.")
                pygame.quit()
                quit()
            self.images.append(img)
        self.image = self.images[0]
        self.rect = self.image.get_rect()

    def flipFrame(self):
        self.frameIndex += (time.time() - self.lastFlip) // self.framDelay
        if self.frameIndex > len(self.images)-1:
            self.frameIndex = 0
        self.image = self.images[self.frameIndex]
        # Preserve former position
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center
        #set the time of the flip under lastFlip
        self.lastFlip = time.time()
        
    def update(self):
        if time.time() >= self.lastFlip + self.frameDelay:
            self.flipFrame()
        
    def draw(self):
        screen.blit(self.image, self.rect)
        
# Planned class for shots/bullets.
class Shot(pygame.sprite.Sprite()):
    def __init__(self, [x,y], shotType=0, flip=False): 
        pygame.sprite.Sprite.__init__(self)
        # if.. elif.. else.. block for setting variables dependent on shotType
        if shotType == 1:
            imageFile = "regshot" # Regular for now. Something else later
            self.damage = 20
        else:
            imageFile = "regshot" # if shotType ID no. is not available, use regular shots
            self.damage = 10
        # load image for sprite
        self.image = pygame.image.load(ARTPATH + "shot\\" + imageFile + ".png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        
# Planned class for ships, including player and enemies
class Ship(AnimatedSprite):
    maxHP = int()
    currHP = int() # Current HP
    rect = pygame.rect.Rect()
    shotsArray = pygame.sprite.Group() # An array to hold all subsidiary shot objects
    def __init__(self, imageFile, maxhp, [x,y]):
        AnimatedSprite._init_(self)
        self.maxHP = HP
        self.hp = self.maxHP
        self.rect.center = [x,y]

    def shoot(self):
        
            
        

screen = pygame.display.set_mode([800,450])
clock = pygame.time.Clock()


done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    #update code block

    
    # draw code block
    screen.fill([0,0,0])
    testAnim.draw()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
