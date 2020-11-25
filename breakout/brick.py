"""Module containing the ball sprite"""
import pygame
from breakout.variables import *

class Brick(pygame.sprite.Sprite):
    """Brick sprite"""

    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.color = color
        self.width = width
        self.height = height
        self.rect = None

    def paint(self):
        """Method painting the sprite"""
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        pygame.draw.rect(self.image, self.color, [0, 0, self.width, self.height])
        self.rect = self.image.get_rect()
