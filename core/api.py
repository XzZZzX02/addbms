import core.text.zippy as zippy
import core.image.infer as npr

def detect(filepath: str, filetype: str):
    """
    @param filepath: 要检测的文本/图像的绝对路径
    @param filetype: 要检测的文本/图像的类型, "image": 图像, "text": 文本
    @return str 检测结果
            demo: Real image, probability: 0.0092
                  ('Human', 0.022368848767306826)
"""
    if (filetype == "image"):
        return npr.image_detect(filepath)
    elif (filetype == "text"):
        return zippy.text_detect(filepath)
    else:
        raise ValueError("错误: 错误的文件类型: image/text")