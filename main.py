import pygame
import sys
import os

SPEED = 10  # константа скорости персонажа
JUMP_HEIGHT = 6  # константа высоты прыжка персонажа
ASSETS = {  # используемые ассеты
    'character': 'character.png',
    'tile': 'tile.png',
    'obstacle': 'obstacle.png'
}


def load_image(name, colorkey=None):
    fullname = os.path.join('resources', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def load_level(filename):  # обработка файла для реализации сборки уровня
    filename = "resources/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):  # генерация уровня из обработанного текстового файла
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('tile', x, y)
            elif level[y][x] == '#':
                Tile('obstacle', x, y)
            elif level[y][x] == '@':
                Tile('tile', x, y)
                new_player = Character(x, y)
    return new_player, x, y


class Character(pygame.sprite.Sprite):
    image = load_image(ASSETS['character'])

    def __init__(self, x, y):
        super().__init__(player_group, all_sprites)
        self.image = Character.image
        self.rect = self.image.get_rect().move(tile_width * x, tile_height * y)

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


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, x, y):
        if tile_type == 'obstacle':
            super().__init__(obstacles, all_sprites)
        else:
            super().__init__(tiles_group, all_sprites)
        image = load_image(ASSETS[tile_type])
        self.image = image
        self.image = pygame.transform.scale(self.image, (tile_width, tile_height))
        self.rect = self.image.get_rect().move(tile_width * x, tile_height * y)


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
    player_group = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()

    tile_width = tile_height = 30  # задаем размеры(можно любой, этот для теста)

    character, level_x, level_y = generate_level(load_level('test_map.txt'))

    clock = pygame.time.Clock()
    fps = 30  # частота обновления экрана (кадров в секунду)

    camera = Camera()  # объект камеры

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
        tiles_group.draw(screen)
        obstacles.draw(screen)
        player_group.draw(screen)
        pygame.display.flip()
    pygame.quit()
