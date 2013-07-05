#-------------------------------------------------------------------------------
# Name:        Main Game File
# Purpose:     Entry point and main code for the game.
#
# Author:      Douglas Keech
#
# Created:     16/06/2013
# Copyright:   (c) MCC Maple Woods Computer Club 2013
# Licence:     (No licence currently defined.)
#-------------------------------------------------------------------------------

import pygame
import random
import time
import gameClasses


def main():
    screen = pygame.display.set_mode([800,450])
    gameClasses.__init__(screen)
    clock = pygame.time.Clock()
    done = False
    player = gameClasses.Player()
    # Main Loop

    while not done:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
                else:
                    player.eventHandler(event)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    pass
                else:
                    player.eventHandler(event)

        #update code block
        if done:
            return # If we're done, why run all the update code?

        player.update()

        # draw code block
        screen.fill([0,0,0]) # Fill with black

        player.draw()

        pygame.display.flip() # Flip make changes visible
        clock.tick(60) # Limit execution speed.

if __name__ == '__main__':
#    init()
    main()
pygame.quit()
