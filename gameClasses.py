#-------------------------------------------------------------------------------
# Name:        GameClasses
# Purpose:     Defines basic classes for the arcade game. Facilitates cleaner
#              code
# Author:      MCC Computer Club
#              Douglas Keech
# Created:     04/07/2013
# Copyright:   (c) MCC Maple Woods Computer Club 2013
# Licence:     (No licence currently defined.)
#-------------------------------------------------------------------------------
import random
import time

import pygame


ARTPATH = './assets/art/'

def __init__(scrn):
    global screen
    screen = scrn
    global allSprites
    allSprites = pygame.sprite.Group()

    # Unimplemented Global lists. Let's hope we can kill the allSprites list.
    #
    #shotSprites = pygame.sprite.Group()
    #shipSprites = pygame.sprite.Group()


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
                print("Someone used the wrong filename! "+ARTPATH+imageFile+str(i)+".png")
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
        self.lastUpdateTime = time.time()

    def update(self):
        # Move the shot in proper direction
        deltaTime = time.time() - self.lastUpdateTime
        if self.flip:
            self.rect.x -= self.vel * deltaTime
        else:
            self.rect.x += self.vel * deltaTime
        # Check if off screen
        if ((self.rect.midleft[0] > screen.get_width()) or
        (self.rect.midright[0] < 0)):
            self.kill()
        self.lastUpdateTime = time.time()


    # Check Collisions
    def checkCollisions(self):
        collisionList = pygame.sprite.Group()
        collisionList = pygame.sprite.spritecollide(self, allSprites, False)
        #for sprite in collisionList:
        #    if isinstance(sprite, Shot):
        #        #print("Shot on shot action")
        #        collisionList.remove(sprite)
        if self in collisionList:
            collisionList.remove(self)
        if len(collisionList) > 0:
            print(len(collisionList), collisionList)
            print("in if..")
            for sprite in collisionList:
                print("In FOR loop..")
                try:
                    sprite.onCollision(self)
                    print("ran collision routine: ", sprite)
                except:
                    print("exception")
                    pass
                collisionList.remove(sprite)

    def onCollision(self, collSprite):
        if isinstance(collSprite, Ship):
            if self not in collSprite.shotsGroup:
                collSprite.currHP -= self.damage
                self.kill()

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
        self.x = self.rect.center[0]
        self.y = self.rect.center[1]
        self.lastUpdateTime = time.time()

        #debugging stuff
        pygame.font.init()
        self.bugFont = pygame.font.SysFont("consolas", 12)
        self.bugLabelX = self.bugFont.render("",1,(0,0,255))
        self.bugLabelY = self.bugFont.render("",1,(0,0,255))

    def update(self):
        # Run proper animation code
        AnimatedSprite.update(self)
        # Check if still alive.
        if self.currHP <= 0:
            self.kill()
        # Move the ship by its velocity
        deltaTime = time.time() - self.lastUpdateTime
        self.x += self.xvel * deltaTime
        self.y += self.yvel * deltaTime
        print(deltaTime)
        self.rect.center = [self.x, self.y]
        #self.bugLabelX = self.bugFont.render("Xvel:" + str(self.xvel * deltaTime) + " - " + str(self.rect.x), 1, (0,0,255))
        #self.bugLabelY = self.bugFont.render("Yvel:" + str(self.yvel * deltaTime) + " - " + str(self.rect.y), 1, (0,0,255))
        self.bugLabelX = self.bugFont.render(str(self.xvel) + " - " + str(self.rect.x), 1, (0,0,255))
        self.bugLabelY = self.bugFont.render(str(self.yvel) + " - " + str(self.rect.y), 1, (0,0,255))

        #print("Xvel:" + str(self.xvel * deltaTime) + " - " + str(self.rect.x))
        #print("Yvel:" + str(self.yvel * deltaTime) + " - " + str(self.rect.y))
        # Update the shots associated with this ship.
        self.shotsGroup.update()
        self.checkCollisions()
        self.lastUpdateTime = time.time()

    def shoot(self, flip=False):
        if ((self.shotCooldown < time.time() - self.lastShotTime) and
            (len(self.shotsGroup) < self.maxShots)):
        #if (1 == 1):
            #newShot = Shot(self.rect.midright, self.shotType)
            if flip:
                self.shotsGroup.add(Shot(self.rect.midleft, self.shotType, flip))
            else:
                self.shotsGroup.add(Shot(self.rect.midright, self.shotType, flip))
            self.lastShotTime = time.time()

    def onCollision(self, collSprite):
        if isinstance(collSprite, Shot):
            self.currHP -= collSprite.damage
            collSprite.kill()

    # Check Collisions
    def checkCollisions(self):
        collisionList = pygame.sprite.Group()
        collisionList = pygame.sprite.spritecollide(self, allSprites, False)
        #for sprite in collisionList:
        #    if isinstance(sprite, Shot):
        #        #print("Shot on shot action")
        #        collisionList.remove(sprite)
        if self in collisionList:
            collisionList.remove(self)
        if len(collisionList) > 0:
            for sprite in collisionList:
                try:
                    sprite.onCollision(self)
                except:
                    pass
                collisionList.remove(sprite)

    def die(self):
        self.kill

    def draw(self):
        AnimatedSprite.draw(self)
        #self.shotsGroup.draw(screen)
        screen.blit(self.bugLabelX, (self.rect.x, self.rect.y - 30))
        screen.blit(self.bugLabelY, (self.rect.x, self.rect.y - 15))
        for shot in self.shotsGroup:
            shot.draw() #screen)


class Player(Ship):
    def __init__(self):
        Ship.__init__(self, [100,100], "testplayer", 3, 50)
        if self not in allSprites:
            allSprites.add(self)
        self.speed = 5
        self.shooting = 0

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
                self.shooting = 1
                #self.shoot()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                self.yvel += self.speed
            if event.key == pygame.K_DOWN:
                self.yvel -= self.speed
            if event.key == pygame.K_LEFT:
                self.xvel += self.speed
            if event.key == pygame.K_RIGHT:
                self.xvel -= self.speed

            if event.key == pygame.K_SPACE:
                self.shooting = 0

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
        if self.shooting == 1:
            self.shoot()
        print(self.currHP)

    def draw(self):
        Ship.draw(self)
        pygame.draw.rect(screen, [0,0,255], self.rect, 1)


class Enemy(Ship):
    def __init__(self, xy_coord):
        Ship.__init__(self, xy_coord, "testplayer", 3, 50, True)
        if self not in allSprites:
            allSprites.add(self)
        self.speed = 5
        self.image = pygame.transform.flip(self.image, True, False)

    def update(self):
        Ship.update(self)
        self.shoot(True)


    def draw(self):
        Ship.draw(self)
        pygame.draw.rect(screen, [255,0,0], self.rect, 1)