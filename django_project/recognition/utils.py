"""
图片预处理工具函数
"""
import torch
from PIL import Image, ImageOps
import numpy as np
import io
import base64


def preprocess_image(image):
    """
    预处理图片用于MNIST模型预测
    
    Args:
        image: PIL Image对象
    
    Returns:
        torch.Tensor: 预处理后的张量 (1, 1, 28, 28)
    """
    # 转换为灰度图
    image = image.convert('L')
    
    # 调整大小为28x28
    image = image.resize((28, 28), Image.LANCZOS)
    
    # 反色处理 (白底黑字 -> 黑底白字)
    image = ImageOps.invert(image)
    
    # 转换为numpy数组并归一化
    img_array = np.array(image, dtype=np.float32) / 255.0
    
    # 转换为PyTorch张量
    img_tensor = torch.from_numpy(img_array)
    
    # 添加batch和channel维度: (1, 1, 28, 28)
    img_tensor = img_tensor.unsqueeze(0).unsqueeze(0)
    
    return img_tensor


def base64_to_image(base64_string):
    """
    将base64字符串转换为PIL Image
    
    Args:
        base64_string: base64编码的图片字符串
    
    Returns:
        PIL.Image: 图片对象
    """
    # 移除data:image/png;base64,前缀
    if ',' in base64_string:
        base64_string = base64_string.split(',')[1]
    
    # 解码base64
    image_data = base64.b64decode(base64_string)
    
    # 转换为PIL Image
    image = Image.open(io.BytesIO(image_data))
    
    return image


def predict_digit(model, image_tensor, device='cpu'):
    """
    使用模型预测数字
    
    Args:
        model: PyTorch模型
        image_tensor: 预处理后的图片张量
        device: 计算设备
    
    Returns:
        tuple: (预测数字, 置信度, 所有类别概率)
    """
    with torch.no_grad():
        image_tensor = image_tensor.to(device)
        outputs = model(image_tensor)
        probabilities = torch.nn.functional.softmax(outputs, dim=1)
        confidence, predicted = torch.max(probabilities, 1)
        
        return (
            predicted.item(),
            confidence.item(),
            probabilities.cpu().numpy()[0].tolist()
        )