

# MNIST手写数字识别Web应用

基于PyTorch和Django的手写数字识别系统，支持在线手写输入和图片上传识别。

## 功能特性

- 🎨 在线手写板绘制数字
- 📤 支持图片文件上传识别
- 🧠 基于CNN的深度学习模型
- 📊 实时显示识别结果和置信度
- 💻 友好的Web界面

## 技术栈

- **后端**: Django 4.2.0
- **深度学习**: PyTorch 2.1.0
- **前端**: HTML5 Canvas + JavaScript
- **图像处理**: Pillow

## 环境要求

- Python 3.10+
- CUDA (可选，用于GPU加速训练)

## 快速开始

### 1. 安装依赖

| 技术            | 版本            | 用途         |
| --------------- | --------------- | ------------ |
| **Python**      | 3.9-3.10        | 编程语言     |
| **Django**      | 4.2.0           | Web框架      |
| **PyTorch**     | 2.1.0           | 深度学习框架 |
| **torchvision** | 0.16.0          | 计算机视觉库 |
| **NumPy**       | 1.24.0          | 数值计算     |
| **Pillow**      | 10.0.0          | 图像处理     |
| **CUDA**        | 12.1 (兼容12.9) | GPU加速      |

### 2. 训练模型

```bash
python models/train_model.py
```

训练完成后，模型将保存到 `models/mnist_cnn.pth`

### 3. 启动Web应用

```bash
python main.py
```

访问 http://127.0.0.1:8000 使用应用

## 项目结构

```
.
├── main.py                    # 应用入口
├── requirements.txt           # 依赖列表
├── models/
│   ├── train_model.py        # 模型训练脚本
│   └── mnist_cnn.pth         # 训练好的模型
└── django_project/
    ├── manage.py
    ├── mnist_project/        # Django项目配置
    └── recognition/          # 识别应用
        ├── ml_model.py       # 模型定义
        ├── utils.py          # 工具函数
        ├── views.py          # 视图函数
        ├── static/           # 静态文件
        └── templates/        # 模板文件
```

## 使用说明

1. **手写识别**: 在画布上绘制0-9的数字，点击"识别"按钮
2. **上传识别**: 点击"上传图片"选择本地图片文件
3. **清除画布**: 点击"清除"按钮重新绘制

## 模型信息

- **架构**: 卷积神经网络 (CNN)
- **数据集**: MNIST (60,000训练样本 + 10,000测试样本)
- **准确率**: ~99%
- **输入**: 28x28灰度图像
- **输出**: 10个类别的概率分布

