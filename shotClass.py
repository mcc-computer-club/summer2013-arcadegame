__author__ = 'MCC-Computer Club'

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
        pygame.draw.rect(screen, [255, 255, 0], self.rect, 1)