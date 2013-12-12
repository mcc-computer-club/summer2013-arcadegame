__author__ = ' '

import pygame

class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, imageFile, frames, frameDelay=.1, flip=False):
        pygame.sprite.Sprite.__init__(self)
        if self not in allSprites:
            allSprites.add(self)
        # Set up frame delay timing variables
        self.frameDelay = frameDelay
        self.lastFlip = time.time()
        # Load frames into self.images array of surface objects.
        self.images = []
        self.frameIndex = 0
        # Set if flipped.
        self.flip = flip
        for i in range(frames):
            try:
                # File name is such: "path\to\file\spriteX.png" Where X is
                #   frame number.
                img = pygame.image.load(ARTPATH + imageFile + str(i) + ".png"
                                        ).convert_alpha()
                                        #Last line looks ugly but I'm trying to
                                        # follow PEP 8!
                #img.set_colorkey([255, 0, 255])
            except:
                # Terminal error
                # Change Error messages after release.
                print("Someone used the wrong filename!")
                print("Or, well, is missing the files. Bad files!")
                print("Quitting now, bye.")
                pygame.quit()
                quit()
            if flip:
                img = pygame.transform.flip(img, True, False)
            self.images.append(img)
        self.image = self.images[0]
        self.rect = self.image.get_rect()

    def flipFrame(self):
        self.frameIndex += int((time.time() - self.lastFlip) // self.frameDelay)
        if self.frameIndex > len(self.images)-1:
            self.frameIndex = 0
        self.image = self.images[self.frameIndex]
        # Preserve former position
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center
        # set the time of the flip under lastFlip
        self.lastFlip = time.time()

    def update(self):
        # check for frame flip
        if time.time() >= self.lastFlip + self.frameDelay:
            self.flipFrame()

    def draw(self):
        screen.blit(self.image, self.rect)
