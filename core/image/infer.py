import __main__
import sys
import os
import torch
from core.image.networks.resnet import resnet50
from core.image.options.test_options import TestOptions
from PIL import Image
import torchvision.transforms as transforms

def image_detect(image_path: str) -> str:
    # 解析测试选项
    opt = TestOptions().parse(print_options=False)

    # 创建并加载模型
    model = resnet50(num_classes=1)
    opt.model_path = os.path.join(os.path.dirname(__file__) + "/NPR.pth")
    state_dict = torch.load(opt.model_path, map_location='cpu', weights_only="True")

    # 去掉 "module." 前缀
    # 训练时使用了多卡，推理使用单卡，无需module.前缀
    from collections import OrderedDict
    new_state_dict = OrderedDict()
    for k, v in state_dict['model'].items():
        name = k[7:]  # 去掉 "module." 前缀
        new_state_dict[name] = v

    model.load_state_dict(new_state_dict)
    model.cuda()
    model.eval()

    # 定义图片预处理步骤
    transform = transforms.Compose([
        transforms.Resize((224, 224)),  # 根据模型需求调整图片大小
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])  # 使用ResNet默认的归一化参数
    ])

    image = Image.open(image_path).convert('RGB')
    input_tensor = transform(image).unsqueeze(0).cuda()  # 增加批次维度并移动到GPU

    # 进行预测
    with torch.no_grad():
        output = model(input_tensor)
        prob = torch.sigmoid(output).item()  # 获取 sigmoid 概率

    # 输出预测结果
    if prob > 0.5:
        return f'Fake image, probability: {prob:.4f}'
    else:
        return f'Real image, probability: {prob:.4f}'


if __name__ == '__main__':
    # 找到 --image_path 参数及其值
    for i, arg in enumerate(sys.argv):
        if arg == '--image_path' and i+1 < len(sys.argv):
            img_path = sys.argv[i+1]
            # 从 sys.argv 中移除这两个元素
            sys.argv.pop(i+1)
            sys.argv.pop(i)
            break

    img_path = "/home/zzx/cat.jpg"

    print(image_detect(img_path))
