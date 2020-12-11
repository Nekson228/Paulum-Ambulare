import pygame

SPEED = 10  # константа скорости персонажа


class Character(pygame.sprite.Sprite):
    image = pygame.image.load('resources/character.png')

    def __init__(self, group):
        super().__init__(group)
        self.image = Character.image
        self.rect = self.image.get_rect()

    def move(self, x, y):
        self.rect.x += x
        self.rect.y += y


if __name__ == '__main__':
    # Инициализация #
    pygame.init()
    pygame.display.set_caption('Untitled Nekit Game')
    size = width, height = 1280, 640
    screen = pygame.display.set_mode(size)
    pygame.mouse.set_visible(False)

    # Спрайты #
    all_sprites = pygame.sprite.Group()
    character = Character(all_sprites)

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
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            character.move(0, -SPEED)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            character.move(0, SPEED)
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            character.move(-SPEED, 0)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            character.move(SPEED, 0)

        # Обновление экрана #
        screen.fill(pygame.Color('black'))
        all_sprites.draw(screen)
        pygame.display.flip()
    pygame.quit()