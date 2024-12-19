"""
    其实实现的有点蠢, 还有一步增加临时文件的操作, 可以看到图像检测里已经有了根据base64直接生成pil对象的api,
    但是文本检测里直接读取标准输入流的操作还有点没太弄明白, 为了保持一致性, 这里还是用了临时文件的操作
"""

import base64
import sqlite3
import os
import core.api as api


class Addbms:
    def __init__(self):
        current_directory = os.path.dirname(__file__)
        db_path = os.path.join(current_directory, 'addbms.db')
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS my_table (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            type TEXT NOT NULL,
            result TEXT
        )
        ''')

    def insert(self, content, type):
        """
        插入数据
        @param content: 内容字段
        @param type: 类型字段, 只能是 "image" 或 "text"
        """
        if type not in ["image", "text"]:
            raise ValueError("type must be 'image' or 'text'")
        self.cursor.execute('''
        INSERT INTO my_table content, type)
        VALUES (?, ?)
        ''', (content, type))
        self.conn.commit()

    def delete(self, id):
        """
        根据 id 删除某一条记录
        @param id: 记录的 id
        """
        self.cursor.execute('''
        DELETE FROM my_table
        WHERE id = ?
        ''', (id,))
        self.conn.commit()

    def delete_by_content(self, content):
        """
        根据内容删除某条数据
        :param content: 内容字段（用于匹配）
        """
        self.cursor.execute('''
        DELETE FROM my_table WHERE content = ?
        ''', (content,))
        self.conn.commit()

    def query(self, content):
        """
        查询某一条记录
        :param content: 内容字段（用于匹配）
        :return: 匹配的记录（元组）或 None
        """
        self.cursor.execute('''
        SELECT * FROM my_table WHERE content = ?
        ''', (content,))
        return self.cursor.fetchone()
    
    def query_all(self):
        """
        查询所有记录
        :return: 所有记录（列表）
        """
        self.cursor.execute('''
        SELECT * FROM my_table
        ''')
        return self.cursor.fetchall()
    
    def update(self, id, result):
        """
        更新某一条记录
        :param id: 记录的 id
        :param result: 结果字段
        """
        self.cursor.execute('''
        UPDATE my_table
        SET result = ?
        WHERE id = ?
        ''', (result, id))
        self.conn.commit()

    def close(self):
        """
        关闭数据库连接
        """
        self.cursor.close()
        self.conn.close()

    def __del__(self):
        self.close()

    def detect(self, id):
        """
        根据 id 检测内容
        :param id: 记录的 id
        """
        content = self.query(id)[1]
        type = self.query(id)[2]
        result = None
        if (type == "image"):
            result =  self.detect_image(content)
        elif (type == "text"):
            result =  self.detect_text(content)
        else:
            raise ValueError("type must be 'image' or 'text'")
        self.update(id, result)
    
    def detect_image(self, content):
        """
        根据 id 检测图片内容
        :param id: 记录的 id
        """
        image_base64 = content
        if image_base64 is None:
            raise ValueError("image_base64 is None")
        # 将 Base64 字符串解码为二进制数据
        binary_data = base64.b64decode(image_base64)

        # 获取当前工作目录的绝对路径
        current_directory = os.getcwd()
        # 拼接文件路径
        image_path = os.path.join(current_directory, "output_image.jpg")
        # 保存为图像文件
        with open(image_path, "wb") as image_file:
            image_file.write(binary_data)
        result = api.detect_image(image_path)
        os.remove(image_path)
        return result

    def detect_text(self, content):
        """
        根据 id 检测文本内容
        :param id: 记录的 id
        """
        text = content
        if text is None:
            raise ValueError("content is None")
        # 获取当前工作目录的绝对路径
        current_directory = os.getcwd()
        text_path = os.path.join(current_directory, "output_text.txt")
        with open(text_path, "w") as text_file:
            text_file.write(text)
        result = api.detect_text("output_text.txt")
        os.remove(text_path)
        return result