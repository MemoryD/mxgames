[mxgames](https://github.com/MemoryD/mxgames) 是一个由 python 写的小游戏集合，基于 pygame。

### 安装

```shell
$ pip install mxgames
```



### 运行

以下命令可以获得一个游戏列表：

```shell
$ python -m mxgames
```

以下命令开始一个游戏：

```shell
$ python -m mxgames.[gamename]
```

`[gamename]` 是游戏名。



### 游戏介绍

- #### **life**

  经典的生命游戏，理论上不需要玩家操作，但是我增加了点击操作，增加更多的可能性和趣味性。

  ```shell
  $ python -m mxgames.life
  ```

  ![life](https://raw.githubusercontent.com/MemoryD/mxgames/master/screenshot/life.gif)

- #### **2048**

  移动方块，相同的方块会融合，一步步凑出 2048。大家应该也很熟悉。

  ```shell
  $ python -m mxgames.2048
  ```

  ![2048](https://raw.githubusercontent.com/MemoryD/mxgames/master/screenshot//2048.gif)

- #### snake

  贪吃蛇，地球人都知道的游戏。

  ```shell
  $ python -m mxgames.snake
  ```

  ![snake](https://raw.githubusercontent.com/MemoryD/mxgames/master/screenshot/snake.gif)

- #### **AI snake**

  自动寻路的贪吃蛇，基于近似的哈密顿环，加入了一些优化，游戏无需操作，但是可以按空格键暂停，游戏运行后会有以下三种结果：

  - 吃满整个屏幕。
  - 没吃满屏幕就陷入死路。
  - 没吃满屏幕，陷入了无限循环，不断绕圈。

  ```shell
  $ python -m mxgames.ai_snake
  ```

  ![ai_snake](https://raw.githubusercontent.com/MemoryD/mxgames/master/screenshot/ai_snake.gif)

  

  