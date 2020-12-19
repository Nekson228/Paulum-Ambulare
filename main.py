import pygame

SPEED = 10  # константа скорости персонажа
JUMP_HEIGHT = 6  # константа высоты прыжка персонажа
ASSETS = {  # используемые ассеты
    'character': 'resources/character.png',
    'obstacle': 'resources/obstacle.png'
}


class Character(pygame.sprite.Sprite):
    image = pygame.image.load(ASSETS['character'])

    def __init__(self, x, y):
        super().__init__(all_sprites)
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

    def __init__(self, x, y, w, h):
        super().__init__(all_sprites)
        self.image = Obstacle.image
        self.image = pygame.transform.scale(self.image, (w, h))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


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
    character = Character(width // 2, height // 2)

    obs1 = Obstacle(200, 50, 50, 100)
    obs2 = Obstacle(250, 50, 100, 50)
    obs3 = Obstacle(350, 50, 100, 50)
    obs4 = Obstacle(450, 50, 50, 100)
    obs5 = Obstacle(450, 100, 50, 250)
    obs6 = Obstacle(200, 100, 50, 250)

    clock = pygame.time.Clock()
    fps = 30  # частота обновления экрана (кадров в секунду)

    camera = Camera() # объект камеры

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
        screen.fill('black')
        camera.update(character)
        # обновляем положение спрайтов
        for sprite in all_sprites:
            camera.apply(sprite)
        all_sprites.draw(screen)
        obstacles.draw(screen)
        obstacles.update()
        pygame.display.flip()
    pygame.quit()
