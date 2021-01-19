import pygame
import sys
import os
import pytmx

# Игровые константы #
SPEED = 10  # скорость персонажа
FPS = 30  # частота обновления экрана (кадров в секунду)
MUSIC_VOLUME = 0.1  # громкость музыки в процентах
SFX_VOLUME = 0.2  # громкость звуков в процентах
RIGHT = 1
LEFT = -1
TEST_MODE = True
TIMER_EVENT = pygame.USEREVENT  # событие для подсчета времени
pygame.time.set_timer(TIMER_EVENT, 100)

pygame.init()


def terminate():
    """Завершение работы программы"""
    pygame.quit()
    sys.exit()


def load_image(name: str) -> pygame.Surface:
    """Загрузка изображения name"""
    fullname = os.path.join('resources', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def play():
    """Запуск музыки"""
    pygame.mixer.music.play(loops=-1, fade_ms=2000)


def pause():
    """Приостановка музыки"""
    pygame.mixer.music.pause()


def unpause():
    """Запуск приостановленной музыки"""
    pygame.mixer.music.unpause()


def text_format(message, font_filename, size, color):
    """Форматирование текста message. Задание ему шрифта по пути font_filename, размера size и цвета color"""
    new_font = pygame.font.Font(f'resources/{font_filename}', size)
    new_text = new_font.render(message, True, color)

    return new_text


class Music:
    """Класс для взаимодействия с музыкой"""
    tracks = ['resources/music/Intro Theme.mp3',
              'resources/music/Grasslands Theme.mp3',
              'resources/music/Game Over.mp3',
              'resources/music/Victory Theme.mp3']

    def __init__(self, volume: float):
        """Инициализация. Задание громкости volume в диапазоне от 0 до 1"""
        self.current_track = 0
        pygame.mixer.music.load(Music.tracks[self.current_track])
        pygame.mixer.music.set_volume(volume)

    def switch(self, n):
        """Смена текущего трека на трек с id n"""
        self.current_track = n
        pygame.mixer.music.load(Music.tracks[self.current_track])
        play()


class Character(pygame.sprite.Sprite):
    """Класс персонажа"""
    # Константы персонажа #
    IDLE_ANIMATION_SPEED = 0.1
    ATTACK_ANIMATION_SPEED = 0.4
    OTHER_ANIMATION_SPEED = 0.2

    JUMP_HEIGHT = 8  # высота прыжка персонажа
    MIN_FALL_SPEED = 1  # минимальная скорость падения
    MAX_FALL_SPEED = JUMP_HEIGHT - 2  # максимальная скорость падения

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
    coin_sound = pygame.mixer.Sound('resources/sounds/coin.wav')

    # Звуки персонажа #
    jump_sound.set_volume(SFX_VOLUME)
    death_sound.set_volume(SFX_VOLUME)

    def __init__(self, x, y):
        """Инициализация. Перемещение спрайта на позицию x, y"""
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
        self.death = False

    def move(self, x, y):
        """Смещение спрайта на x, y пикселей. Проверка на коллизии с блоками, противниками, монетами,
        финишем. Проверка на вхождение в нижнюю границу уровня и проверка нахождения на платформе. """
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
        if self.rect.x + self.rect.w > display.screen_rect.x + display.screen_rect.w:
            self.rect.x = display.screen_rect.x + display.screen_rect.w - self.rect.w
        elif self.rect.x < display.screen_rect.x:
            self.rect.x = display.screen_rect.x
        if TEST_MODE is False:
            if not self.jump:
                self.check_standing()
        self.check_enemy_collision()
        self.check_out_of_bounds()
        self.check_coin()
        self.check_finish()

    def check_coin(self):
        """Проверка коллизии с монетами"""
        collided_object = pygame.sprite.spritecollideany(self, game_objects)
        if collided_object and isinstance(collided_object, Coin):
            Character.coin_sound.play()
            stats.increase_coins()
            collided_object.kill()

    def check_finish(self):
        """Проверка коллизии с финишем"""
        collided_object = pygame.sprite.spritecollideany(self, game_objects)
        if collided_object and isinstance(collided_object, Finish):
            finish()
            stats.reset_attempts()
            reset_level()

    def check_enemy_collision(self):
        """Проверка коллизии с врагом"""
        if not TEST_MODE:
            collided_enemy = pygame.sprite.spritecollideany(self, mobs_group)
            if collided_enemy:
                if not self.death:
                    self.set_death()

    def check_out_of_bounds(self):
        """Проверка вхождения в нижнюю границу уровня"""
        if self.rect.y >= display.screen_rect.y + display.screen_rect.h:
            if not self.death:
                self.set_death()

    def check_standing(self):
        """Проверка нахождения на платформе"""
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
        """Установка текущей анимации на animation"""
        if not self.death:
            self.current_animation = animation
            self.animation_frame = 0
            if animation in (Character.idle_animation_right, Character.idle_animation_left):
                self.animation_speed = Character.IDLE_ANIMATION_SPEED
            else:
                self.animation_speed = Character.OTHER_ANIMATION_SPEED

    def set_jump(self, state):
        """Установка прыжка на state"""
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
        """Перевод персонажа в состояние покоя"""
        if self.current_animation in (Character.run_animation_right, Character.run_animation_left):
            self.set_animation(Character.idle_animation_right if self.facing == RIGHT
                               else Character.idle_animation_left)

    def set_death(self):
        """Перевод персонажа в состояние смерти"""
        self.set_animation(Character.die_animation_right if self.facing == RIGHT else Character.die_animation_left)
        self.death = True
        stats.increase_attempts()
        Character.death_sound.play()
        pygame.mixer.music.fadeout(3000)

    def update(self):
        """Обновление персонажа. Перемещение персонажа по оси y если он прыгает или падает. Смена кадров анимации"""
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
        if self.current_animation in (Character.die_animation_right, Character.die_animation_left):
            if self.animation_frame >= len(self.current_animation):
                game_over()
                reset_level()
        self.animation_frame %= len(self.current_animation)
        self.image = self.current_animation[int(self.animation_frame)]


class Enemy(pygame.sprite.Sprite):
    """Класс врага"""
    # Константы персонажа #
    IDLE_ANIMATION_SPEED = 0.1

    # Анимации персонажа #
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

    def __init__(self, x, y):
        """Инициализация. Перемещение спрайта на позицию x, y"""
        super().__init__(mobs_group, all_sprites)

        self.current_animation = Enemy.run_animation_right
        self.animation_frame = 0
        self.attack_animation_type = 0
        self.animation_speed = Enemy.IDLE_ANIMATION_SPEED
        self.image = self.current_animation[self.animation_frame]
        self.rect = self.image.get_rect().move(x, y).inflate(-20, 0)

        self.facing = RIGHT

    def move(self, x):
        """Смещение спрайта на x пикселей. Проверка на коллизию с блоками или объектами-ограничителями"""
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
        """Установка текущей анимации на animation"""
        self.current_animation = animation
        self.animation_frame = 0

    def update(self):
        """Обновление спрайта. Смещение на SPEED // 5 пикселей. Смена кадров анимации"""
        self.move(SPEED // 5)
        self.animation_frame += self.animation_speed
        self.animation_frame = round(self.animation_frame, 1)
        self.animation_frame %= len(self.current_animation)
        self.image = self.current_animation[int(self.animation_frame)]


class Coin(pygame.sprite.Sprite):
    """Класс монет"""
    IDLE_ANIMATION_SPEED = 0.1

    # Анимация #
    idle_animation = [
        load_image('tilesheets/coin_1.png'),
        load_image('tilesheets/coin_2.png'),
        load_image('tilesheets/coin_3.png'),
        load_image('tilesheets/coin_4.png'),
        load_image('tilesheets/coin_5.png'),
        load_image('tilesheets/coin_6.png'),
        load_image('tilesheets/coin_7.png'),
        load_image('tilesheets/coin_8.png'),
        load_image('tilesheets/coin_9.png'),
        load_image('tilesheets/coin_10.png'),
        load_image('tilesheets/coin_11.png'),
        load_image('tilesheets/coin_12.png'),
    ]

    def __init__(self, x, y):
        """Инициализация. Перемещение спрайта на позицию x, y"""
        super().__init__(game_objects, all_sprites)

        self.animation_frame = 0
        self.attack_animation_type = 0
        self.animation_speed = Coin.IDLE_ANIMATION_SPEED
        self.image = Coin.idle_animation[self.animation_frame]
        self.rect = self.image.get_rect().move(x, y)

    def update(self):
        """Обновление спрайта. Смена кадра анимации"""
        self.animation_frame += self.animation_speed
        self.animation_frame = round(self.animation_frame, 1)
        self.animation_frame %= len(Coin.idle_animation)
        self.image = Coin.idle_animation[int(self.animation_frame)]


class Tile(pygame.sprite.Sprite):
    """Основной класс для большинства игровых объектов на карте"""
    def __init__(self, tile_img, x, y, w, h):
        """Иницилизация. Созднание спрайта с размером w * h пикселей. Перемещение спрайта на позицию (x; y)"""
        super().__init__(all_sprites)
        self.image = tile_img
        self.image = pygame.transform.scale(self.image, (w, h))
        self.rect = self.image.get_rect().move(x, y)


class Block(Tile):
    """Класс блока-препятствия"""
    def __init__(self, tile_img, x, y):
        """Инициализация аналогичная классу Tile"""
        super().__init__(tile_img, x, y, tile_width, tile_height)
        self.add(obstacles_group)


class Deco(Tile):
    """Класс блоков-ограничителей"""
    def __init__(self, img, x, y, w, h):
        """Инициализация аналогичная классу Tile"""
        super().__init__(img, x, y, w, h)
        self.add(non_visible_things)
        self.remove(all_sprites)


class Finish(Tile):
    """Класс финишного флага"""
    def __init__(self, img, x, y, w, h):
        """Инициализация аналогичная классу Tile"""
        super(Finish, self).__init__(img, x, y, w, h)
        self.add(game_objects)


def reset_level():
    """Пересоздание уровня"""
    global character
    # Обнуление статистики и удаление спрайтов #
    stats.reset_time()
    stats.reset_coins()
    game_map.reset_coins()
    for group in all_groups:
        group.empty()
    # Возвращение экрана и игрока в исходное состояние #
    character = game_map.render()
    display.reset()


class TiledMap:
    """Класс для загрузки уровня сделанного в TiledMapEditor"""
    def __init__(self, tmx_map):
        tmx_map = "main_maps/" + tmx_map
        self.level_map = pytmx.load_pygame(tmx_map, pixelalpha=True)
        self.coins = 0

    def get_tile_size(self):
        """Получениие размеров тайла"""
        return self.level_map.tilewidth, self.level_map.tileheight

    def get_level_size(self):
        """Получение размера уровня в тайлах"""
        return self.level_map.width, self.level_map.height

    def get_coins(self):
        """Получение количества монет на уровне"""
        return self.coins

    def reset_coins(self):
        """Обнуление количества монет на уровне"""
        self.coins = 0

    def render(self) -> Character:
        """Прорисовка всех объектов на уровне"""
        char = None
        for x, y, gid in self.level_map.layernames['Background']:
            tile = self.level_map.get_tile_image_by_gid(gid)
            if tile:
                Tile(tile, x * tile_width, y * tile_height, tile_width, tile_height)
        for tile_object in self.level_map.layernames['Platforms']:
            if tile_object.type == 'Block':
                Block(tile_object.image, tile_object.x, tile_object.y)
        for entity in self.level_map.layernames['Mobs']:
            Enemy(entity.x, entity.y)
        for entity in self.level_map.layernames['Character']:
            char = Character(entity.x, entity.y)
        for block in self.level_map.layernames['Collisions']:
            if block.type == 'Collide':
                Deco(block.image, block.x, block.y, int(block.width), int(block.height))
        for entity in self.level_map.layernames['Game Objects']:
            if entity.type == 'Finish':
                Finish(entity.image, entity.x, entity.y, int(entity.width), int(entity.height))
            elif entity.type == 'Coin':
                Coin(entity.x, entity.y)
                self.coins += 1
        for x, y, gid in self.level_map.layernames['Water']:
            tile = self.level_map.get_tile_image_by_gid(gid)
            if tile:
                Tile(tile, x * tile_width, y * tile_height, tile_width, tile_height)
        return char


class Camera:
    """Класс для фиксации объекта в центре экрана"""
    X_TOLERANCE = SPEED
    Y_TOLERANCE = Character.MAX_FALL_SPEED ** 2

    def __init__(self):
        """Инициализация"""
        self.dx = 0
        self.dy = 0

        self.scroll_x = True
        self.scroll_y = True

        self.top_blocked = self.bottom_blocked = self.right_blocked = self.left_blocked = False

    def reset(self):
        """Возвращение камеры в исходное состояние"""
        self.dx = 0
        self.dy = 0

        self.scroll_x = True
        self.scroll_y = True

        self.top_blocked = self.bottom_blocked = self.right_blocked = self.left_blocked = False

    def apply(self, obj):
        """Сдвиг объекта obj на смещение камеры"""
        if isinstance(obj, pygame.sprite.Sprite):
            obj.rect.x += self.dx if self.scroll_x else 0
            obj.rect.y += self.dy if self.scroll_y else 0

        elif isinstance(obj, pygame.Rect):
            obj.x += self.dx if self.scroll_x else 0
            obj.y += self.dy if self.scroll_y else 0
            if obj.x + obj.w <= display_width + Camera.X_TOLERANCE:
                self.scroll_x = False
                self.right_blocked = True
            if obj.x >= -Camera.X_TOLERANCE:
                self.scroll_x = False
                self.left_blocked = True
            if obj.y + obj.h <= display_height + Camera.Y_TOLERANCE:
                self.scroll_y = False
                self.bottom_blocked = True
            if obj.y >= -Camera.Y_TOLERANCE:
                self.scroll_y = False
                self.top_blocked = True

    def update(self, target):
        """Позиционирование камеры на объекте target"""
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
    """Запуск главного меню"""
    menu = True
    music.switch(0)
    background = pygame.transform.scale(load_image('menu_screens/main_menu.png'), (display_width, display_height))
    selected = "start"

    # Проверка и обработка событий #
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
    """Запуск меню паузы"""
    pause()
    menu = True
    selected = "resume"

    # Проверка событий #
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

    # Обработка выбранного пункта меню #
    if selected == 'resume':
        unpause()
    elif selected == 'quit':
        main_menu(from_pause=True)


def game_over():
    """Запуск экрана смерти"""
    music.switch(2)
    menu = True
    background = pygame.transform.scale(load_image('menu_screens/game_over.png'), (display_width, display_height))
    selected = "restart"

    # Проверка событий #
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
    # Обработка выбранного пункта меню #
    if selected == 'restart':
        reset_level()
        music.switch(1)
    elif selected == 'quit':
        main_menu()


def finish():
    """Запуск экрана победы"""
    color = pygame.Color(255, 230, 0)
    pygame.mixer.music.load(Music.tracks[3])
    pygame.mixer.music.play()
    attempts, time, coins = stats.get_stats()
    all_coins = game_map.get_coins()
    attempts_text = text_format(f"ATTEMPTS: {attempts}", font, 20, color)
    time_text = text_format(f"TIME: {time}", font, 20, color)
    coins_text = text_format(f"COINS: {coins}/{all_coins}", font, 20, color)
    time_template = time_text.get_rect()
    menu = True
    background = pygame.transform.scale(load_image('menu_screens/victory_screen.png'), (display_width, display_height))
    selected = "retry"

    # Проверка событий #
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = "retry"
                elif event.key == pygame.K_DOWN:
                    selected = "quit"
                if event.key == pygame.K_RETURN:
                    if selected == "retry":
                        menu = False
                    if selected == "quit":
                        menu = False

        display.screen.fill('black')
        display.screen.blit(background, (0, 0))
        title = text_format("YOU WIN!", font, 60, color)
        if selected == "retry":
            text_retry = text_format(">RETRY<", font, 20, color)
        else:
            text_retry = text_format("RETRY", font, 20, color)
        if selected == "quit":
            text_quit = text_format(">QUIT<", font, 20, color)
        else:
            text_quit = text_format("QUIT", font, 20, color)

        title_rect = title.get_rect()
        retry_rect = text_retry.get_rect()
        quit_rect = text_quit.get_rect()

        display.screen.blit(title, (display_width / 2 - (title_rect.width / 2), 60))
        display.screen.blit(text_retry, (display_width / 2 - (retry_rect.width / 2), 180))
        display.screen.blit(text_quit, (display_width / 2 - (quit_rect.width / 2), 220))
        display.screen.blit(attempts_text, (100, 200))
        display.screen.blit(time_text, (display_width - time_template.width - 100, 200))
        display.screen.blit(coins_text, (100, 240))
        pygame.display.flip()
        display.clock.tick(FPS)
    # Обработка выбранного пункта меню #
    if selected == 'retry':
        music.switch(1)
    elif selected == 'quit':
        main_menu()


class Display:
    """Класс для обновления экрана"""
    def __init__(self, screen_size):
        """Инициализация. Созднание экрана с размером screen_size"""
        self.screen = pygame.display.set_mode(screen_size)
        self.screen_rect = pygame.Rect((0, 0), (0, 0))
        self.clock = pygame.time.Clock()  # объект игровых часов
        self.camera = Camera()  # объект игровой камеры

    def reset(self):
        """Возвращение экрана в исходное положение"""
        self.screen_rect.x = self.screen_rect.y = 0
        self.camera.reset()

    def set_level_size(self, level_size):
        """Задание размера уровня level_size в пикселях"""
        self.screen_rect.width, self.screen_rect.height = level_size

    def update(self):
        """Обновление картинки на экране. Обновление игровых объектов"""
        self.clock.tick(FPS if not character.death else FPS // 2)
        self.screen.fill('black')

        self.camera.update(character)
        for sprite in all_sprites:
            self.camera.apply(sprite)
        for block in non_visible_things:
            self.camera.apply(block)
        self.camera.apply(self.screen_rect)
        all_sprites.draw(self.screen)
        character.update()
        game_objects.update()
        mobs_group.update()

        pygame.display.flip()


class Stats:
    """Класс для хранения и изменения статистик персонажа"""
    def __init__(self):
        """Инициализация"""
        self.attempts = 1
        self.coins = 0
        self.time_passed = 0

    def get_stats(self):
        """Получение игровой статистики"""
        return self.attempts, self.time_passed, self.coins

    def increase_attempts(self):
        """Увеличить количество попыток"""
        self.attempts += 1

    def increase_coins(self):
        """Увеличить количество монет"""
        self.coins += 1

    def increase_time(self, delta_time):
        """Увеличить количество прошедшего игрового времени"""
        self.time_passed += delta_time
        self.time_passed = round(self.time_passed, 1)

    def reset_attempts(self):
        """Возвращение попыток к исходному значению"""
        self.attempts = 1

    def reset_coins(self):
        """Возвращение собранных монет к исходному значению"""
        self.coins = 0

    def reset_time(self):
        """Возвращение прошедшего времени к исходному значению"""
        self.time_passed = 0


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

    all_groups = [all_sprites, player_group, obstacles_group, non_visible_things, game_objects, mobs_group]

    # Игровые переменные #
    music = Music(MUSIC_VOLUME)
    font = "8 Bit Font.ttf"
    display = Display(display_size)
    game_map = TiledMap('main_level.tmx')  # карта уровня
    tile_size = tile_width, tile_height = game_map.get_tile_size()  # размеры тайлов в пикселях
    level_tiles = level_width, level_height = game_map.get_level_size()  # размер уровня в тайлах
    display.set_level_size((level_width * tile_width, level_height * tile_height))
    stats = Stats()

    # Запуск игры #
    main_menu()
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
            if event.type == TIMER_EVENT:
                stats.increase_time(0.1)

        # Передвижение персонажа #
        keys = pygame.key.get_pressed()
        if not character.death:
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
