# OSMChina-Zhongli_Tilebox

## 介绍

>
>“帝君这么下载瓦片一定有他的深意”

本项目有以下功能

1. Zhongli_Tilebox.Request

   可以下载指定等级下，固定范围或全图的瓦片（完善中）

2. Zhongli_Tilebox.Combiner

   可以把一堆瓦片合并（在做了）

3. Zhongli_Tilebox.Viewer

   可以直接查看瓦片（在做了）

某种意义上可以看作Universal Map Downloader的开源实现版本

但是我们更有节操，线程限制更好，更少给服务器带来负载

注意：这个项目与[github.com/AMDmi3/tiletool](https://wiki.openstreetmap.org/wiki/Tiletool)不是一回事，但他的功能我们可以学习

## 测试用例

### Requester

```python
taskGenerator(0, "OSMChina", "测试任务S", MODE="Full")
taskGenerator(2, "OSMChina", "测试任务R", 2, 3, 2, 3, MODE="Region")
taskGenerator(3, "OSMChina", "测试任务F", MODE="Full")
```

## TODO

- [ ] UA重做
- [ ] 多组件
    - [x] 多组件-模块化
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

## 承诺

OSMChina承诺

本项目可且仅可用于爬取OSMChina自有的瓦片服务。

不提供对其他非自有瓦片服务的爬取并屏蔽对外来源。

该工具仅用于诊断和调试渲染风格使用。


## 感谢

感谢以下个人或团体在技术上给予我们的指点

此外还应感谢所有使用本项目的用户，用户的支持是我们的动力。

（以下排名不分先后）

+ Python猫