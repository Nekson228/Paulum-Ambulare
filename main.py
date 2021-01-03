import pygame
import sys
import os
import pytmx

# Игровые константы #
SPEED = 15  # скорость персонажа
JUMP_HEIGHT = 8  # высота прыжка персонажа
MIN_FALL_SPEED = 1  # минимальная скорость падения
MAX_FALL_SPEED = JUMP_HEIGHT  # максимальная скорость падения
FPS = 30  # частота обновления экрана (кадров в секунду)
RIGHT = 1
LEFT = -1


def load_image(name: str) -> pygame.Surface:
    fullname = os.path.join('resources', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Character(pygame.sprite.Sprite):
    # Константы персонажа #
    IDLE_ANIMATION_SPEED = 0.1
    OTHER_ANIMATION_SPEED = 0.2

    # Анимации персонажа #
    idle_animation_right = [
        load_image('character/adventurer-idle-00.png'),
        load_image('character/adventurer-idle-01.png')
    ]
    idle_animation_left = [
        pygame.transform.flip(load_image('character/adventurer-idle-00.png'), True, False),
        pygame.transform.flip(load_image('character/adventurer-idle-01.png'), True, False),
    ]
    run_animation_right = [
        load_image('character/adventurer-run-00.png'),
        load_image('character/adventurer-run-01.png'),
        load_image('character/adventurer-run-02.png'),
        load_image('character/adventurer-run-03.png'),
        load_image('character/adventurer-run-04.png'),
        load_image('character/adventurer-run-05.png'),
    ]
    run_animation_left = [
        pygame.transform.flip(load_image('character/adventurer-run-00.png'), True, False),
        pygame.transform.flip(load_image('character/adventurer-run-01.png'), True, False),
        pygame.transform.flip(load_image('character/adventurer-run-02.png'), True, False),
        pygame.transform.flip(load_image('character/adventurer-run-03.png'), True, False),
        pygame.transform.flip(load_image('character/adventurer-run-04.png'), True, False),
        pygame.transform.flip(load_image('character/adventurer-run-05.png'), True, False),
    ]
    jump_right = [
        load_image('character/adventurer-jump-02.png')
    ]
    jump_left = [
        pygame.transform.flip(load_image('character/adventurer-jump-02.png'), True, False)
    ]
    fall_right = [
        load_image('character/adventurer-jump-03.png')
    ]
    fall_left = [
        pygame.transform.flip(load_image('character/adventurer-jump-03.png'), True, False)
    ]
    attack_animations_right = [
        [
            load_image('character/adventurer-attack1-00.png'),
            load_image('character/adventurer-attack1-01.png'),
            load_image('character/adventurer-attack1-02.png'),
            load_image('character/adventurer-attack1-03.png'),
            load_image('character/adventurer-attack1-04.png'),
        ],
        [
            load_image('character/adventurer-attack2-00.png'),
            load_image('character/adventurer-attack2-01.png'),
            load_image('character/adventurer-attack2-02.png'),
            load_image('character/adventurer-attack2-03.png'),
            load_image('character/adventurer-attack2-04.png'),
            load_image('character/adventurer-attack2-05.png'),
        ],
        [
            load_image('character/adventurer-attack3-00.png'),
            load_image('character/adventurer-attack3-01.png'),
            load_image('character/adventurer-attack3-02.png'),
            load_image('character/adventurer-attack3-03.png'),
            load_image('character/adventurer-attack3-04.png'),
            load_image('character/adventurer-attack3-05.png'),
        ]
    ]
    attack_animations_left = [
        [
            pygame.transform.flip(load_image('character/adventurer-attack1-00.png'), True, False),
            pygame.transform.flip(load_image('character/adventurer-attack1-01.png'), True, False),
            pygame.transform.flip(load_image('character/adventurer-attack1-02.png'), True, False),
            pygame.transform.flip(load_image('character/adventurer-attack1-03.png'), True, False),
            pygame.transform.flip(load_image('character/adventurer-attack1-04.png'), True, False),
        ],
        [
            pygame.transform.flip(load_image('character/adventurer-attack2-00.png'), True, False),
            pygame.transform.flip(load_image('character/adventurer-attack2-01.png'), True, False),
            pygame.transform.flip(load_image('character/adventurer-attack2-02.png'), True, False),
            pygame.transform.flip(load_image('character/adventurer-attack2-03.png'), True, False),
            pygame.transform.flip(load_image('character/adventurer-attack2-04.png'), True, False),
            pygame.transform.flip(load_image('character/adventurer-attack2-05.png'), True, False),
        ],
        [
            pygame.transform.flip(load_image('character/adventurer-attack3-00.png'), True, False),
            pygame.transform.flip(load_image('character/adventurer-attack3-01.png'), True, False),
            pygame.transform.flip(load_image('character/adventurer-attack3-02.png'), True, False),
            pygame.transform.flip(load_image('character/adventurer-attack3-03.png'), True, False),
            pygame.transform.flip(load_image('character/adventurer-attack3-04.png'), True, False),
            pygame.transform.flip(load_image('character/adventurer-attack3-05.png'), True, False),
        ],
    ]

    def __init__(self, x, y):
        super().__init__(player_group, all_sprites)

        self.current_animation = Character.idle_animation_right
        self.animation_frame = 0
        self.attack_animation_type = 0
        self.animation_speed = Character.IDLE_ANIMATION_SPEED
        self.image = self.current_animation[self.animation_frame]
        self.rect = self.image.get_rect().move(tile_width * x, tile_height * y)

        self.facing = RIGHT

        self.jump = False
        self.fall = False
        self.attack = False

    def update(self):
        self.animation_frame += self.animation_speed
        self.animation_frame = round(self.animation_frame, 1)
        if self.current_animation in Character.attack_animations_right or \
                self.current_animation in Character.attack_animations_left:
            if self.animation_frame == len(self.current_animation):
                self.current_animation = Character.idle_animation_right if self.facing == RIGHT \
                    else Character.idle_animation_left
                self.animation_frame = 0
                self.animation_speed = Character.IDLE_ANIMATION_SPEED
                self.attack = False
        self.animation_frame %= len(self.current_animation)
        self.image = self.current_animation[int(self.animation_frame)]

    def move(self, x, y):
        self.rect.x += x
        self.rect.y += y

        if x != 0:
            self.facing = RIGHT if x > 0 else LEFT
            if not (self.jump or self.fall):
                self.animation_speed = Character.OTHER_ANIMATION_SPEED
                if x > 0 and self.current_animation != Character.run_animation_right:
                    self.current_animation = Character.run_animation_right
                    self.animation_frame = 0
                elif x < 0 and self.current_animation != Character.run_animation_left:
                    self.current_animation = Character.run_animation_left
                    self.animation_frame = 0
            else:
                if self.jump:
                    self.current_animation = Character.jump_right if self.facing == RIGHT else Character.jump_left
                elif self.fall:
                    self.current_animation = Character.fall_right if self.facing == RIGHT else Character.fall_left

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
                if self.fall:
                    self.current_animation = Character.idle_animation_right \
                        if self.facing == RIGHT else Character.idle_animation_left
                    self.animation_speed = Character.IDLE_ANIMATION_SPEED
                self.fall = False
        else:
            self.fall = True
            self.current_animation = Character.fall_right if self.facing == RIGHT else Character.fall_left

    def set_jump(self, state):
        if state is True:
            self.rect.y -= 1
            collided_sprite = pygame.sprite.spritecollideany(self, obstacles)
            self.rect.y += 1
            if collided_sprite:
                self.jump = False
            else:
                self.jump = True
                self.current_animation = Character.jump_right if self.facing == RIGHT else Character.jump_left
                self.animation_frame = 0
        else:
            self.jump = False

    def set_standing(self):
        if self.current_animation in (Character.run_animation_right, Character.run_animation_left):
            self.current_animation = Character.idle_animation_right if self.facing == RIGHT \
                else Character.idle_animation_left
            self.animation_frame = 0
            self.animation_speed = Character.IDLE_ANIMATION_SPEED

    def set_attack(self):
        if not self.attack and not self.jump and not self.fall:
            self.attack = True
            self.current_animation = Character.attack_animations_right[self.attack_animation_type] \
                if self.facing == RIGHT \
                else Character.attack_animations_left[self.attack_animation_type]
            self.animation_frame = 0
            self.attack_animation_type += 1
            if self.attack_animation_type == len(Character.attack_animations_right):
                self.attack_animation_type = 0
            self.animation_speed = Character.OTHER_ANIMATION_SPEED


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
        character.update()

        pygame.display.flip()


if __name__ == '__main__':
    # Инициализация #
    pygame.init()
    pygame.display.set_caption('Untitled Nekit Game')
    size = width, height = 1280, 640
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
    tile_size = tile_width, tile_height = game_map.get_tile_size()  # размеры тайлов
    game_map.render()

    character = Character(0, 0)
    character.check_standing()

    # Основной цикл #
    while True:
        # Проверка событий #
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                character.set_attack()

        # Передвижение персонажа #
        keys = pygame.key.get_pressed()
        if not character.attack:
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                character.move(-SPEED, 0)
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                character.move(SPEED, 0)
            if not (keys[pygame.K_LEFT] or keys[pygame.K_a]) and not (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
                character.set_standing()
            if keys[pygame.K_SPACE] and not character.fall and not character.jump:
                character.set_jump(True)

        if character.jump:
            if jump_delta >= -JUMP_HEIGHT:
                if jump_delta > 0:
                    character.move(0, -jump_delta ** 2)
                    jump_delta -= 1
                else:
                    character.check_standing()
                    character.set_jump(False)
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
