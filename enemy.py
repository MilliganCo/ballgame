## enemy.py

import pygame
import random
import math
from settings import *


class Enemy:
    def __init__(self, x, y, boss=False):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.health = 5 if boss else 3
        self.boss = boss
        self.color = RED if not boss else GREEN

    def update(self, balls):
        if self.health <= 0:
            return False
        target = None
        min_distance = float('inf')
        for ball in balls:
            dist = math.hypot(ball.x - self.x, ball.y - self.y)
            if dist < min_distance:
                min_distance = dist
                target = ball
        if target:
            dx, dy = target.x - self.x, target.y - self.y
            distance = math.hypot(dx, dy)
            if distance > 0:
                self.vx = (dx / distance) * 1.5
                self.vy = (dy / distance) * 1.5
        self.x += self.vx
        self.y += self.vy
        return True

    def take_damage(self, damage):
        self.health -= damage
        if self.health == 2:
            self.color = DARK_RED
        elif self.health == 1:
            self.color = DARKER_RED

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 15 if self.boss else 10)
