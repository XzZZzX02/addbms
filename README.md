# 生成式人工智能多模态内容识别
addbms -- AI-generated Detector Database Management Software 

## 概述

本系统旨在帮助应用人员自动判断输入的多模态内容（包括图像、视频、语音、文本等）是否由生成式人工智能（AIGC）生成。系统提供数据录入、内容识别、批量化处理等功能，并支持可视化结果展示。

## 项目结构
```
addbms
├── README.md
├── core
│   ├── __init__.py
│   ├── api.py  提供检测的统一api
│   ├── image   图像检测
│   │   ├── NPR.pth     模型
│   │   ├── __init__.py
│   │   ├── infer.py    图像检测主类
│   │   ├── util.py
│   │   ├── networks
│   │   └── options
│   └── text    文本检测
│       ├── __init__.py
│       ├── ai-generated.txt
│       └── zippy.py    文本检测主类
├── database
│   ├── __init__.py
│   └── db.py   数据库接口类
├── gui     未来会有的
└── test.py
```
## 系统架构

系统分为以下几个主要模块：

- **数据管理模块 (db.py)**: 负责数据的存储、查询、删除等操作。
- **文本检测模块 (zippy.py)**: 使用压缩算法判断文本内容是否由AI生成。
- **图像检测模块 (infer.py, resnet.py, trainer.py)**: 使用预训练的ResNet模型判断图像内容是否由AI生成。
- **API接口模块 (api.py)**: 提供统一的接口供外部调用。
- **工具模块 (util.py, base_options.py, test_options.py, train_options.py)**: 提供一些通用工具函数和模型训练/测试选项配置。

## 模块设计

### 数据管理模块(db.py)

#### 功能概述

- 管理多模态数据的存储和查询。
- 支持插入、删除、查询数据记录。
- 支持数据真伪检测结果的更新。

#### 数据库设计

表结构：

- `id`：主键，自增。
- `content`：数据内容，以文本形式存储（图像数据以Base64编码）。
- `type`：数据类型，如`image`, `text`。
- `result`：检测结果。

#### 关键函数

`insert(content, type)`：插入数据记录。

`delete(id)`：删除指定记录。

`query(id)`：查询指定记录。

`update(id, result)`：更新检测结果。

### 文本检测模块(zippy.py)

使用开源库[zippy](https://github.com/thinkst/zippy)对本内容进行检测。

#### 功能概述

- 使用压缩算法判断文本内容是否由AI生成。
- 支持Brotli，Zlib，LZMA等多种压缩算法。

#### 关键函数

`text_detect(text_path)`：读取文本文件并进行检测。

`BrotliLlmDetector`, `ZlibLlmDetector`, `LzmaLlmDetector`：不同压缩算法的检测器类。

### 图像检测模块(infer.py, resnet.py, trainer.py)

使用开源库[NPR](https://github.com/chuangchuangtan/NPR-DeepfakeDetection)对图像内容进行检测。

#### 功能概述

- 使用预训练的ResNet模型判断图像内容是否由AI生成。
- 支持模型的训练、测试和加载。

#### 关键函数

`image_detect(image_path)`: 读取图像文件并进行检测。

`Trainer`类: 模型训练和推理的基类。

`resnet50`类: 定义ResNet50模型结构。

### API接口模块 (api.py)

#### 功能概述

提供统一的接口供外部调用，进行多模态内容的真伪检测。

#### 关键函数

`detect(filepath, filetype)`: 根据文件类型调用相应的检测模块进行检测。

## 系统流程

1. **数据录入**:

   用户将多模态数据输入系统，数据以特定格式存储在数据库中。

2. **数据识别**:

   - 系统根据数据类型调用相应的检测模块进行真伪判断。
   - 检测结果存储在数据库中，并进行可视化展示。

3. **批量化处理**:

   - 支持批量选择数据进行识别，结果统一展示。

## 接口说明

供GUI调用的接口主要由db.py提供, 调用时遵循标准的调用过程   
1. 初始化数据库

   ```python
   import database.db
   
   # 初始化数据库示例，创建并连接数据库，如果表不存在则创建表
   addbms = Addbms()
   ```

   提供了所有的数据库相关接口并加载数据库，应该在GUI被加载之初就进行实例化

2. 插入数据

   ```python
   # 已经获得了数据库实例， 需指明内容的类型
   addbms.insert(content, type)
   ```

   将要检测的内容插入数据库，与检测api分离，可以设计"插入并检测"的按钮，应该在插入后立即更新GUI中与数据库相关的控件

3. 删除数据

   ```python
   # 根据记录id删除
   addbms.delete(id)
   # 根据内容删除
   addbms.delete_by_content(content)
   ```

4. 查询数据

   ```python
   # 查询单条
   addbms.query(content)
   # 查询所有
   addbms.query_all()
   ```

   返回记录对应的元组`(id, content, type, result)`

5. 检测数据

   ```python
   # 提供记录id，接口本身对类型进行封装，无需指定类型，检测后应该立即更新记录
   addbms.detect(id)
   ```

   目前`update`只支持更新result

## GUI设计

(也许应该有张示例图)

* 数据库显示表单

* 插入文本按钮：直接输入文本并插入

* 插入图像按钮：调用本地explorer获取图像，并转为Base64编码并插入

* 检测按钮：支持从数据库表单中获取选中的id并进行检测，应该有全选记录的全选框

* 删除内容按钮

大概就这些？

## TODO LIST

- [ ] GUI！！！
- [ ] 更好看的GUI！
- [ ] 摒弃在创建临时文件式的api调用方式
