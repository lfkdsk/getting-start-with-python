# AI Game FightTheater



## 使用 World 创建生命周期

在上面的一个章节之中我们把两个对象绘制到了屏幕上面去，我们走出了第一步，但是如果每当我们添加一个对象的时候都要在 while 循环里面调用一个 `render` 方法，我们明显不能为每个创建的对象调用这个 `render` 方法，那么我们就要有一个统筹的方法来设计游戏的生命周期。

为此我们设计了一个 `World` 类来进行生命周期的管理：

``` python
class World(object):
    def __init__(self, screen):
			# 包含世界中全部的精灵对象的处理
      # 还要包含瓦片背景的初始化
   	def render(self, surface):
      # 为每一个对象调用 render 对象
    
    # 还要包含为世界增加、消灭对象的方法
```

我们先实现 World 中的一部分初始化的代码：

``` python
class World(object):
    def __init__(self, screen):
        # 全部的精灵对象
        self.entities = {}
        # current entity id
        self.entity_id = 0
        # 加载地图
        self.game_map = load_pygame(game_settings.MAP_DIR)
        self.background_layer = Surface(game_settings.SCREEN_SIZE).convert_alpha()
        self.player_layer = Surface(game_settings.SCREEN_SIZE).convert_alpha()
        self.player_layer.fill((0, 0, 0, 0))
        # initial double-side heroes
        draw_background_with_tiled_map(self.background_layer, self.game_map)
        screen.blit(self.background_layer, game_settings.SCREEN_SIZE)
```

和刚才说的一样我们在 World 的初始化方法之中，添加了管理对象的一些属性，并且加载了我们之前使用的 **瓦片地图** 的内容。这里的绘制方法和之前看起来相比有一些复杂：

![layers](project-game/layers.png)

我们在 World 里面创建了两个 Layer （分层），用来处理不同的事情，一个是 `background_layer` 专门用来绘制瓦片地图的背景，由于我们对背景没有什么改变，所以不用重复在 while 循环里面反复的渲染重绘，之后我们又创建了一个 `player_layer` 这个分层单独用来绘制全部的游戏对象，这个层次的背景是透明的（`(0, 0, 0, 0)` 的不透明度是 0 因此是透明的） ，`player_layer` 只用来绘制精灵，而背景要从下面的一层之中显示，因此 `player_layer` 的背景要是透明的。

再下面我们来看 World 的 `render()` 方法：

``` python
    def render(self, surface):
        self.player_layer.fill((0, 0, 0, 0))

        # render entities
        for entity in self.entities.values():
            entity.render(self.player_layer)

        # render_score_message(self.player_layer)
        surface.blit(self.background_layer, (0, 0))
        surface.blit(self.player_layer, (0, 0))
```

`render()` 方法是用来在 `While` 循环之中进行刷新重绘的，因此在每次重绘都会把 `player_layer` 清空成透明。之后我们会对 `entities` 里面所有的对象调用绘制，这里我们会注意到我们在调用 `entity.render()` 的时候使用的 Surface 对象是 `player_layer` ，而不是传入的 surface。这也说明我们确实把对象都绘制到了对象层。

在之后的两行就体现出了我们 World 分层的实现方式：

``` python
        surface.blit(self.background_layer, (0, 0))
        surface.blit(self.player_layer, (0, 0))
```

我们在全局的 surface 上面进行绘制，先绘制的背景层次，然后再绘制的对象层次。

之后我们再添加一对方法用来向世界添加 Hero 对象和移除 Hero 对象：

``` python
    def add_entity(self, entity):
        self.entities[self.entity_id] = entity
        entity.id = self.entity_id
        self.entity_id += 1

    def remove_entity(self, entity):
        del self.entities[entity.id]
```

`add_entity` 使用 `entity_id` 这个字段来管理当前创建的对象的 id 数目，而 `remove_entity` 就是删除对应 ID 的对象。这里我们来对这个 World 类进行一下测试，我们写一个向 World 随机生成 Hero 对象的方法：

``` python
def random_create(world):
    from game.entities import Hero
    green_hero_img = load_alpha_image('green_hero.png')
    graves_img = load_alpha_image('graves.png')

    for _ in range(0, 11):
        randX, randY = randint(0, game_settings.SCREEN_WIDTH), randint(0, game_settings.SCREEN_HEIGHT)
        hero = Hero(world, green_hero_img, graves_img, 'green')
        hero.location = Vector2(randX, randY)
        hero.name = 'green-hero'
        world.add_entity(hero)
```

这里我们使用 `for-in` 循环使用 `randint` 方法创建了分布在全局的随机位置，之后这些 Hero 对象都会被通过 `add_entity` 方法添加到 World 之中，我们在 `starter.py` 的 `While` 循环之中只要调用 World 的 render 函数就可以使用了：

``` python
    game_world = World(game_screen)
    random_create(game_world)

    while not game_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True
                
        game_world.render(game_screen)
        pygame.display.update()
```



