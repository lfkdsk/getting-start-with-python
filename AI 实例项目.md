#    AI Game FightTheater



## 获取实例代码

1. 创建虚拟环境 & 安装依赖包：


``` shell
# 启动虚拟环境
virtualenv env
source env/bin/activate
# 安装依赖包
pip install -r requirements.txt
# 安装 gameobjects 包
cd gameobjects-0.0.3
python ./setup.py install
```

2. 启动游戏：

``` shell
python game
```


![show](project-game/pic.gif)



## Fighter Theater

恭喜你！当你读到这个章节的时候你对 Python 的基础知识已经有了一定的了解了，在前面的几个章节之中我们由浅入深的涉及到了 Python 使用的各个方面，我们从 HelloWorld 入手直到涉及到了更有深度的内容，让我们能怎么写出来更具有 Pythonic 风格的代码。

现在我们就来开发一些有趣的 Python 应用程序，本门课程是做人工智能、机器学习的基础课程和理论基础，这里我们就来开发一款名叫 **Fighter Theater** 的 AI 游戏，这款游戏相较于我们平常接触的能够玩的游戏来讲，更像是一种能够自动运行的程序，游戏中出现的 Hero（Sprite 精灵）都包含一种被称作 自动机（State Machine），自动机中包含多个状态（State）当条件发生变化的时候，就会产生一些动作（Action），之后换转入到一个新的 State。

![fsm](project-game/fsm.png)

在游戏中我们将英雄（Hero）氛围绿、红两方，两侧各有一个代表当前方的神社，游戏场景之中会随机刷新出能量石（Energy Store），双方的英雄会在一定的区域进行游荡，当发现了新的能量石之后就会根据距离进行前往能量石的位置去捡起能量石并且送往神社，神社就会获得加分。如果路上遇到敌方的英雄就会进行互相攻击，而血量减少的时候就会试图逃跑。随着时间的流逝，双方的英雄也会随机的增加在界面之上，这让我们的游戏能 `Live Long and Prosper` 。

![project-game](project-game/pic.png)

在这个项目之中我们会接触一个 Python 的第三方模块 —— Pygame，Pygame 是一个非常简洁明快的游戏开发模块，这里没有太多框架性质的复杂要求，我们可以轻松地使用模块中提供的一些工具就能方便的创建图形、显示动画、播放声音等等的功能，这里我们要去用这个模块来制作一些复杂的游戏。



## 规划项目

相比于我们之前的 Python 的学习都是在使用代码段进行学习开发，而这时我们是在开发一个大型的复杂程序，提前规划好项目的结构并且对程序进行解耦是非常有必要的。有了项目的具体规划（蓝图）再去施工就能让我们开发的程序的流程更为规范，不至于偏离我们想要的轨道。

这里我们可以先来看一下项目之中的文件结构：

``` shell
$ tree .
.
├── __init__.py
├── __main__.py
├── entities.py
├── game_funcs.py
├── settings.py
├── starter.py
├── states.py
└── world.py

0 directories, 8 files
```

* `__main__.py` 是当前 game 包的启动模块，我们在这个模块之中启动游戏项目。
* `entities.py` 中我们定义游戏中出现的实体类，包含基类、Hero 和 EnergyStore
* `game_funcs.py` 中我们保存了一些游戏主循环之中的逻辑方法，用来拓展解耦。
* `settings.py` 文件之中我们保留游戏中一些全局的配置，在一个统一的地方进行统一的配置想要修改的时候就会十分方便。
* `starter.py` 中我们存放了游戏开启的主循环。
* `states.py` 中我们定义了游戏中使用的状态机定义。
* `world.py` 中设定了整个游戏世界的生命周期过程。

## 预先准备

为了将这个程序和其他程序的依赖包版本进行隔离，我们最好使用虚拟环境进行安装依赖包，这里我们可以参考 **附录D-使用虚拟环境** 配置并使用虚拟环境。

我们要使用 Pygame 进行开发，Pygame 模块并不是 Python 所自带的模块因此我们需要使用 pip 进行安装，关于使用 pip 进行安装模块可以查看 **附录C-使用 pip 包管理工具**。但在这里 Pygame 使用的依赖可能很多，这里我们就不妨赘述一下 Pygame 的安装过程。

##### Linux 下安装

在 Linux 下安装 Pygame ，尤其我们使用 2.7.x 版本的 Python 是比较好安装的，这里我们可以使用 pip 进行安装：

``` python
pip install pygame
```

也可以使用 `apt` 进行安装：

``` python
sudo apt-get install python-pygame
```

##### macOS 下安装

在 macOS 下的安装除了 pip 安装 pygame 之外，我们还有使用 HomeBrew 安装一些 Pygame 的依赖库，关于 HomeBrew 的使用我们可以去官网了解学习。

使用 HomeBrew 安装依赖库：

``` shell
brew install hg sdl sdl_image sdl_ttf
```

如果想要使用和音频相关的依赖库，我们还需要：

``` python
brew install sdl_mixer portmidi
```

##### Windows 下安装

在官方网站中直接寻找可下载的 release 版本：

``` shell
https://www.pygame.org/news
```

------

这里我们也建议在 `requirements.txt` 中记录所有的 Python 的第三方依赖包：

``` shell
pytmx==3.21.5
pygame==1.9.3
psutil==5.4.3
```

完成一个游戏我们不只是需要程序代码，资源文件图片、地图等等东西也是非常必要的东西，这里和这个游戏相关的资源文件我们都有提供可以在这个位置获取

``` shell
https://github.com/lfkdsk/FighterTheater/tree/master/img
```

这其中包含背景的雪碧图、瓦片地图文件、各个英雄和能量石的具体图片。





## 开启游戏项目

在使用 Pygame 的基础结构之中，我们把启动项目的文件设计成标准的 Python 脚本的启动文件：

``` python
def game_looper():
  # ...
  pass

if __name__ == '__main__':
  game_looper()
```

我们在脚本之中经常会见到这样的结构，我们不写出在模块之中直接编写逻辑，而是抽出脚本的主程序然后进行一个判断。这个判断 `if __name__ == '__main__'` 可能对很多人产生困惑，在 Python 之中这种带有两侧双下划线的方法被称作 Python 的 magical method ，这个 `__name__` 代表了当前的模块的名称，而当这个属性是 `'__main__'` 的时候代表这个模块是作为启动程序来启动，这时候我们才运行游戏的主循环。

解决了这个部分的逻辑结构，我们先来创建一个空的 Pygame 窗口，创建 Pygame 窗口的基础结构是这个样子的：

``` python
import pygame
import sys

def game_looper():
    pygame.init()
    game_screen = pygame.display.set_mode((960， 640))
    while True:
        # 处理事件逻辑
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        pygame.display.update()
```

这里我们给处理一个非常基础的创建 Pygame 窗口的模板代码，首先我们使用 `pygame.init()` 来初始化 Pygame 的设置。在 L6 我们使用 `pygame.display.set_mode(tuple)` 来创建一个









