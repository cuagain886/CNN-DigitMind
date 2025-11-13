# MNIST手写数字识别项目 

##  项目概述

**项目名称**: MNIST手写数字识别Web应用  
**项目类型**: 深度学习 + Web应用  
**开发语言**: Python  
**框架**: Django + PyTorch  

---

##  系统环境

### 操作系统
- **系统**: Windows 11
- **架构**: x64
- **Shell**: PowerShell / CMD

### 硬件配置
- **GPU**: NVIDIA GPU (支持CUDA 12.9)
- **CUDA版本**: 12.9
- **CUDA编译器**: Built on Wed_Apr_9_19:29:17_Pacific_Daylight_Time_2025

---

##  Python环境

### Conda环境管理
- **环境管理器**: Anaconda / Miniconda
- **环境名称**: `mnist_env_gpu` (GPU版本) 
- **Python版本**: 3.10 (GPU)

### 当前激活环境
```
conda activate mnist_env_gpu
```

---

##  依赖包版本

### 核心依赖

| 包名 | 版本 | 用途 |
|------|------|------|
| **Python** | 3.10.19 | 编程语言 |
| **PyTorch** | 2.1.0 | 深度学习框架 |
| **torchvision** | 0.16.0 | 计算机视觉库 |
| **torchaudio** | 2.1.0 | 音频处理（依赖） |
| **Django** | 4.2.0 | Web框架 |
| **Pillow** | 10.0.0 | 图像处理 |
| **NumPy** | 1.24.0 | 数值计算 |

---

##  开发工具

### IDE/编辑器
- **VSCode** (推测，基于环境信息)
- **Python扩展**: 已安装

---

##  Web服务器配置

### 开发服务器
- **服务器**: Django内置开发服务器
- **地址**: `0.0.0.0:8000`
- **访问URL**: `http://127.0.0.1:8000`
- **启动方式**: `python main.py`

### 静态文件
- **STATIC_URL**: `/static/`
- **静态文件目录**: `recognition/static/`

### 媒体文件
- **MEDIA_URL**: `/media/`
- **媒体文件目录**: `django_project/media/`

---

##  机器学习环境

### 模型架构
- **模型类型**: CNN (卷积神经网络)
- **输入**: 28x28灰度图像
- **输出**: 10个类别 (0-9数字)

### 模型结构
```
MNISTNet(
  Conv2d(1, 32, kernel_size=3, padding=1)
  ReLU
  MaxPool2d(2, 2)
  Conv2d(32, 64, kernel_size=3, padding=1)
  ReLU
  MaxPool2d(2, 2)
  Linear(3136, 128)
  ReLU
  Dropout(0.5)
  Linear(128, 10)
)
```

### 训练配置
- **数据集**: MNIST (60,000训练 + 10,000测试)
- **优化器**: Adam
- **学习率**: 0.001
- **批次大小**: 64 (CPU) / 256 (GPU推荐)
- **训练轮数**: 10
- **损失函数**: CrossEntropyLoss

---

##  数据流程

### 1. 用户输入
```
手写板绘制 → Canvas → Base64
或
图片上传 → File → PIL Image
```

### 2. 预处理
```
PIL Image → 灰度化 → 28x28 → 反色 → 归一化 → Tensor
```

### 3. 模型推理
```
Tensor → CNN → Softmax → 概率分布
```

### 4. 结果返回
```
JSON {digit, confidence, probabilities} → 前端显示
```

---

## 
