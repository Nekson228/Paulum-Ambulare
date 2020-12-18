import pygame

SPEED = 10  # константа скорости персонажа
JUMP_HEIGHT = 6  # константа высоты прыжка персонажа
ASSETS = {  # используемые ассеты
    'character': 'resources/character.png',
    'obstacle': 'resources/obstacle.png'
}


class Character(pygame.sprite.Sprite):
    image = pygame.image.load(ASSETS['character'])

    def __init__(self, group, x, y):
        super().__init__(group)
        self.image = Character.image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

        self.jump = False
        self.jump_delta = JUMP_HEIGHT

    def move(self, x, y):
        self.rect.x += x
        self.rect.y += y
        collided_sprite = pygame.sprite.spritecollideany(self, obstacles)
        if collided_sprite:
            if x > 0:
                self.rect.x = collided_sprite.rect.x - self.rect.w
            elif x < 0:
                self.rect.x = collided_sprite.rect.x + collided_sprite.rect.w
            if y > 0:
                self.rect.y = collided_sprite.rect.y - self.rect.h
            elif y < 0:
                self.rect.y = collided_sprite.rect.y + collided_sprite.rect.h


class Obstacle(pygame.sprite.Sprite):
    image = pygame.image.load(ASSETS['obstacle'])

    def __init__(self, group, x, y, w, h):
        super().__init__(group)
        self.image = Obstacle.image
        self.image = pygame.transform.scale(self.image, (w, h))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y


if __name__ == '__main__':
    # Инициализация #
    pygame.init()
    pygame.display.set_caption('Untitled Nekit Game')
    size = width, height = 640, 640
    screen = pygame.display.set_mode(size)
    pygame.mouse.set_visible(False)

    # Спрайты #
    all_sprites = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()
    character = Character(all_sprites, width // 2, height // 2)

    obs1 = Obstacle(obstacles, 200, 50, 50, 100)
    obs2 = Obstacle(obstacles, 250, 50, 100, 50)
    obs3 = Obstacle(obstacles, 350, 50, 100, 50)
    obs4 = Obstacle(obstacles, 450, 50, 50, 100)
    obs5 = Obstacle(obstacles, 450, 100, 50, 250)
    obs6 = Obstacle(obstacles, 200, 100, 50, 250)

    clock = pygame.time.Clock()
    fps = 30  # частота обновления экрана (кадров в секунду)

    # Основной цикл #
    run = True
    while run:
        clock.tick(fps)
        # Проверка событий #
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Передвижение персонажа #
        keys = pygame.key.get_pressed()
        if not character.jump:
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                character.move(0, -SPEED)
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                character.move(0, SPEED)
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            character.move(-SPEED, 0)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            character.move(SPEED, 0)
        if keys[pygame.K_SPACE]:
            character.jump = True

        if character.jump:
            if character.jump_delta >= -JUMP_HEIGHT:
                character.move(0, -character.jump_delta ** 2 * (1 if character.jump_delta > 0 else -1))
                character.jump_delta -= 1
            else:
                character.jump = False
                character.jump_delta = JUMP_HEIGHT
        # Обновление экрана #
        screen.fill(pygame.Color('black'))
        all_sprites.draw(screen)
        obstacles.draw(screen)
        obstacles.update()
        pygame.display.flip()
    pygame.quit()
