import pygame
import sys
import os
import pytmx

# Игровые константы #
SPEED = 10  # скорость персонажа
JUMP_HEIGHT = 8  # высота прыжка персонажа
MIN_FALL_SPEED = 1  # минимальная скорость падения
MAX_FALL_SPEED = JUMP_HEIGHT  # максимальная скорость падения
ASSETS = {  # используемые ассеты
    'character': 'character.png',
    'tile': 'tile.png',
    'obstacle': 'obstacle.png'
}
FPS = 30  # частота обновления экрана (кадров в секунду)


def load_image(name):
    fullname = os.path.join('resources', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Character(pygame.sprite.Sprite):
    image = load_image(ASSETS['character'])

    def __init__(self, x, y):
        super().__init__(player_group, all_sprites)
        self.image = Character.image
        self.rect = self.image.get_rect().move(32 * x, 32 * y)

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
        if collided_sprite:
            collided_top = range(collided_sprite.rect.topleft[0], collided_sprite.rect.topright[0])
            if self.rect.left in collided_top or self.rect.right in collided_top:
                self.fall = False
        else:
            self.fall = True

    def set_jump(self):
        self.rect.y -= 1
        collided_sprite = pygame.sprite.spritecollideany(self, obstacles)
        self.rect.y += 1
        if collided_sprite:
            self.jump = False
        else:
            self.jump = True


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_img, x, y, block=False, half_block=False):
        super().__init__(all_sprites)
        if block or half_block:
            self.add(obstacles)
        self.image = tile_img
        self.image = pygame.transform.scale(self.image, (tile_width, tile_height))
        self.rect = self.image.get_rect().move(x, y)


class TiledMap:
    def __init__(self, tmx_map):
        tmx_map = "main_maps/" + tmx_map
        self.level_map = pytmx.load_pygame(tmx_map, pixelalpha=True)

    def get_tile_size(self):
        return self.level_map.tilewidth, self.level_map.tileheight

    def render(self):
        for x, y, gid in self.level_map.layernames['Background']:
            tile = self.level_map.get_tile_image_by_gid(gid)
            if tile:
                Tile(tile, x * tile_width, y * tile_height)
        for tile_object in self.level_map.layernames['Objects']:
            if tile_object.type == 'Block':
                Tile(tile_object.image, tile_object.x, tile_object.y, block=True)
            elif tile_object.type == 'Half-Block':
                Tile(tile_object.image, tile_object.x, tile_object.y, half_block=True)
        for x, y, gid in self.level_map.layernames['Water']:
            tile = self.level_map.get_tile_image_by_gid(gid)
            if tile:
                Tile(tile, x * tile_width, y * tile_height)


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


def terminate():
    pygame.quit()
    sys.exit()


class Display:
    def __init__(self, screen_size):
        self.screen = pygame.display.set_mode(screen_size)
        self.clock = pygame.time.Clock()  # объект игровых часов
        self.camera = Camera()  # объект игровой камеры

    def update(self):
        self.clock.tick(FPS)
        self.screen.fill('black')
        self.camera.update(character)

        for sprite in all_sprites:
            self.camera.apply(sprite)
        all_sprites.draw(self.screen)

        pygame.display.flip()


if __name__ == '__main__':
    # Инициализация #
    pygame.init()
    pygame.display.set_caption('Untitled Nekit Game')
    size = width, height = 640, 640
    display = Display(size)
    pygame.mouse.set_visible(False)

    # Спрайты #
    all_sprites = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()

    # Игровые переменные #
    jump_delta = JUMP_HEIGHT
    fall_delta = MIN_FALL_SPEED

    game_map = TiledMap('level_ex.tmx')  # карта уровня
    tile_size = tile_width, tile_height = game_map.get_tile_size()
    game_map.render()

    character = Character(0, 19)
    character.check_standing()

    # Основной цикл #
    while True:
        # Проверка событий #
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

        # Передвижение персонажа #
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            character.move(-SPEED, 0)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            character.move(SPEED, 0)
        # if keys[pygame.K_UP] or keys[pygame.K_a]:
        #     character.move(0, -SPEED)
        # if keys[pygame.K_DOWN] or keys[pygame.K_d]:
        #     character.move(0, SPEED)
        if keys[pygame.K_SPACE] and not character.fall and not character.jump:
            character.set_jump()

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
        display.update()
# привет
