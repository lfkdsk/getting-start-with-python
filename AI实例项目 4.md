## 整合游戏策略

我们基本的游戏的功能算是已经完成了，这里我们剩余的一些部分就是如何才能设计好游戏的运行节奏，能让我们这个可以无限进行 “观赏” 的游戏进行下去的策略也是非常重要的，这一节会介绍 `game_funcs.py` 实现中的一些策略函数的实现：

``` python
def initial_heroes(world):
    green_hero_nums = game_settings.DEFAULT_HERO_NUM
    for _ in range(green_hero_nums):
        item = create_hero(world, 'green')
        while has_close_entities(world, item):
            item.location = get_left_random_location()

    red_hero_nums = game_settings.DEFAULT_HERO_NUM
    for _ in range(red_hero_nums):
        item = create_hero(world, 'red')
        while has_close_entities(world, item):
            item.location = get_right_random_location()

    store_nums = game_settings.DEFAULT_HERO_NUM
    for _ in range(store_nums):
        create_random_store(world)
```

`initial_heroes` 函数在 World 的初始化函数之中各初始化相同数目的双方的 Hero，我们这里借用了 `has_close_entities` 方法判断初始化对象附近是否有其他的己方对象就重新 roll 位置，这样能让我们双方初始化对象的时候的位置更为分散，在这之后我们又会随机创建多个初始化的能量石。

另外我们会在 World 里面增加一个生命周期 `random_emit()` :

``` python
    def random_emit(self):
        create_random_heroes(self)
        create_random_stores(self)
 
# game_funcs.py
def create_random_heroes(world):
    if randint(0, 100) == 80 and len(world.entities) < game_settings.MAX_ENTITIES:
        create_hero(world, HERO_TYPES[randint(0, 1)])
        create_hero(world, world.min_hero_type())


def create_random_stores(world):
    if randint(1, 20) == 10 and len(world.energy_stores) < 40:
        store = create_random_store(world)
        world.energy_stores[store.id] = store
```

这个生命周期会在每次循环的时候通过随机数 roll 中来判断是否创建新的 Hero 和新的 Energy Stone，这里面我们为了防止局势产生一边倒的情况，我们在 roll 中生成随机 Hero 的时候，在给一方增加新 Hero 的时候，也会给当前较少的那一方的 Hero Type 也创建一个 Hero 对象。

定义在屏幕中打印 Text 的函数：

``` python
def display_message(screen, text, size, color, rect):
    largeText = pygame.font.Font(None, size)
    TextSurf, TextRect = text_objects(text, largeText, color)
    TextRect.left = rect[0]
    TextRect.top = rect[1]
    screen.blit(TextSurf, TextRect)


def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()
```

并且提供这两个方法的使用函数：

``` python
def render_score_message(surface):
    # render scores
    display_message(
        text='G:{}'.format(game_settings.left_score),
        color=(255, 255, 255),
        size=22,
        rect=(20, 20),
        screen=surface
    )

    display_message(
        text='R:{}'.format(game_settings.right_score),
        color=(255, 255, 255),
        size=22,
        rect=(20, 40),
        screen=surface
    )

    display_message(
        text='Memory: {}'.format(psutil.Process(os.getpid()).memory_info().rss),
        color=(255, 255, 255),
        size=22,
        rect=(20, 60),
        screen=surface
    )

    display_message(
        text='Time: {}'.format(datetime.datetime.now() - start_time),
        color=(255, 255, 255),
        size=22,
        rect=(20, 80),
        screen=surface
    )
```

这里面我们在屏幕的左上角打印，两侧获得能量石的得分，并且打印当前的内存消耗，和整个程序的运行时长。

在我们实现了以上的游戏策略成功应用之后，我们就能完成如实例所示 Python Game 了。

::: collapse game_funcs.py

``` python
import os
from random import randint

import psutil
import pygame
from gameobjects.vector2 import Vector2
import datetime
from settings import game_settings
from states import HERO_STATES


def draw_background_with_tiled_map(game_screen, game_map):
    # draw map data on screen
    for layer in game_map.visible_layers:
        for x, y, gid, in layer:
            tile = game_map.get_tile_image_by_gid(gid)
            if not tile:
                continue

            game_screen.blit(
                tile,
                (x * game_map.tilewidth,
                 y * game_map.tileheight)
            )


def load_alpha_image(resource_img):
    path = os.path.join(
        game_settings.BASE_DIR,
        'img/{}'.format(resource_img),
    )

    return pygame.image.load(path)


green_hero_img = load_alpha_image('green_hero.png')
red_hero_img = load_alpha_image('red_hero.png')
graves_img = load_alpha_image('graves.png')

HERO_TYPES = ('red', 'green')

green_energy_img = load_alpha_image('green_energy.png')
red_energy_img = load_alpha_image('red_energy.png')
ENERGY_IMAGES = {
    'green-store': green_energy_img,
    'red-store': red_energy_img,
}


def display_message(screen, text, size, color, rect):
    largeText = pygame.font.Font(None, size)
    TextSurf, TextRect = text_objects(text, largeText, color)
    TextRect.left = rect[0]
    TextRect.top = rect[1]
    screen.blit(TextSurf, TextRect)


def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()


def get_left_random_location():
    x, y = game_settings.LEFT_HOME_LOCATION
    randX, randY = randint(x, x + 80), randint(80, game_settings.SCREEN_HEIGHT - 40)
    return Vector2(randX, randY)


def get_right_random_location():
    x, y = game_settings.RIGHT_HOME_LOCATION
    randX, randY = randint(x - 80, x), randint(80, game_settings.SCREEN_HEIGHT - 40)
    return Vector2(randX, randY)


def create_hero(world, hero_type):
    if hero_type == 'green':
        location = get_left_random_location()
        image = green_hero_img
        hero_name = 'green-hero'
    elif hero_type == 'red':
        location = get_right_random_location()
        image = red_hero_img
        hero_name = 'red-hero'
    else:
        raise KeyError("error type")

    from entities import Hero
    hero = Hero(world, image, graves_img, hero_type)
    hero.location = location
    hero.name = hero_name
    hero.brain.set_state(HERO_STATES[0])
    world.add_entity(hero)

    return hero


def create_random_store(world):
    rand_type = 0 if randint(0, 100) % 2 == 0 else 1
    energy_img, energy_type = ENERGY_IMAGES.values()[rand_type], ENERGY_IMAGES.keys()[rand_type]
    from entities import EnergyStore
    energy_store = EnergyStore(world, energy_img, energy_type)
    w, h = game_settings.SCREEN_SIZE
    energy_store.location = Vector2(randint(60, w - 60), randint(60, h - 60))
    world.add_energy_store(energy_store)

    return energy_store


def create_random_heroes(world):
    if randint(0, 100) == 80 and len(world.entities) < game_settings.MAX_ENTITIES:
        create_hero(world, HERO_TYPES[randint(0, 1)])
        create_hero(world, world.min_hero_type())


def create_random_stores(world):
    if randint(1, 20) == 10 and len(world.energy_stores) < 40:
        store = create_random_store(world)
        world.energy_stores[store.id] = store


def has_close_entities(world, item):
    entities = world.entities
    for entity in entities.values():
        item_location = entity.location
        if item.id != entity.id and item_location.get_distance_to(item.location) < 30:
            return True

    return False


def initial_heroes(world):
    green_hero_nums = game_settings.DEFAULT_HERO_NUM
    for _ in range(green_hero_nums):
        item = create_hero(world, 'green')
        while has_close_entities(world, item):
            item.location = get_left_random_location()

    red_hero_nums = game_settings.DEFAULT_HERO_NUM
    for _ in range(red_hero_nums):
        item = create_hero(world, 'red')
        while has_close_entities(world, item):
            item.location = get_right_random_location()

    store_nums = game_settings.DEFAULT_HERO_NUM
    for _ in range(store_nums):
        create_random_store(world)


start_time = datetime.datetime.now()


def render_score_message(surface):
    # render scores
    display_message(
        text='G:{}'.format(game_settings.left_score),
        color=(255, 255, 255),
        size=22,
        rect=(20, 20),
        screen=surface
    )

    display_message(
        text='R:{}'.format(game_settings.right_score),
        color=(255, 255, 255),
        size=22,
        rect=(20, 40),
        screen=surface
    )

    display_message(
        text='Memory: {}'.format(psutil.Process(os.getpid()).memory_info().rss),
        color=(255, 255, 255),
        size=22,
        rect=(20, 60),
        screen=surface
    )

    display_message(
        text='Time: {}'.format(datetime.datetime.now() - start_time),
        color=(255, 255, 255),
        size=22,
        rect=(20, 80),
        screen=surface
    )
```

:::

