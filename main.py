from ctypes.wintypes import HFONT
import neat
import os
import sys
import neat.config
import pygame
import math
from ship import Ship

pygame.init()

#Screen Variables
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 900
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
TRACK = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "Track4.png")), (SCREEN_WIDTH, SCREEN_HEIGHT))
FONT = pygame.font.Font('freesansbold.ttf', 25)


def eval_genomes(genomes, config):
    #global variables for the AI to use
    global ships, ge, nets, SCORE, best, lastBest
    ships = []
    ge = []
    nets = []
    SCORE = 0
    best = 0
    lastBest = 0
    clock = pygame.time.Clock()

    #connecting all lists
    for genome_id, genome in genomes:
        ship = pygame.sprite.GroupSingle(Ship(SCREEN))
        ships.append(ship)
        ge.append(genome)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        genome.fitness = 0
    
    #Screen stats
    def statistics():
        global ships, ge, SCORE
        SCORE += 1
        text = FONT.render("Current Score: " + str(SCORE), True, (0,0,0))
        text_1 = FONT.render(f'Ships Alive:  {str(len(ships))}', True, (18, 105, 29))
        text_2 = FONT.render(f'Current Generation:  {pop.generation+1}', True, (0, 0, 0))
        text_3 = FONT.render(f'Max Score from ancestor:  {lastBest}', True, (222, 155, 64))

        SCREEN.blit(text, (50, 690))
        SCREEN.blit(text_1, (50, 730))
        SCREEN.blit(text_2, (50, 770)) 
        SCREEN.blit(text_3, (50, 810))

    #game loop
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        #track image on screen
        SCREEN.blit(TRACK, (0, 0))    
        statistics()

        #if no more ships then break out
        if len(ships) == 0:
            lastBest = best
            break

        #collision logic
        for i, ship in enumerate(ships):
            ge[i].fitness += 1
            if ship.sprite.play == False:
                if ge[i].fitness > best:
                    best = ge[i].fitness
                removeShip(i)
        
        #inputs and outputs into NEAT
        for i, ship in enumerate(ships):
            #input
            output = nets[i].activate(ship.sprite.collectData())

            #get outputs
            decision = output.index(max(output))

            #action based on output
            if decision == 1:
                ship.sprite.direction = 1
            elif decision == 2:
                ship.sprite.direction = -1
            else:
                ship.sprite.direction = 0
            

        clock.tick(60)
        # Screen drawing
        for ship in ships:
            ship.draw(SCREEN)
            ship.update()
        pygame.display.update()

#runs NEAT
def run(config_path):
    global pop, best_genome, best_fitness
    config = neat.config.Config(
        #default algorithms for simplicity
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        #file path
        config_path
    )

    #population
    pop = neat.Population(config)
    #number of gens
    pop.run(eval_genomes, 50)

#removes after death
def removeShip(index):
    ships.pop(index)
    ge.pop(index)
    nets.pop(index)

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    for _ in range(1):
        run(config_path)


