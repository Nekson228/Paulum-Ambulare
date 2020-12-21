import pygame
import sys
import os

SPEED = 10  # константа скорости персонажа
JUMP_HEIGHT = 7  # константа высоты прыжка персонажа
MIN_FALL_SPEED = 1
MAX_FALL_SPEED = JUMP_HEIGHT
ASSETS = {  # используемые ассеты
    'character': 'character.png',
    'tile': 'tile.png',
    'obstacle': 'obstacle.png'
}


def load_image(name):
    fullname = os.path.join('resources', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def load_level(filename):  # обработка файла для реализации сборки уровня
    filename = "levels/" + filename
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
        self.fall = False

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
        if not self.jump:
            self.check_standing()

    def check_standing(self):
        self.rect.h += 1
        collided_sprite = pygame.sprite.spritecollideany(self, obstacles)
        self.rect.h -= 1
        self_bottom = range(self.rect.bottomleft[0], self.rect.bottomright[0])
        if collided_sprite and (collided_sprite.rect.right in self_bottom or collided_sprite.rect.left in self_bottom):
            self.fall = False
        else:
            self.fall = True

    def check_jump_ability(self):
        self.rect.y -= 1
        collided_sprite = pygame.sprite.spritecollideany(self, obstacles)
        self.rect.y += 1
        if collided_sprite:
            return False
        return True


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
    character.check_standing()

    clock = pygame.time.Clock()
    fps = 30  # частота обновления экрана (кадров в секунду)

    camera = Camera()  # объект камеры

    # Игровые переменные #
    jump_delta = JUMP_HEIGHT
    fall_delta = MIN_FALL_SPEED

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
        if keys[pygame.K_SPACE] and not character.fall and not character.jump:
            character.jump = character.check_jump_ability()

        if character.jump:
            if jump_delta >= -JUMP_HEIGHT:
                if jump_delta > 0:
                    character.move(0, -jump_delta ** 2)
                    jump_delta -= 1
                else:
                    character.check_standing()
                    character.jump = False
                    jump_delta = JUMP_HEIGHT
                    character.check_standing()

        if character.fall and not character.jump:
            if fall_delta < MAX_FALL_SPEED:
                character.move(0, fall_delta ** 2)
                fall_delta += 1
            else:
                character.move(0, MAX_FALL_SPEED ** 2)
        elif not character.fall:
            fall_delta = MIN_FALL_SPEED

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
