"""Module containing the ball sprite"""
import pygame
from random import randint
from breakout.variables import *

class Ball(pygame.sprite.Sprite):
    """Ball sprite"""

    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.color = color
        self.width = width
        self.height = height
        self.velocity = [randint(1, 8), -randint(4, 8)]
        self.rect = None

    def paint(self):
        """Method painting the sprite"""
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        pygame.draw.rect(self.image, self.color, [0, 0, self.width, self.height])
        self.rect = self.image.get_rect()

    def restore(self):
        """Restores ball position after live loss"""
        self.rect.x = 345
        self.rect.y = 460
        self.velocity = [randint(-1, 8), -randint(4, 8)]

    def update(self):
        """Update the ball's position"""
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

    def bounce(self):
        """Bounce after collision"""
        self.velocity[1] = -self.velocity[1]
        self.velocity[0] = randint(-8, 8)
        if self.velocity[0] == 0:
            self.velocity[0] = 4

    def bounce_paddle(self, paddle):
        """Bounce after collision with paddle"""
        self.velocity[1] = -self.velocity[1]
        self.velocity[0] = self.velocity[0] + paddle.speed/2 + randint(-4, 4)
        if self.velocity[0] > 8:
            self.velocity[0] = 8
        if self.velocity[0] < -8:
            self.velocity[0] = -8
