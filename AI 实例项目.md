# AI Game FightTheater



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

在游戏中我们将英雄（Hero）氛围绿、红两方，两侧各有一个代表当前方的神社，游戏场景之中



## 规划项目

