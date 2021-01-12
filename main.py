import pygame
import sys
import os
import pytmx

# Игровые константы #
SPEED = 10  # скорость персонажа
FPS = 30  # частота обновления экрана (кадров в секунду)
RIGHT = 1
LEFT = -1
MUSIC_VOLUME = 0.1
SFX_VOLUME = 0.2
TEST_MODE = False

player_x = 0
player_y = 0  # нужно для объявления игрока

pygame.init()


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name: str) -> pygame.Surface:
    fullname = os.path.join('resources', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def play():
    pygame.mixer.music.play(loops=-1, fade_ms=2000)


def pause():
    pygame.mixer.music.pause()


def unpause():
    pygame.mixer.music.unpause()


def text_format(message, font_filename, size, color):
    new_font = pygame.font.Font(f'resources/{font_filename}', size)
    new_text = new_font.render(message, True, color)

    return new_text


class Music:
    tracks = ['resources/music/Intro Theme.mp3',
              'resources/music/Grasslands Theme.mp3',
              'resources/music/Game Over.mp3']

    def __init__(self, volume: float):
        self.current_track = 0
        pygame.mixer.music.load(Music.tracks[self.current_track])
        pygame.mixer.music.set_volume(volume)

    def switch(self, n):
        self.current_track = n
        pygame.mixer.music.load(Music.tracks[self.current_track])
        play()


class Character(pygame.sprite.Sprite):
    # Константы персонажа #
    IDLE_ANIMATION_SPEED = 0.1
    ATTACK_ANIMATION_SPEED = 0.4
    OTHER_ANIMATION_SPEED = 0.2

    JUMP_HEIGHT = 8  # высота прыжка персонажа
    MIN_FALL_SPEED = 1  # минимальная скорость падения
    MAX_FALL_SPEED = JUMP_HEIGHT - 1  # максимальная скорость падения

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
    fall_animation_right = [
        load_image('character/adventurer-fall-00.png'),
        load_image('character/adventurer-fall-01.png'),
    ]
    fall_animation_left = [
        pygame.transform.flip(load_image('character/adventurer-fall-00.png'), True, False),
        pygame.transform.flip(load_image('character/adventurer-fall-01.png'), True, False)
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
    die_animation_right = [
        load_image('character/adventurer-die-00.png'),
        load_image('character/adventurer-die-01.png'),
        load_image('character/adventurer-die-02.png'),
        load_image('character/adventurer-die-03.png'),
        load_image('character/adventurer-die-04.png'),
        load_image('character/adventurer-die-05.png'),
        load_image('character/adventurer-die-06.png'),
    ]
    die_animation_left = [
        pygame.transform.flip(load_image('character/adventurer-die-00.png'), True, False),
        pygame.transform.flip(load_image('character/adventurer-die-01.png'), True, False),
        pygame.transform.flip(load_image('character/adventurer-die-02.png'), True, False),
        pygame.transform.flip(load_image('character/adventurer-die-03.png'), True, False),
        pygame.transform.flip(load_image('character/adventurer-die-04.png'), True, False),
        pygame.transform.flip(load_image('character/adventurer-die-05.png'), True, False),
        pygame.transform.flip(load_image('character/adventurer-die-06.png'), True, False),
    ]
    jump_sound = pygame.mixer.Sound('resources/sounds/jump.wav')
    death_sound = pygame.mixer.Sound('resources/sounds/hurt.wav')

    jump_sound.set_volume(SFX_VOLUME)
    death_sound.set_volume(SFX_VOLUME)

    def __init__(self, x, y):
        super().__init__(player_group, all_sprites)

        self.current_animation = Character.idle_animation_right
        self.animation_frame = 0
        self.attack_animation_type = 0
        self.animation_speed = Character.IDLE_ANIMATION_SPEED
        self.image = self.current_animation[self.animation_frame]
        self.rect = self.image.get_rect().move(x, y)

        self.facing = RIGHT
        self.jump_delta = Character.JUMP_HEIGHT
        self.fall_delta = Character.MIN_FALL_SPEED

        self.jump = False
        self.fall = False
        self.attack = False
        self.death = False

    def move(self, x, y):
        self.rect.x += x
        self.rect.y += y

        if x != 0:
            self.facing = RIGHT if x > 0 else LEFT
            if not (self.jump or self.fall):
                if self.facing == RIGHT and self.current_animation != Character.run_animation_right:
                    self.set_animation(Character.run_animation_right)
                elif self.facing == LEFT and self.current_animation != Character.run_animation_left:
                    self.set_animation(Character.run_animation_left)
            else:
                if self.jump:
                    self.set_animation(Character.jump_right if self.facing == RIGHT else Character.jump_left)
                elif self.fall:
                    self.set_animation(Character.fall_animation_right if self.facing == RIGHT
                                       else Character.fall_animation_left)

        collided_sprite = pygame.sprite.spritecollideany(self, obstacles_group)
        if collided_sprite:
            if x > 0:
                self.rect.x = collided_sprite.rect.x - self.rect.w
            elif x < 0:
                self.rect.x = collided_sprite.rect.x + collided_sprite.rect.w
            if y > 0:
                self.rect.y = collided_sprite.rect.y - self.rect.h
            elif y < 0:
                self.rect.y = collided_sprite.rect.y + collided_sprite.rect.h
        if TEST_MODE is False:
            if not self.jump:
                self.check_standing()
        self.check_enemy_collision()
        self.check_out_of_bounds()
        self.check_finish()

    def check_finish(self):
        collided_object = pygame.sprite.spritecollideany(self, game_objects)
        if collided_object and isinstance(collided_object, Finish):
            print('finish')

    def check_enemy_collision(self):
        if not TEST_MODE:
            collided_enemy = pygame.sprite.spritecollideany(self, mobs_group)
            if collided_enemy:
                if not self.death:
                    self.set_death()

    def check_out_of_bounds(self):
        if self.rect.y >= display.screen_rect.y + display.screen_rect.h:
            if not self.death:
                self.set_death()

    def check_standing(self):
        self.rect.h += 1
        collided_sprite = pygame.sprite.spritecollideany(self, obstacles_group)
        self.rect.h -= 1
        if collided_sprite:
            collided_top = range(collided_sprite.rect.topleft[0], collided_sprite.rect.topright[0])
            if self.rect.left in collided_top or self.rect.right in collided_top:
                if self.fall:
                    self.set_animation(Character.idle_animation_right if self.facing == RIGHT
                                       else Character.idle_animation_left)
                self.fall = False
        else:
            self.fall = True
            self.set_animation(Character.fall_animation_right if self.facing == RIGHT
                               else Character.fall_animation_left)

    def set_animation(self, animation):
        if not self.death:
            self.current_animation = animation
            self.animation_frame = 0
            if animation in Character.attack_animations_right or animation in Character.attack_animations_left:
                self.animation_speed = Character.ATTACK_ANIMATION_SPEED
            elif animation in (Character.idle_animation_right, Character.idle_animation_left):
                self.animation_speed = Character.IDLE_ANIMATION_SPEED
            else:
                self.animation_speed = Character.OTHER_ANIMATION_SPEED

    def set_jump(self, state):
        if state is True:
            self.rect.y -= 1
            collided_sprite = pygame.sprite.spritecollideany(self, obstacles_group)
            self.rect.y += 1
            if collided_sprite:
                self.jump = False
            else:
                Character.jump_sound.play()
                self.jump = True
                self.set_animation(Character.jump_right if self.facing == RIGHT else Character.jump_left)
        else:
            self.jump = False

    def set_standing(self):
        if self.current_animation in (Character.run_animation_right, Character.run_animation_left):
            self.set_animation(Character.idle_animation_right if self.facing == RIGHT
                               else Character.idle_animation_left)

    def set_attack(self):
        if not self.attack and not self.jump and not self.fall:
            self.set_animation(Character.attack_animations_right[self.attack_animation_type] if self.facing == RIGHT
                               else Character.attack_animations_left[self.attack_animation_type])
            self.attack = True
            self.attack_animation_type += 1
            if self.attack_animation_type == len(Character.attack_animations_right):
                self.attack_animation_type = 0

    def set_death(self):
        self.set_animation(Character.die_animation_right if self.facing == RIGHT else Character.die_animation_left)
        self.death = True
        Character.death_sound.play()
        pygame.mixer.music.fadeout(3000)

    def update(self):
        if self.jump:
            if self.jump_delta >= -Character.JUMP_HEIGHT:
                if self.jump_delta > 0:
                    self.move(0, -self.jump_delta ** 2)
                    self.jump_delta -= 1
                else:
                    self.check_standing()
                    self.set_jump(False)
                    self.jump_delta = Character.JUMP_HEIGHT

        if self.fall and not self.jump:
            if self.fall_delta < Character.MAX_FALL_SPEED:
                self.move(0, self.fall_delta ** 2)
                self.fall_delta += 1
            else:
                self.move(0, Character.MAX_FALL_SPEED ** 2)
        elif not self.fall:
            self.fall_delta = Character.MIN_FALL_SPEED
        if not self.death:
            self.check_enemy_collision()

        self.animation_frame += self.animation_speed
        self.animation_frame = round(self.animation_frame, 1)
        if self.current_animation in Character.attack_animations_right or \
                self.current_animation in Character.attack_animations_left:
            if self.animation_frame >= len(self.current_animation):
                self.set_animation(Character.idle_animation_right if self.facing == RIGHT
                                   else Character.idle_animation_left)
                self.attack = False
        elif self.current_animation in (Character.die_animation_right, Character.die_animation_left):
            if self.animation_frame >= len(self.current_animation):
                game_over()
                reset_level()
        self.animation_frame %= len(self.current_animation)
        self.image = self.current_animation[int(self.animation_frame)]


class Enemy(pygame.sprite.Sprite):
    # Константы персонажа #
    IDLE_ANIMATION_SPEED = 0.1
    ATTACK_ANIMATION_SPEED = 0.4
    OTHER_ANIMATION_SPEED = 0.2

    JUMP_HEIGHT = 8  # высота прыжка персонажа
    MIN_FALL_SPEED = 1  # минимальная скорость падения
    MAX_FALL_SPEED = JUMP_HEIGHT - 1  # максимальная скорость падения

    # Анимации персонажа #
    idle_animation_right = [
        load_image('enemy/idle_1.png'),
        load_image('enemy/idle_2.png')
    ]
    idle_animation_left = [
        pygame.transform.flip(load_image('enemy/idle_1.png'), True, False),
        pygame.transform.flip(load_image('enemy/idle_2.png'), True, False)
    ]
    run_animation_right = [
        load_image('enemy/run_1.png'),
        load_image('enemy/run_2.png'),
        load_image('enemy/run_3.png'),
        load_image('enemy/run_4.png'),
        load_image('enemy/run_5.png'),
        load_image('enemy/run_6.png'),
        load_image('enemy/run_7.png'),
        load_image('enemy/run_8.png')
    ]
    run_animation_left = [
        pygame.transform.flip(load_image('enemy/run_1.png'), True, False),
        pygame.transform.flip(load_image('enemy/run_2.png'), True, False),
        pygame.transform.flip(load_image('enemy/run_3.png'), True, False),
        pygame.transform.flip(load_image('enemy/run_4.png'), True, False),
        pygame.transform.flip(load_image('enemy/run_5.png'), True, False),
        pygame.transform.flip(load_image('enemy/run_6.png'), True, False),
        pygame.transform.flip(load_image('enemy/run_7.png'), True, False),
        pygame.transform.flip(load_image('enemy/run_8.png'), True, False)
    ]
    taking_hit_animations_right = [
        load_image('enemy/hit_1.png'),
        load_image('enemy/hit_2.png'),
        load_image('enemy/hit_3.png'),
        load_image('enemy/hit_4.png')
    ]
    taking_hit_animations_left = [
        pygame.transform.flip(load_image('enemy/hit_1.png'), True, False),
        pygame.transform.flip(load_image('enemy/hit_2.png'), True, False),
        pygame.transform.flip(load_image('enemy/hit_3.png'), True, False),
        pygame.transform.flip(load_image('enemy/hit_4.png'), True, False)
    ]
    death_animations_right = [
        load_image('enemy/death_1.png'),
        load_image('enemy/death_2.png'),
        load_image('enemy/death_3.png'),
        load_image('enemy/death_4.png')
    ]
    death_animations_left = [
        pygame.transform.flip(load_image('enemy/death_1.png'), True, False),
        pygame.transform.flip(load_image('enemy/death_2.png'), True, False),
        pygame.transform.flip(load_image('enemy/death_3.png'), True, False),
        pygame.transform.flip(load_image('enemy/death_4.png'), True, False)
    ]
    attack_animations_right = [
        load_image('enemy/attack_1.png'),
        load_image('enemy/attack_2.png'),
        load_image('enemy/attack_3.png'),
        load_image('enemy/attack_4.png'),
        load_image('enemy/attack_5.png'),
        load_image('enemy/attack_6.png'),
        load_image('enemy/attack_7.png'),
        load_image('enemy/attack_8.png')]
    attack_animations_left = [
        pygame.transform.flip(load_image('enemy/attack_1.png'), True, False),
        pygame.transform.flip(load_image('enemy/attack_2.png'), True, False),
        pygame.transform.flip(load_image('enemy/attack_3.png'), True, False),
        pygame.transform.flip(load_image('enemy/attack_4.png'), True, False),
        pygame.transform.flip(load_image('enemy/attack_5.png'), True, False),
        pygame.transform.flip(load_image('enemy/attack_6.png'), True, False),
        pygame.transform.flip(load_image('enemy/attack_7.png'), True, False),
        pygame.transform.flip(load_image('enemy/attack_8.png'), True, False)
    ]

    def __init__(self, x, y):
        super().__init__(mobs_group, all_sprites)

        self.current_animation = Enemy.idle_animation_right
        self.animation_frame = 0
        self.attack_animation_type = 0
        self.animation_speed = Enemy.IDLE_ANIMATION_SPEED
        self.image = self.current_animation[self.animation_frame]
        self.rect = self.image.get_rect().move(x, y)

        self.facing = RIGHT
        self.jump_delta = Enemy.JUMP_HEIGHT
        self.fall_delta = Enemy.MIN_FALL_SPEED

        self.fall = False
        self.attack = False

    def move(self, x):
        self.rect.x += x * self.facing

        if x != 0:
            if self.facing == RIGHT and self.current_animation != Enemy.run_animation_right:
                self.set_animation(Enemy.run_animation_right)
            elif self.facing == LEFT and self.current_animation != Enemy.run_animation_left:
                self.set_animation(Enemy.run_animation_left)

        collided_block = pygame.sprite.spritecollideany(self, non_visible_things)
        collided_sprite = pygame.sprite.spritecollideany(self, obstacles_group)
        if collided_sprite or collided_block:
            self.facing *= -1

    def set_animation(self, animation):
        self.current_animation = animation
        self.animation_frame = 0
        if animation in Enemy.attack_animations_right or animation in Enemy.attack_animations_left:
            self.animation_speed = Enemy.ATTACK_ANIMATION_SPEED
        elif animation in (Enemy.idle_animation_right, Enemy.idle_animation_left):
            self.animation_speed = Enemy.IDLE_ANIMATION_SPEED
        else:
            self.animation_speed = Enemy.OTHER_ANIMATION_SPEED

    def set_attack(self):
        if not self.attack and not self.fall:
            self.set_animation(Enemy.attack_animations_right[self.attack_animation_type] if self.facing == RIGHT
                               else Enemy.attack_animations_left[self.attack_animation_type])
            self.attack = True
            self.attack_animation_type += 1
            if self.attack_animation_type == len(Enemy.attack_animations_right):
                self.attack_animation_type = 0

    def update(self):
        self.move(SPEED // 5)
        self.animation_frame += self.animation_speed
        self.animation_frame = round(self.animation_frame, 1)
        if self.current_animation in Enemy.attack_animations_right or \
                self.current_animation in Enemy.attack_animations_left:
            if self.animation_frame >= len(self.current_animation):
                self.set_animation(Enemy.idle_animation_right if self.facing == RIGHT
                                   else Enemy.idle_animation_left)
                self.attack = False
        self.animation_frame %= len(self.current_animation)
        self.image = self.current_animation[int(self.animation_frame)]


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_img, x, y, block=False):
        super().__init__(all_sprites)
        if block:
            self.add(obstacles_group)
        self.image = tile_img
        self.image = pygame.transform.scale(self.image, (tile_width, tile_height))
        self.rect = self.image.get_rect().move(x, y)


class Deco(pygame.sprite.Sprite):
    def __init__(self, img, x, y, w, h):
        super().__init__(non_visible_things)
        self.image = img
        self.image = pygame.transform.scale(self.image, (w, h))
        self.rect = self.image.get_rect().move(x, y)


class Finish(pygame.sprite.Sprite):
    def __init__(self, img, x, y, w, h):
        super().__init__(game_objects, all_sprites)
        self.image = img
        self.image = pygame.transform.scale(self.image, (w, h))
        self.rect = self.image.get_rect().move(x, y)


def reset_level():
    global character
    for group in all_groups:
        group.empty()
    character = game_map.render()
    display.reset()


class TiledMap:
    def __init__(self, tmx_map):
        tmx_map = "main_maps/" + tmx_map
        self.level_map = pytmx.load_pygame(tmx_map, pixelalpha=True)

    def get_tile_size(self):
        return self.level_map.tilewidth, self.level_map.tileheight

    def get_level_size(self):
        return self.level_map.width, self.level_map.height

    def render(self):
        char = None
        for x, y, gid in self.level_map.layernames['Background']:
            tile = self.level_map.get_tile_image_by_gid(gid)
            if tile:
                Tile(tile, x * tile_width, y * tile_height)
        for tile_object in self.level_map.layernames['Objects']:
            if tile_object.type == 'Block':
                Tile(tile_object.image, tile_object.x, tile_object.y, block=True)
        for entity in self.level_map.layernames['Mobs']:
            Enemy(entity.x, entity.y)
        for entity in self.level_map.layernames['Character']:
            char = Character(entity.x, entity.y)
        for block in self.level_map.layernames['Collisions']:
            if block.type == 'Collide':
                Deco(block.image, block.x, block.y, int(block.width), int(block.height))
        for flag in self.level_map.layernames['Finish']:
            Finish(flag.image, flag.x, flag.y, int(flag.width), int(flag.height))
        for x, y, gid in self.level_map.layernames['Water']:
            tile = self.level_map.get_tile_image_by_gid(gid)
            if tile:
                Tile(tile, x * tile_width, y * tile_height)
        return char


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

        self.scroll_x = True
        self.scroll_y = True

        self.top_blocked = self.bottom_blocked = self.right_blocked = self.left_blocked = False

    def reset(self):
        self.dx = 0
        self.dy = 0

        self.scroll_x = True
        self.scroll_y = True

        self.top_blocked = self.bottom_blocked = self.right_blocked = self.left_blocked = False

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        if isinstance(obj, pygame.sprite.Sprite):
            obj.rect.x += self.dx if self.scroll_x else 0
            obj.rect.y += self.dy if self.scroll_y else 0

        elif isinstance(obj, pygame.Rect):
            obj.x += self.dx if self.scroll_x else 0
            obj.y += self.dy if self.scroll_y else 0
            if obj.x + obj.w <= display_width:
                self.scroll_x = False
                self.right_blocked = True
            if obj.x >= 0:
                self.scroll_x = False
                self.left_blocked = True
            if obj.y + obj.h <= display_height:
                self.scroll_y = False
                self.bottom_blocked = True
            if obj.y >= 0:
                self.scroll_y = False
                self.top_blocked = True

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - display_width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - display_height // 2)
        if self.scroll_x is False:
            if target.rect.x >= display_width // 2 and self.left_blocked:
                self.scroll_x = True
                self.left_blocked = False
            elif target.rect.x + target.rect.w <= display_width // 2 and self.right_blocked:
                self.scroll_x = True
                self.right_blocked = False
        if self.scroll_y is False:
            if target.rect.y >= display_height // 2 and self.top_blocked:
                self.scroll_y = True
                self.top_blocked = False
            elif target.rect.y + target.rect.h <= display_height // 2 and self.bottom_blocked:
                self.scroll_y = True
                self.bottom_blocked = False


def main_menu(from_pause=False):
    menu = True
    music.switch(0)
    background = pygame.transform.scale(load_image('menu_screens/main_menu.png'), (display_width, display_height))
    selected = "start"

    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = "start"
                elif event.key == pygame.K_DOWN:
                    selected = "quit"
                if event.key == pygame.K_RETURN:
                    if selected == "start":
                        menu = False
                    if selected == "quit":
                        terminate()

        display.screen.fill('black')
        display.screen.blit(background, (0, 0))
        title = text_format("PAULUM AMBULARE", font, 40, 'black')
        if selected == "start":
            if not from_pause:
                text_start = text_format(">START<", font, 20, 'black')
            else:
                text_start = text_format(">CONTINUE<", font, 20, 'black')
        else:
            if not from_pause:
                text_start = text_format("START", font, 20, 'black')
            else:
                text_start = text_format("CONTINUE", font, 20, 'black')
        if selected == "quit":
            text_quit = text_format(">QUIT<", font, 20, 'black')
        else:
            text_quit = text_format("QUIT", font, 20, 'black')

        title_rect = title.get_rect()
        start_rect = text_start.get_rect()
        quit_rect = text_quit.get_rect()

        display.screen.blit(title, (display_width / 2 - (title_rect.width / 2), 40))
        display.screen.blit(text_start, (display_width / 2 - (start_rect.width / 2), 250))
        display.screen.blit(text_quit, (display_width / 2 - (quit_rect.width / 2) + 30, 350))
        pygame.display.flip()
        display.clock.tick(FPS)
    music.switch(1)


def pause_menu():
    pause()
    menu = True
    selected = "resume"

    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = "resume"
                elif event.key == pygame.K_DOWN:
                    selected = "quit"
                if event.key == pygame.K_RETURN:
                    if selected == "resume":
                        menu = False
                    if selected == "quit":
                        menu = False

        display.screen.fill('black')
        if selected == "resume":
            text_resume = text_format(">RESUME<", font, 20, 'white')
        else:
            text_resume = text_format("RESUME", font, 20, 'white')
        if selected == "quit":
            text_quit = text_format(">QUIT<", font, 20, 'white')
        else:
            text_quit = text_format("QUIT", font, 20, 'white')

        resume_rect = text_resume.get_rect()
        quit_rect = text_quit.get_rect()

        display.screen.blit(text_resume, (display_width / 2 - (resume_rect.width / 2), 300))
        display.screen.blit(text_quit, (display_width / 2 - (quit_rect.width / 2), 360))
        pygame.display.flip()
        display.clock.tick(FPS)
    if selected == 'resume':
        unpause()
    elif selected == 'quit':
        main_menu(from_pause=True)


def game_over():
    music.switch(2)
    menu = True
    background = pygame.transform.scale(load_image('menu_screens/game_over.png'), (display_width, display_height))
    selected = "restart"

    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = "restart"
                elif event.key == pygame.K_DOWN:
                    selected = "quit"
                if event.key == pygame.K_RETURN:
                    if selected == "restart":
                        menu = False
                    if selected == "quit":
                        menu = False

        display.screen.fill('black')
        display.screen.blit(background, (0, 0))
        title = text_format("GAME OVER", font, 40, 'red')
        if selected == "restart":
            text_restart = text_format(">RESTART<", font, 20, 'red')
        else:
            text_restart = text_format("RESTART", font, 20, 'red')
        if selected == "quit":
            text_quit = text_format(">QUIT<", font, 20, 'red')
        else:
            text_quit = text_format("QUIT", font, 20, 'red')

        title_rect = title.get_rect()
        restart_rect = text_restart.get_rect()
        quit_rect = text_quit.get_rect()

        display.screen.blit(title, (display_width / 2 - (title_rect.width / 2), 320))
        display.screen.blit(text_restart, (display_width / 2 - (restart_rect.width / 2), 380))
        display.screen.blit(text_quit, (display_width / 2 - (quit_rect.width / 2), 420))
        pygame.display.flip()
        display.clock.tick(FPS)
    if selected == 'restart':
        music.switch(1)
    elif selected == 'quit':
        main_menu()


class Display:
    def __init__(self, screen_size):
        self.screen = pygame.display.set_mode(screen_size)
        self.screen_rect = pygame.Rect((0, 0), (0, 0))
        self.clock = pygame.time.Clock()  # объект игровых часов
        self.camera = Camera()  # объект игровой камеры

    def reset(self):
        self.screen_rect.x = self.screen_rect.y = 0
        self.camera.reset()

    def set_level_size(self, level_size):
        self.screen_rect.width, self.screen_rect.height = level_size

    def update(self):
        self.clock.tick(FPS if not character.death else FPS // 3)
        self.screen.fill('black')

        self.camera.update(character)
        for sprite in all_sprites:
            self.camera.apply(sprite)
        for block in non_visible_things:
            self.camera.apply(block)
        self.camera.apply(self.screen_rect)
        all_sprites.draw(self.screen)
        character.update()
        mobs_group.update()

        pygame.display.flip()


if __name__ == '__main__':
    # Инициализация #
    pygame.display.set_caption('PAULUM AMBULARE.EXE')
    display_size = display_width, display_height = 1280, 640
    pygame.mouse.set_visible(False)

    # Спрайты #
    all_sprites = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    obstacles_group = pygame.sprite.Group()
    non_visible_things = pygame.sprite.Group()
    game_objects = pygame.sprite.Group()
    mobs_group = pygame.sprite.Group()

    all_groups = [all_sprites, player_group, obstacles_group, non_visible_things, mobs_group, game_objects]

    # Игровые переменные #
    music = Music(MUSIC_VOLUME)
    font = "8 Bit Font.ttf"
    display = Display(display_size)
    main_menu()
    game_map = TiledMap('level_ex.tmx')  # карта уровня
    tile_size = tile_width, tile_height = game_map.get_tile_size()  # размеры тайлов в пикселях
    level_tiles = level_width, level_height = game_map.get_level_size()  # размер уровня в тайлах
    display.set_level_size((level_width * tile_width, level_height * tile_height))
    character = game_map.render()
    if not TEST_MODE:
        character.check_standing()

    # Основной цикл #
    while True:
        # Проверка событий #
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and not character.death:
                pause_menu()

        # Передвижение персонажа #
        keys = pygame.key.get_pressed()
        if not character.attack and not character.death:
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                character.move(-SPEED, 0)
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                character.move(SPEED, 0)
            if TEST_MODE is True:
                if keys[pygame.K_UP]:
                    character.move(0, -SPEED)
                if keys[pygame.K_DOWN]:
                    character.move(0, SPEED)
            if not (keys[pygame.K_LEFT] or keys[pygame.K_a]) and not (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
                character.set_standing()
            if TEST_MODE is False:
                if keys[pygame.K_SPACE] and not character.fall and not character.jump:
                    character.set_jump(True)

        display.update()
