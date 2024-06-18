import math
import os
import random
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

class Ship(pygame.sprite.Sprite):
    def __init__(self, SCREEN):
        super().__init__()
        self.o = pygame.image.load(os.path.join("Assets", "Ship.png"))
        self.image = self.o
        self.rect = self.image.get_rect(center=(1025, 750))
        self.angle = 0
        self.velocity = pygame.math.Vector2(0, -1)
        self.rotationVelocity = 1
        self.direction = 0
        self.SCREEN = SCREEN
        self.play = True
        self.radars = []  # stores a list of all the radars used by this instance of the ship

        #self.image = pygame.transform.rotozoom(self.o, 30, 0.75)
        #self.rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        self.radars.clear()
        self.drive()
        self.rotate()
        self.detection(-50)
        self.detection(50)
        self.detection(-20)
        self.detection(20)
        self.detection(0)
        self.collision()
        self.collectData()

    def drive(self):
        self.rect.center += self.velocity.normalize() * 1.0  # Move in the direction of the velocity

    def rotate(self):
        if self.direction == 1:
            self.angle -= self.rotationVelocity
            self.velocity.rotate_ip(self.rotationVelocity)
        if self.direction == -1:
            self.angle += self.rotationVelocity
            self.velocity.rotate_ip(-self.rotationVelocity)

        self.image = pygame.transform.rotozoom(self.o, self.angle, 0.75)
        self.rect = self.image.get_rect(center=self.rect.center)

    def detection(self, angle):
        length = 0
        x = int(self.rect.center[0])
        y = int(self.rect.center[1])

        while not self.SCREEN.get_at((x, y)) == pygame.Color(246, 233, 183, 255) and length < 1000:
            length += 1
            x = int(self.rect.center[0] - math.sin(math.radians(self.angle + angle)) * length)
            y = int(self.rect.center[1] - math.cos(math.radians(self.angle + angle)) * length)

        # Visuals
        pygame.draw.line(self.SCREEN, (255, 255, 255, 255), self.rect.center, (x, y), 1)
        #pygame.draw.circle(self.SCREEN, (255, 0, 0, 0), (x, y), 3)

        distance = int(math.sqrt(math.pow(self.rect.center[0] - x, 2) + math.pow(self.rect.center[1] - y, 2)))
        self.radars.append([angle, distance])

    def collision(self):
        length = 20

        # Collision points
        rightPoint = [int(self.rect.center[0] - math.sin(math.radians(self.angle + 18)) * length),
                      int(self.rect.center[1] - math.cos(math.radians(self.angle + 18)) * length)]
        leftPoint = [int(self.rect.center[0] - math.sin(math.radians(self.angle - 18)) * length),
                     int(self.rect.center[1] - math.cos(math.radians(self.angle - 18)) * length)]

        # If the ship is out of the track, end its life
        if self.SCREEN.get_at(rightPoint) == pygame.Color(246, 233, 183, 255) or self.SCREEN.get_at(leftPoint) == pygame.Color(246, 233, 183, 255):
            self.play = False

        # Draw Collision Points
        pygame.draw.circle(self.SCREEN, (0, 255, 0, 0), rightPoint, 2)
        pygame.draw.circle(self.SCREEN, (0, 255, 0, 0), leftPoint, 2)

    def collectData(self):
        input = [0, 0, 0, 0, 0]
        for i, radar in enumerate(self.radars):
            input[i] = int(radar[1])
        return input
