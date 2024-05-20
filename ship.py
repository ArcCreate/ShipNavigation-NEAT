import math
import os
import pygame

class Ship(pygame.sprite.Sprite):

    #consturctor 
    def __init__(self):
        super().__init__()
        self.o = pygame.image.load(os.path.join("Assets", "Ship.png"))
        self.image = self.o
        self.rect = self.image.get_rect(center = (400, 400))
        self.driving = False
        self.velocity = pygame.math.Vector2(0, -0.1)
        self.angle = 0
        self.rotationVelocity = 1
        self.direction = 0

    #updating function for pygame
    def update(self):
        self.drive()
        self.rotate()

    #driving function
    def drive(self):
        if self.driving:
            self.rect.center += self.velocity * 10  # Move in the direction of the velocity

    #rotates car while driving
    def rotate(self):        
        if self.direction == 1:
            self.angle -= self.rotationVelocity
            self.velocity.rotate_ip(self.rotationVelocity)
        if self.direction == -1:
            self.angle += self.rotationVelocity
            self.velocity.rotate_ip(-self.rotationVelocity)

        self.image = pygame.transform.rotozoom(self.o, self.angle, 0.75)
        self.rect = self.image.get_rect(center = self.rect.center)
        