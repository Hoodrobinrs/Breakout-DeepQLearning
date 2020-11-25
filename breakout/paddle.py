"""Module containing the paddle sprite"""
import pygame
from variables import *

class Paddle(pygame.sprite.Sprite):
    """Paddle sprite"""

    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.color = color
        self.width = width
        self.height = height
        self.rect = None
        self.speed = 0

    def paint(self):
        """Method painting the sprite"""
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        pygame.draw.rect(self.image, self.color, [0, 0, self.width, self.height])
        self.rect = self.image.get_rect()

    def move_left(self, pixels):
        """Moves the paddle left by x pixels"""
        self.rect.x -= pixels
        self.speed = -10
        if self.rect.x < 0:
            self.rect.x = 0

    def move_right(self, pixels):
        """Moves the paddle right by x pixels"""
        self.rect.x += pixels
        self.speed = 10
        if self.rect.x > 700:
            self.rect.x = 700

    def not_moving(self):
        """Sets speed to 0"""
        self.speed = 0
