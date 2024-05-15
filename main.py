import neat
import os
import sys
import pygame
import math
from ship import Ship

#Screen Variables
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 900
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
TRACK = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "Track1.png")), (SCREEN_WIDTH, SCREEN_HEIGHT))

ship = pygame.sprite.GroupSingle(Ship())

def eval_genomes():
    #game loop
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        #track image on screen
        SCREEN.blit(TRACK, (0, 0))    

        #input
        input = pygame.key.get_pressed()
        if sum(pygame.key.get_pressed()) <= 1:
            ship.sprite.driving = False
        
        if input[pygame.K_UP]:
            ship.sprite.driving = True

        ship.draw(SCREEN)
        s = ship.sprite
        pygame.draw.rect(SCREEN, (255, 255, 255), s.rect, 2)
        ship.update()
        pygame.display.update()

eval_genomes()

