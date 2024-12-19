# 生成式人工智能多模态内容识别
addbms -- AI-generated Detector Database Management Software 
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
