# note自由

*为了让游戏有更强的自由性，我们就需要让note的速度、起始位置、图片等更富有多样性。那么我们怎样去实现这一功能？*

## 1、v=s/t

我们以黄模式为例，来解释这一公式的具体应用。![noteFreedome1](C:\Users\hdy\Documents\PythonScripts\ehirection\README\noteFreedome1.png)

> 若给定的数据只有一个路程或速度，那么就应使用
> $$
> t=s / v(pixel / sec) = s / (v (pixel / frame) * LastFpsTime / 1000)
> $$
> 来计算另一值。
>
> 但如果用户想要更改速度的同时保持路程不变呢？

![noteFreedome2](C:\Users\hdy\Documents\PythonScripts\ehirection\README\noteFreedome2.png)

> 显而易见，我们需要更改那个所谓的定制“t”来达到目的。而这个定制t不应该被直接更改，而是通过v和s来更改
>
> 因此，我们就需要两个数据，即速度和路程。
> $$
> t = s / v
> $$

当然，并不是任何时候我们都要改变两个值。有的时候我们只需要改变速度，这时另一个值当然要用默认值。

默认值：

t = 1s

s = 335pixel

v = 335 pixel / s

当用户更改速度和路程其中的某一个值，t跟着变化。

当然这是在非比例模式下。

## 2、实际游戏

### 负数时间轴

原本我的算法是提前播放音乐，但是这不好控制。于是我引用一个负的时间轴。

实际游戏运算中，电脑会先读取铺面数据，在这期间，计算所有note的延迟，也就是上文提到的”t“。之后再拿文件中的note时间减去该值，获得一个实际添加值。具体如下：
$$
currentTime = documentTime - delayTime(t)
$$
当然是允许负数的。

然后选出所有note中最小的一个currentTime，并且时间从该值流动，运算也从该值开始。音乐在时间为0的时候开始播放。

举个例子：如果算出最小的currentTime为-1.2，那么GameVar.lastTime（实际判定时间）就从-1.2开始流动，note也从这时开始移动。当流动到0的时候，音乐开始播放。并且之后的所有note都用currentTime与GameVar.lastTime比较进行生成。

### Enemy

由于Enemy的功能都有了很大变化，所以我打算重写这一类。

而我打算将这一个类作为所有note的基类，一是增加可读性，二是便于玩家写mod。

类的属性：

| 属性名                   | 释义                         |
| :----------------------- | :--------------------------- |
| dire                     | 方向（或者你可以叫做“种类”） |
| mode                     | 所属的模式                   |
| time                     | 生成的时间                   |
| distance = 335           |                              |
| speed = 1                |                              |
| delay = distance / speed |                              |
| movement = None          | 运动轨迹                     |
|                          |                              |
|                          |                              |

### Movement

上个类的提到了一个东西，叫做”movement“（运动轨迹）。为什么这么写？因为一个note可以有多种运动方式，包括但不限于直线运动、曲线、或者在速度上的线性和非线性，所以直接在一个类里写。

| 属性名                                   | 释义                                                         |
| ---------------------------------------- | ------------------------------------------------------------ |
| startPos                                 |                                                              |
| endPos                                   |                                                              |
| speedType = "linear"、"nonlinear"        | 速度的种类。线性、非线性。                                   |
| speedValue = ()                          | 对于速度的值。对于线性是个int，对于非线性是个贝塞尔曲线。    |
| moveType = "line"、"quadratic"、"circle" | 移动的种类。直线、二次函数、圆。                             |
| moveValue = ()                           | 对于除了直线的移动种类补充的值。（对于二次函数是第三个点，对于圆是半径和角度） |
|                                          |                                                              |
|                                          |                                                              |
|                                          |                                                              |



### EnemyControl

由于我继续要在主游戏里完成这些，也需要在indexDesigner中完成预览功能，所以我希望这两个地方代码能互通，并且很方便的开启游戏。

首先，是类的属性。

| 属性名                  | 解释                                    |
| ----------------------- | :-------------------------------------- |
| enemies = []            | list 存储enemy对象                      |
| enemyData = []          | list 存储文档Enemy数据                  |
| distance = 335          | int(pixel) 从生成的地方到判子的默认距离 |
| speed = 1               | int(pixel / s) 默认速度                 |
| time = distance / speed | 默认时间延时                            |
| canvas = canvas         | 画布（传参）                            |

类的方法

| 方法名           | 解释               |
| ---------------- | ------------------ |
| load()           | 加载Enemy数据      |
| spawn()          | 生成Enemy          |
| draw()           | 渲染Enemy          |
| step()           | 移动Enemy          |
| check(list DMs)  | 检测Enemy          |
| deadAnimations() | 播放Enemy消除动画  |
| delete()         | 删除Enemy          |
| reset()          | 重置游戏（初始化） |
| main()           | 主函数             |

### JudgeControl

当然，我们还需要一个类来控制各个判子

属性：

| 属性名         | 解释               |
| -------------- | ------------------ |
| DMcomp = []    | 用列表存储判子     |
| judgeData = [] | 文档关于判子的数据 |

方法：



### GameControl

为了进一步简化代码，我将把整个游戏封装在该类中。

属性：

| 属性名                                        | 解释             |
| --------------------------------------------- | ---------------- |
| self.canvas = canvas                          | 画布（传参）     |
| self.enemyControl = EnemyControl(self.canvas) | EnemyControl实例 |
| self.mode                                     | 模式的名字       |
|                                               |                  |
|                                               |                  |
|                                               |                  |
|                                               |                  |
|                                               |                  |
|                                               |                  |

