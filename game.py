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
                img = pygame.image.load(ARTPATH + str(i) + imageFile).convert()
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
        self.frameIndex += 1
        if self.frameIndex > len(self.images)-1:
            self.frameIndex = 0
        self.image = self.images[self.frameIndex]
        # Preserve former position
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center
        
    def update(self):
        if time.time() >= self.lastFlip + self.frameDelay:
            self.flipFrame()
            self.lastFlip = time.time()
        
    def draw(self):
        screen.blit(self.image, self.rect)
        
# Planned class for ships, including player and enemies
#class Ship(AnimatedSprite):
#    def __init__(self, imageFile):
#        pygame.sprite.Sprite.__init__(self)
            
        

screen = pygame.display.set_mode([800,450])
clock = pygame.time.Clock()

testAnim = AnimatedSprite("rgbcirc.png", 3, .2)
testAnim.rect.center = [100, 100]


done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    #update code block
    testAnim.update()

    
    # draw code block
    screen.fill([0,0,0])
    testAnim.draw()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
