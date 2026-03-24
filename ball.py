## ball.py

import pygame
import random
import math
from settings import *


class Ball:
    def __init__(self, x, y, color, gravity=True):
        self.x = x
        self.y = y
        self.vx = random.uniform(-6, 6) if gravity else random.uniform(-3, 3)
        self.vy = -(random.uniform(6, 15) + (HEIGHT - y) / 50) if gravity else random.uniform(-3, 3)
        self.bounces = random.randint(3, 7) if gravity else random.randint(5, 10)
        self.color = color
        self.effect_timer = 0
        self.trail = []
        self.gravity = gravity
        self.size = 5 if gravity else 7  # Синие шары меньше и без гравитации

    def move(self):
        global RADIUS, PULSE_EFFECT
        if self.gravity:
            self.vy += GRAVITY
        self.x += self.vx
        self.y += self.vy
        self.trail.append((int(self.x), int(self.y)))
        if len(self.trail) > (10 if not self.gravity else 5):
            self.trail.pop(0)

        if math.hypot(self.x - CENTER[0], self.y - CENTER[1]) >= RADIUS:
            self.x -= self.vx
            self.y -= self.vy
            self.vx = -self.vx * (0.9 if self.gravity else 1)
            self.vy = -self.vy * (0.8 if self.gravity else 1)
            self.bounces -= 1
            self.effect_timer = 10
            PULSE_EFFECT = 5
            if random.random() < (0.3 if self.color == BLUE else 0.1):
                RADIUS += random.choice([-5, 5])
        return self.bounces > 0

    def draw(self, screen):
        for t in self.trail:
            pygame.draw.circle(screen, self.color, t, 3 if self.color == BLUE else 2)
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
        if self.effect_timer > 0:
            pygame.draw.circle(screen, RED if self.color == YELLOW else WHITE, (int(self.x), int(self.y)),
                               self.size + 5, 1)
            self.effect_timer -= 1
