## settings.py

import pygame
import math

# Размеры экрана
WIDTH, HEIGHT = 800, 650  # Увеличена высота для интерфейса
CENTER = (WIDTH // 2, HEIGHT // 2 - 50)
RADIUS = 250  # Радиус внешнего круга
INNER_RADIUS = RADIUS // 3  # Внутренний круг (область запуска)
GRAVITY = 0.2  # Гравитация
FPS = 60  # Ограничение кадров в секунду
PULSE_EFFECT = 0  # Пульсация круга

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
DARK_GRAY = (50, 50, 50)
GREEN = (0, 255, 0)
GRAY = (100, 100, 100)  # Цвет фона консоли
DARK_RED = (150, 0, 0)  # Ослабленный враг
DARKER_RED = (100, 0, 0)  # Почти уничтоженный враг

# Настройка Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ASCII Physics Ball Game")
font = pygame.font.SysFont("Courier", 18)
console_font = pygame.font.SysFont("Courier", 14)
clock = pygame.time.Clock()