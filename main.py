import neat
import os
import sys
import neat.config
import pygame
import math
from ship import Ship

#Screen Variables
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 900
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
TRACK = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "Track1.png")), (SCREEN_WIDTH, SCREEN_HEIGHT))


def eval_genomes(genomes, config):
    #global variables for the AI to use
    global ships, ge, nets
    ships = []
    ge = []
    nets = []

    #connecting all lists
    for genome_id, genome in genomes:
        ship = pygame.sprite.GroupSingle(Ship(SCREEN))
        ships.append(ship)
        ge.append(genome)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        genome.fitness = 0

    #game loop
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        #track image on screen
        SCREEN.blit(TRACK, (0, 0))    

        #if no more ships then break out
        if len(ships) == 0:
            break

        #collision logic
        for i, ship in enumerate(ships):
            ge[i].fitness += 0.1
            if ship.sprite.play == False:
                removeShip(i)
        
        #inputs and outputs into NEAT
        for i, ship in enumerate(ships):
            #input
            output = nets[i].activate(ship.sprite.collectData())

            #action based on output
            if output[0] > 0.7:
                ship.sprite.direction = 1
            elif output[1] > 0.7:
                ship.sprite.direction = -1
            elif(output[0] <= 0.7 and output[1] <= 0.7):
                ship.sprite.direction = 0
            

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


