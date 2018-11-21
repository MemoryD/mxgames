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

  ![life](https://github.com/MemoryD/mxgames/blob/master/screenshot/life.gif)

- #### **2048**

  移动方块，相同的方块会融合，一步步凑出 2048。大家应该也很熟悉。

  ```shell
  $ python -m mxgames.2048
  ```

  ![life](https://github.com/MemoryD/mxgames/blob/master/screenshot/2048.gif)

- #### snake

  贪吃蛇，地球人都知道的游戏。

  ```shell
  $ python -m mxgames.snake
  ```

  ![life](https://github.com/MemoryD/mxgames/blob/master/screenshot/snake.gif)

