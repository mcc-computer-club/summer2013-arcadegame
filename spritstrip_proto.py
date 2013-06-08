# Sprite Strip animation prototype.
#
# BUGGY! Will not currently work right.
# Might look into Pyganim for animation.

import pygame

class aniSprite(pygame.sprite.Sprite):
    frameCount = 1
    currentFrame = 1
    def __init__(self, frameCount):
        pygame.sprite.Sprite.__init__(self)
        self.frameCount = frameCount
        # Load a sprite image in.
        self.spriteStrip = pygame.image.load("assets\\art\spritestriptest.png").convert()
        self.spriteStrip.set_colorkey([ 255,   0, 255])
        print(pygame.image.tostring(self.spriteStrip, "RGBA"))
        #self.image = pygame.image.load("assets\\art\spritestriptest.png").convert()
        #self.image = pygame.surface.Surface([int(self.spriteStrip.get_width()/self.frameCount)*(self.currentFrame-1),
        #                             self.spriteStrip.get_height()])
        #self.image = pygame.image([int(self.spriteStrip.get_width()/self.frameCount)*(self.currentFrame-1),
        #                             self.spriteStrip.get_height()])
        #self.image = self.image.blit(self.spriteStrip, [0,0],
        #                             pygame.rect.Rect(0,0,50,50))
                                     #self.image.get_rect())
                                     #[(int(self.spriteStrip.get_width()/self.frameCount)*(self.currentFrame-1)),
                                     #self.spriteStrip.get_height()])
        #self.image.set_colorkey([ 255,   0, 255 ])
        # Get image deminsions
        self.rect = self.image.get_rect()
        self.rect.width /= frameCount
        
        
    def animate(self):
        currentFrame += 1
        if currentFrame > frameCount:
            currentFrame = 1
        self.image.scroll(int(self.image.get_width()/self.frameCount)*self.currentFrame,0)
        

    def update(self):
        self.animate

pygame.init()

screen = pygame.display.set_mode([400, 400])

ships_array = pygame.sprite.Group()
ship = aniSprite(4)
ship.rect.x = 175
ship.rect.y = 175
ships_array.add(ship)

clock = pygame.time.Clock()
done = False
while not done:
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True


    ship.update()

    screen.fill([0,0,0])

    #ship.draw(screen)
    ships_array.draw(screen)

    pygame.display.flip()

pygame.quit()
