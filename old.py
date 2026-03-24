import pygame
import random
import math

# Инициализация Pygame
pygame.init()

# Размеры экрана
WIDTH, HEIGHT = 1920, 800
CENTER = (WIDTH // 2, HEIGHT // 2)
RADIUS = 250  # Радиус круга
GRAVITY = 0.2  # Гравитация
pulse_effect = 0  # Эффект пульсации круга

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Настройка экрана
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ASCII Physics Ball Game")

# Шрифты
font = pygame.font.SysFont("Courier", 18)


def inside_circle(x, y):
    return math.sqrt((x - CENTER[0]) ** 2 + (y - CENTER[1]) ** 2) <= RADIUS


# Класс шариков
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
        self.size = 5 if gravity else 7  # Уменьшенный размер синих шаров

    def move(self):
        global RADIUS, pulse_effect
        if self.gravity:
            self.vy += GRAVITY
        self.x += self.vx
        self.y += self.vy
        self.trail.append((int(self.x), int(self.y)))
        if len(self.trail) > (10 if not self.gravity else 5):
            self.trail.pop(0)

        # Проверка на отскоки
        if not inside_circle(self.x, self.y):
            self.x -= self.vx
            self.y -= self.vy
            self.vx = -self.vx * (0.9 if self.gravity else 1)
            self.vy = -self.vy * (0.8 if self.gravity else 1)
            self.bounces -= 1
            self.effect_timer = 10  # Запуск эффекта при отскоке
            pulse_effect = 5  # Пульсация круга
            if random.random() < (0.3 if self.color == BLUE else (0.1 if self.gravity else 0.05)):
                RADIUS += random.choice([-5, 5])
        return self.bounces > 0

    def draw(self):
        for t in self.trail:
            pygame.draw.circle(screen, self.color, t, 3 if self.color == BLUE else 2)
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
        if self.effect_timer > 0:
            pygame.draw.circle(screen, RED if self.color == YELLOW else WHITE, (int(self.x), int(self.y)),
                               self.size + 5, 1)
            self.effect_timer -= 1


# Игровой цикл
balls = []
score = 0
running = True

while running:
    screen.fill(BLACK)

    # Отрисовка пульсирующего круга
    pulse_radius = RADIUS + pulse_effect
    pygame.draw.circle(screen, WHITE, CENTER, pulse_radius, 1)
    if pulse_effect > 0:
        pulse_effect -= 1

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            if inside_circle(mx, my):
                if random.random() < 0.3:  # 30% шанс появления синего шара
                    balls.append(Ball(mx, my, BLUE, gravity=False))
                else:
                    balls.append(Ball(mx, my, YELLOW if random.random() < 0.2 else WHITE))

    # Обновление и отрисовка шаров
    new_balls = []
    for ball in balls:
        if ball.move():
            new_balls.append(ball)
        else:
            score += 1  # Учёт уничтоженного шарика
            ball.effect_timer = 15  # Эффект исчезновения
    balls = new_balls

    for ball in balls:
        ball.draw()

    # Отображение ASCII-консоли
    console_text = f"[ Console: Balls destroyed: {score} ]"
    text_surface = font.render(console_text, True, WHITE)
    screen.blit(text_surface, (20, HEIGHT - 30))

    pygame.display.flip()
    pygame.time.delay(30)

pygame.quit()
