import pygame
import random
import math
from settings import *
from ball import Ball
from enemy import Enemy
from gate import Gate

# Списки объектов
balls = []
enemies = []
gates = []
score = 0
launches = 10
console_messages = []

# Таймеры спавна
spawn_gate_timer = 200
spawn_enemy_timer = 300

def add_console_message(message):
    """Добавляет сообщение в консоль"""
    console_messages.append(message)
    if len(console_messages) > 5:
        console_messages.pop(0)

def spawn_gate():
    """Создаёт ворота в случайной точке внешнего круга"""
    angle = random.uniform(0, 2 * math.pi)
    x = CENTER[0] + RADIUS * math.cos(angle)
    y = CENTER[1] + RADIUS * math.sin(angle)
    gates.append(Gate(x, y))
    add_console_message("Gate appeared!")

def spawn_enemy():
    """Создаёт врага в случайной точке внешнего круга"""
    angle = random.uniform(0, 2 * math.pi)
    x = CENTER[0] + RADIUS * math.cos(angle)
    y = CENTER[1] + RADIUS * math.sin(angle)
    enemy = Enemy(x, y, boss=random.random() < 0.1)
    enemies.append(enemy)
    add_console_message("Boss appeared!" if enemy.boss else "Enemy appeared!")

# Основной игровой цикл
running = True
while running:
    screen.fill(BLACK)

    # Пульсация круга
    pulse_radius = RADIUS + PULSE_EFFECT
    pygame.draw.circle(screen, WHITE, CENTER, pulse_radius, 1)
    pygame.draw.circle(screen, DARK_GRAY, CENTER, INNER_RADIUS, 1)
    if PULSE_EFFECT > 0:
        PULSE_EFFECT -= 1

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            if math.hypot(mx - CENTER[0], my - CENTER[1]) < INNER_RADIUS and launches > 0:
                launches -= 1
                balls.append(Ball(mx, my, BLUE if random.random() < 0.3 else (YELLOW if random.random() < 0.2 else WHITE)))

    # Спавн ворот и врагов
    if spawn_gate_timer <= 0:
        spawn_gate()
        spawn_gate_timer = 200
    spawn_gate_timer -= 1

    if spawn_enemy_timer <= 0:
        spawn_enemy()
        spawn_enemy_timer = 300
    spawn_enemy_timer -= 1

    # Обновление и отрисовка шаров
    new_balls = []
    for ball in balls:
        if ball.move():
            new_balls.append(ball)
    balls = new_balls

    # Обновление и отрисовка врагов
    new_enemies = []
    for enemy in enemies:
        if enemy.update(balls):
            new_enemies.append(enemy)
    enemies = new_enemies

    # Обновление и отрисовка ворот
    new_gates = []
    for gate in gates:
        gate.draw(screen)
        if gate.timer > 0:
            new_gates.append(gate)
    gates = new_gates

    # Отрисовка врагов
    for enemy in enemies:
        enemy.draw(screen)

    # Отрисовка шаров
    for ball in balls:
        ball.draw(screen)

    # Отрисовка консоли
    pygame.draw.rect(screen, GRAY, (0, HEIGHT - 100, WIDTH, 100))
    console_text = font.render(f"Balls destroyed: {score} | Launches left: {launches}", True, WHITE)
    screen.blit(console_text, (20, HEIGHT - 90))

    for i, msg in enumerate(console_messages):
        text_surface = console_font.render(msg, True, WHITE)
        screen.blit(text_surface, (20, HEIGHT - 70 + i * 15))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
