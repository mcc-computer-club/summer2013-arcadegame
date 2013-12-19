#-------------------------------------------------------------------------------
# Name:        GameClasses
# Purpose:     Defines basic classes for the arcade game. Facilitates cleaner
#              code
# Author:      Douglas Keech
#
# Created:     04/07/2013
# Copyright:   (c) MCC Maple Woods Computer Club 2013
# Licence:     (No licence currently defined.)
#-------------------------------------------------------------------------------
import random
import time

import pygame


ARTPATH = 'assets/art/'

def __init__(scrn):
    global screen
    screen = scrn
    global allSprites
    allSprites = pygame.sprite.Group()

class AnimatedSprite(pygame.sprite.Sprite):
    x=0
    y=0
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
                #terminal error
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


# Planned class for shots/bullets.
class Shot(pygame.sprite.Sprite):
    def __init__(self, xy_coord, shotType=0, flip=False):
        pygame.sprite.Sprite.__init__(self)
        if self not in allSprites:
            allSprites.add(self)
        # self.flip is a bool. When false, image is not flipped, and will face
        #   and move right. When true, image will be flipped to face and move
        #   left.
        self.flip = flip
        # if.. elif.. else.. block for setting variables dependent on shotType
        if shotType == 1:
            # Regular for now. Something else later.
            imageFile = "regshot"
            self.damage = 20
            self.vel = 10
        else:
            # If shotType ID number is not available, use regular shots.
            imageFile = "regshot"
            self.damage = 10
            self.vel = 10
        # load image for sprite
        self.image = pygame.image.load(ARTPATH + "shot/" + imageFile + ".png"
                                       ).convert_alpha()
                                       # ... Last line STILL looks ugly.
        self.rect = self.image.get_rect()
        self.rect.center = xy_coord
        if self.flip:
            print("Flipped")
            self.image = pygame.transform.flip(self.image, True, False)

    def update(self):
        # Move the shot in proper direction
        if self.flip:
            self.rect.x -= self.vel
        else:
            self.rect.x += self.vel
        # Check if off screen
        if ((self.rect.midleft[0] > screen.get_width()) or
        (self.rect.midright[0] < 0)):
            self.kill()
        # Check Collisions
        #collisionList = pygame.sprite.spritecollideany(self, allSprites)
        collisionList = pygame.sprite.Group()
        collisionList = pygame.sprite.spritecollide(self, allSprites, False)
        for sprite in collisionList:
            if isinstance(sprite, Shot):
                print("Shot on shot action")
                collisionList.remove(sprite)
            if self in collisionList:
                collisionList.remove(self)
        if len(collisionList) > 0:
            print(collisionList)
            print("in if..")
            for sprite in collisionList:
                print("In FOR loop..")
                try:
                    sprite.onCollision(self)
                    print("ran collision routine")
                except:
                    print("exception")
                    pass
                collisionList.remove(sprite)

        def onCollision(self, collSprite):
            pass

    def draw(self):
        screen.blit(self.image, self.rect)
        pygame.draw.rect(screen,[255,255,0],self.rect, 1)


# Planned class for ships. Parent to player and enemy classes
class Ship(AnimatedSprite):
    def __init__(self, xy_coord, imageFile, frames, maxhp, flip=False):
        AnimatedSprite.__init__(self, imageFile, frames, .1 , flip)
        if self not in allSprites:
            allSprites.add(self)
        self.xvel = 0
        self.yvel = 0
        self.shotsGroup = pygame.sprite.Group()
        self.shotType = 0
        self.maxShots = 3
        self.shotCooldown = .1  # Delay in secs before next shot can be fired.
        self.lastShotTime = time.time()-10 # Large negative number will always allow for
                                #   instant fire at start of life.
        self.maxHP = maxhp
        self.currHP = self.maxHP
        self.rect.center = xy_coord
        

    def shoot(self, flip=False):
        if ((self.shotCooldown < time.time() - self.lastShotTime) and
            (len(self.shotsGroup) < self.maxShots)):
            #newShot = Shot(self.rect.midright, self.shotType)
            self.shotsGroup.add(Shot(self.rect.midright, self.shotType, flip))
            self.lastShotTime = time.time()

    def onCollision(self, collSprite):
        pass
        if isinstance(collSprite, Shot):
            self.currHP -= collSprite.damage
            collSprite.kill()

    def update(self):
        # Run proper animation code
        AnimatedSprite.update(self)
        # Check if still alive.
        if self.currHP <= 0:
            pass
            #self.kill()
        # Move the ship by its velocity
        self.rect.x += self.xvel
        self.rect.y += self.yvel
        # Update the shots associated with this ship.
        self.shotsGroup.update()

    def draw(self):
        AnimatedSprite.draw(self)
        #self.shotsGroup.draw(screen)
        for shot in self.shotsGroup:
            shot.draw() #screen)


class Player(Ship):
    def __init__(self):
        Ship.__init__(self, [100,100], "testplayer", 3, 50)
        if self not in allSprites:
            allSprites.add(self)
        self.speed = 5

    def eventHandler(self, event):
        if event.type == pygame.KEYDOWN:
            # Movement keys
            if event.key == pygame.K_UP:
                self.yvel -= self.speed
                if self.yvel < -self.speed:
                    self.yvel = -self.speed
            if event.key == pygame.K_DOWN:
                self.yvel += self.speed
                if self.yvel > self.speed:
                    self.yvel = self.speed
            if event.key == pygame.K_LEFT:
                self.xvel -= self.speed
                if self.xvel < -self.speed:
                    self.xvel = -self.speed
            if event.key == pygame.K_RIGHT:
                self.xvel += self.speed
                if self.xvel > self.speed:
                    self.xvel = self.speed
            # Action keys. Will use inline comments for each.
            if event.key == pygame.K_SPACE:  # Shoot.
                self.shoot()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                self.yvel -= self.speed
            if event.key == pygame.K_UP:
                self.yvel += self.speed
            if event.key == pygame.K_RIGHT:
                self.xvel -= self.speed
            if event.key == pygame.K_LEFT:
                self.xvel += self.speed

    def onCollision(self, collSprite):
        pass
        if isinstance(collSprite, Shot):
            if collSptite in self.shotsGroup:
                pass
            else:
                Ship.onCollision(self, collSprite)
        else:
            Ship.onCollision(self, collSprite)

    def update(self):
        Ship.update(self)

    def draw(self):
        Ship.draw(self)
        pygame.draw.rect(screen, [0,0,255], self.rect, 1)


class Enemy(Ship):
    def __init__(self):
        Ship.__init__(self, [100,100], "testplayer", 3, 50, True)
        if self not in allSprites:
            allSprites.add(self)
        self.speed = 5
        self.image = pygame.transform.flip(self.image, True, False)

    def update(self):
        Ship.update(self)

    def draw(self):
        Ship.draw(self)
        pygame.draw.rect(screen, [255,0,0], self.rect, 1)


