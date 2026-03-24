## gate.py

import pygame
import random
from settings import *


class Gate:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.timer = 20  # Эффект исчезновения

    def draw(self, screen):
        if self.timer > 0:
            pygame.draw.rect(screen, BLUE, (self.x - 10, self.y - 10, 20, 20), 1)
            self.timer -= 1

    def check_collision(self, ball):
        if math.hypot(ball.x - self.x, ball.y - self.y) < ball.size + 10:
            self.timer = 0  # Убираем ворота после взаимодействия
            return True
        return False