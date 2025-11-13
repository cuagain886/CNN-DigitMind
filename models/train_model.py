"""
MNIST模型训练脚本
"""
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
import sys
import os
import numpy as np

# 修复numpy版本兼容性问题
np.ndarray = np.ndarray

# 添加项目路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'django_project'))
from recognition.ml_model import MNISTNet


def train_model(epochs=10, batch_size=64, learning_rate=0.001):
    """训练MNIST模型"""
    
    print('步骤1: 初始化设备...')
    # 设置设备
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f'使用设备: {device}')
    if torch.cuda.is_available():
        print(f'GPU名称: {torch.cuda.get_device_name(0)}')
        print(f'GPU内存: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.2f} GB')
    
    print('\n步骤2: 设置数据预处理...')
    # 数据预处理
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
    ])
    print('数据预处理配置完成')
    
    print('\n步骤3: 加载MNIST数据集...')
    print('正在下载/加载训练数据...')
    train_dataset = datasets.MNIST(
        root='./data',
        train=True,
        download=True,
        transform=transform
    )
    print(f'训练数据加载完成: {len(train_dataset)} 个样本')
    
    print('正在下载/加载测试数据...')
    test_dataset = datasets.MNIST(
        root='./data',
        train=False,
        download=True,
        transform=transform
    )
    print(f'测试数据加载完成: {len(test_dataset)} 个样本')
    
    print('\n步骤4: 创建数据加载器...')
    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=0  # Windows上设置为0避免多进程问题
    )
    print(f'训练数据加载器: {len(train_loader)} 个batch')
    
    test_loader = DataLoader(
        test_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=0
    )
    print(f'测试数据加载器: {len(test_loader)} 个batch')
    
    print('\n步骤5: 初始化模型...')
    model = MNISTNet().to(device)
    print('模型已加载到设备')
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    print('损失函数和优化器配置完成')
    
    print(f'\n步骤6: 开始训练')
    print('=' * 60)
    print(f'训练参数: epochs={epochs}, batch_size={batch_size}, lr={learning_rate}')
    print('=' * 60)
    
    # 训练循环
    for epoch in range(epochs):
        model.train()
        train_loss = 0
        correct = 0
        total = 0
        
        for batch_idx, (data, target) in enumerate(train_loader):
            data, target = data.to(device), target.to(device)
            
            # 前向传播
            optimizer.zero_grad()
            output = model(data)
            loss = criterion(output, target)
            
            # 反向传播
            loss.backward()
            optimizer.step()
            
            # 统计
            train_loss += loss.item()
            _, predicted = output.max(1)
            total += target.size(0)
            correct += predicted.eq(target).sum().item()
            
            if (batch_idx + 1) % 100 == 0:
                print(f'Epoch [{epoch+1}/{epochs}] '
                      f'Batch [{batch_idx+1}/{len(train_loader)}] '
                      f'Loss: {loss.item():.4f} '
                      f'Acc: {100.*correct/total:.2f}%')
        
        # 验证
        model.eval()
        test_loss = 0
        correct = 0
        total = 0
        
        with torch.no_grad():
            for data, target in test_loader:
                data, target = data.to(device), target.to(device)
                output = model(data)
                test_loss += criterion(output, target).item()
                _, predicted = output.max(1)
                total += target.size(0)
                correct += predicted.eq(target).sum().item()
        
        test_accuracy = 100. * correct / total
        print(f'\nEpoch {epoch+1} 完成:')
        print(f'训练损失: {train_loss/len(train_loader):.4f}')
        print(f'测试准确率: {test_accuracy:.2f}%')
        print('=' * 60)
    
    # 保存模型
    model_path = os.path.join(os.path.dirname(__file__), 'mnist_cnn.pth')
    torch.save(model.state_dict(), model_path)
    print(f'\n模型已保存到: {model_path}')
    print(f'最终测试准确率: {test_accuracy:.2f}%')
    
    return model, test_accuracy


if __name__ == '__main__':
    print('MNIST手写数字识别模型训练')
    print('=' * 60)
    train_model(epochs=10, batch_size=64, learning_rate=0.001)