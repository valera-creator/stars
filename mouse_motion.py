import os
import random

import pygame

pygame.init()
fps = 50
gravity = 0.15  # для движения по y

clock = pygame.time.Clock()
WIDTH, HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT))


def load_image(name, png=False, obrezanie_fon=False):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        quit()
    image = pygame.image.load(fullname)
    if obrezanie_fon:  # убрать фон
        del_color = image.get_at((0, 0))
        image.set_colorkey(del_color)
    if not png:
        image = image.convert()  # не png форматы
    else:
        image = image.convert_alpha()  # png
    return image


# для отслеживания улетевших частиц
# удобно использовать пересечение прямоугольников
screen_rect = (0, 0, WIDTH, HEIGHT)


class Particle(pygame.sprite.Sprite):
    # сгенерируем частицы разного размера
    fire = [load_image(name="star.png", png=True, obrezanie_fon=True)]
    for scale in (5, 10, 20, 25, 30, 35, 41):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(all_sprites)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()

        # у каждой частицы своя скорость - это вектор
        self.vx = dx
        self.vy = dy
        # и свои координаты
        self.rect.x, self.rect.y = pos

        # гравитация будет одинаковой
        self.gravity = gravity

    def update(self):
        # применяем гравитационный эффект:
        # движение с ускорением под действием гравитации
        self.vy += self.gravity
        # перемещаем частицу
        self.rect.x += self.vx
        self.rect.y += self.vy
        # убиваем, если частица ушла за экран
        if not self.rect.colliderect(screen_rect):
            self.kill()


def create_particles(position):
    # количество создаваемых частиц
    particle_count = 50
    # возможные скорости
    numbers = range(-8, 11)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers))


all_sprites = pygame.sprite.Group()
pygame.mouse.set_visible(0)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
            running = False
        if event.type == pygame.MOUSEMOTION:
            # создаем частицы по движению мыши
            create_particles(event.pos)

    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    all_sprites.update()
    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
