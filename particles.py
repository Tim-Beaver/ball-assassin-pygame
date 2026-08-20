from pygame import *
import settings
from math import *
import os
import settings
import random


class Particle(sprite.Sprite):
    def __init__(self, image, pos, dx, dy, group, player):
        super().__init__(group)
        self.image = image
        self.player = player
        self.rect = self.image.get_rect(center=self.player.rect.center)

        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos

    def update(self, *args):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if not self.rect.colliderect(self.player.rect):
            self.kill()


def create_particles(position, group, player, image):
    particle_count = random.randint(2, 4)
    numbers = range(-4, 4)
    for _ in range(particle_count):
        Particle(image, position, random.choice(numbers), random.choice(numbers), group, player)
