"""
MNIST CNN模型定义
"""
import torch
import torch.nn as nn
import torch.nn.functional as F


class MNISTNet(nn.Module):
    """MNIST卷积神经网络"""
    
    def __init__(self):
        super(MNISTNet, self).__init__()
        # 第一层卷积: 1 -> 32 channels
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, padding=1)
        # 第二层卷积: 32 -> 64 channels
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        # 池化层
        self.pool = nn.MaxPool2d(2, 2)
        # 全连接层
        self.fc1 = nn.Linear(64 * 7 * 7, 128)
        self.fc2 = nn.Linear(128, 10)
        # Dropout
        self.dropout = nn.Dropout(0.5)
    
    def forward(self, x):
        # 第一层: 卷积 -> ReLU -> 池化
        x = self.pool(F.relu(self.conv1(x)))
        # 第二层: 卷积 -> ReLU -> 池化
        x = self.pool(F.relu(self.conv2(x)))
        # 展平
        x = x.view(-1, 64 * 7 * 7)
        # 全连接层
        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.fc2(x)
        return x


def load_model(model_path, device='cpu'):
    """加载训练好的模型"""
    model = MNISTNet()
    try:
        model.load_state_dict(torch.load(model_path, map_location=device))
        model.to(device)
        model.eval()
        return model
    except FileNotFoundError:
        print(f"模型文件未找到: {model_path}")
        print("请先训练模型或将模型文件放置在正确位置")
        return None