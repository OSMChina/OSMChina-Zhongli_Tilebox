# OSMChina-Zhongli_Tilebox

[![Codacy Badge](https://app.codacy.com/project/badge/Grade/09550a3454354189bd3963a89dd0a422)](https://www.codacy.com/gh/OSMChina/OSMChina-Zhongli_Tilebox/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=OSMChina/OSMChina-Zhongli_Tilebox&amp;utm_campaign=Badge_Grade)
<!-- ![FOSSA Status] -->
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
<!-- ![BLACK PYTHON STYLE] -->

## 介绍

>
>“帝君这么下载瓦片一定有他的深意”

本项目有以下功能

1. Zhongli_Tilebox.requester

   可以下载指定等级下，固定范围或全图的瓦片（完善中）

2. Zhongli_Tilebox.combiner

   可以把一堆瓦片合并（在做了）

3. Zhongli_Tilebox.viewer

   可以直接查看瓦片（在做了）

某种意义上可以看作Universal Map Downloader的开源实现版本

但是我们更有节操，线程限制更好，更少给服务器带来负载

注意：这个项目与[github.com/AMDmi3/tiletool](https://wiki.openstreetmap.org/wiki/Tiletool)不是一回事，但他的功能我们可以学习

## 测试用例

### Requester

** 验证下载 **

```python
task_generator(
    task="requester",
    zoom=0,
    tile_name="OSMChina",
    task_name="OSMChina_验证测试任务_" + str(0),
    mode="Full",
    allow_multi_processor=False,
)
```

** 全图下载 **

```python
task_generator(
    task="requester",
    zoom=2,
    tile_name="OSMChina",
    task_name="OSMChina_全图测试任务_" + str(2),
    mode="Full",
    allow_multi_processor=False,
)
```

** 区域下载 **

```python
task_generator(
    task="requester",
    zoom=2,
    tile_name="OSMChina",
    task_name="OSMChina_区域测试任务_" + str(2),
    x_min=2,
    x_max=3,
    y_min=2,
    y_max=3,
    mode="Region",
    allow_multi_processor=False,
)
```

## TODO

- [ ] UA重做
- [ ] 配置文件分离（不用每次改main.py，先检查本地其他文件）
- [ ] 多组件
    - [ ] 多组件-模块化
        - [ ] 多组件-对图片合并模型进行设计，使之允许用ImageMagick/PIL/OpenCV/python=photoshop等多种本地可行的方式合并图片
    - [x] 多组件-数据源分离
    - [ ] 多组件-Combiner
    - [ ] 多组件-Viewer
- [ ] 多线程
    - [x] 能跑
    - [ ] 能稳定高速运行
    - [ ] 线程数自定义
    - [ ] 延迟时间
    - [ ] 遵守服务端对批量下载的控制协议（我们试图创造）
- [ ] 多样化的请求顺序
    - [ ] 多样化的请求顺序（随机压测）
    - [ ] 多样化的请求顺序（中心辐射）
    - [ ] 多样化的请求顺序（多中心同步辐射）
- [ ] 允许重启后继续进度
    - [ ] 专有格式的进度文件
    - [ ] 专有格式的任务文件
    - [ ] 所有组件联动一套项目文件
    - [ ] 引入Grid模式
        - [ ] 支持按照给定子任务作业
        - [ ] 支持自动拆分子任务
- [] 支持多种不同的瓦片索引数
    - [ ] 谷歌格式（https://www.maptiler.com/google-maps-coordinates-tile-bounds-projection）

## 承诺

OSMChina承诺

本项目可且仅可用于爬取OSMChina自有的瓦片服务。我们推荐瓦片提供商基于referer来判断是否属于合法的请求。

不提供对其他非自有瓦片服务的爬取并屏蔽对外来源，同时支持基于瓦片提供商域名和特定apikey的屏蔽，在屏蔽列表中的内容将不允许使用本工具。我们欢迎您将您的服务添加到我们的屏蔽列表中。尽管它并不能绝对安全和绝对避免被绕开。

该工具仅用于诊断和调试渲染风格使用。


## 感谢

感谢以下个人或团体在技术上给予我们的指点

此外还应感谢所有使用本项目的用户，用户的支持是我们的动力。

（以下排名不分先后）

+ Python猫
