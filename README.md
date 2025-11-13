# MNIST手写数字识别Web应用

基于Django框架和PyTorch深度学习库开发的Web应用，实现MNIST手写数字识别功能。

## 项目特点

- 🎨 **手写板绘制**: 支持鼠标/触摸屏直接绘制数字
- 📤 **图片上传**: 支持上传PNG/JPG格式的数字图片
- 🧠 **深度学习**: 使用PyTorch CNN模型，准确率>98%
- 📊 **可视化结果**: 实时显示预测结果和概率分布
- 🚀 **简单易用**: 一键启动，无需复杂配置

## 技术栈

- **后端**: Django 4.2
- **深度学习**: PyTorch 2.0
- **前端**: HTML5, CSS3, JavaScript
- **数据库**: SQLite

## 项目结构

```
源代码/
├── main.py                      # 程序入口
├── requirements.txt             # 依赖包
├── README.md                    # 项目说明
├── DESIGN.md                    # 设计文档
├── django_project/              # Django项目
│   ├── manage.py
│   ├── mnist_project/           # 项目配置
│   └── recognition/             # 识别应用
│       ├── ml_model.py          # CNN模型定义
│       ├── views.py             # 视图函数
│       ├── utils.py             # 工具函数
│       ├── templates/           # HTML模板
│       └── static/              # 静态文件
└── models/                      # 模型文件
    ├── train_model.py           # 训练脚本
    └── mnist_cnn.pth            # 模型权重(训练后生成)
```

## 快速开始

### 🎮 GPU用户特别说明

如果您有NVIDIA GPU（如CUDA 12.9），强烈推荐使用GPU加速版本：

```bash
# 一键安装GPU环境
setup_gpu.bat

# 或手动安装
conda create -n mnist_env_gpu python=3.10 -y
conda activate mnist_env_gpu
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
pip install Django==4.2.0 Pillow==10.0.0 numpy==1.24.0
```

**GPU优势**: 训练速度提升5-10倍（从12分钟降至2分钟）

详细配置请查看: **[GPU_SETUP.md](GPU_SETUP.md)** 📖

---

### 方式一: 使用Conda环境（推荐）

#### 1. 一键安装（自动配置环境）

**Windows用户**:
```bash
setup_windows.bat
```

**macOS/Linux用户**:
```bash
chmod +x setup_unix.sh
./setup_unix.sh
```

#### 2. 手动安装

```bash
# 创建并激活Conda环境
conda create -n mnist_env python=3.9 -y
conda activate mnist_env

# 安装PyTorch
conda install pytorch torchvision cpuonly -c pytorch -y

# 安装其他依赖
pip install Django==4.2.0 Pillow==10.0.0 numpy==1.24.0
```

或使用environment.yml:
```bash
conda env create -f environment.yml
conda activate mnist_env
```

#### 3. 训练模型（首次使用）

```bash
cd models
python train_model.py
```

训练完成后会在`models/`目录下生成`mnist_cnn.pth`模型文件。

#### 4. 启动应用

```bash
python main.py
```

#### 5. 访问应用

打开浏览器访问: http://127.0.0.1:8000

### 方式二: 使用pip（传统方式）

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 训练模型
cd models
python train_model.py
cd ..

# 3. 启动应用
python main.py

# 4. 访问应用
# 打开浏览器访问: http://127.0.0.1:8000
```

## 📚 详细文档

- **[GPU_SETUP.md](GPU_SETUP.md)** - GPU加速配置指南（CUDA 12.9用户必读）⚡
- **[CONDA_SETUP.md](CONDA_SETUP.md)** - Conda环境配置详细指南
- **[DESIGN.md](DESIGN.md)** - 项目设计文档

## 使用说明

### 手写板模式
1. 在画布上用鼠标绘制数字（0-9）
2. 点击"识别"按钮
3. 查看右侧识别结果

### 图片上传模式
1. 切换到"上传图片"标签
2. 点击或拖拽图片到上传区域
3. 点击"识别图片"按钮
4. 查看识别结果

## 模型信息

### CNN网络架构
- 输入层: 1×28×28 灰度图像
- 卷积层1: 32个3×3卷积核
- 池化层1: 2×2最大池化
- 卷积层2: 64个3×3卷积核
- 池化层2: 2×2最大池化
- 全连接层1: 128个神经元
- 输出层: 10个神经元（0-9数字）

### 训练参数
- 数据集: MNIST (60,000训练 + 10,000测试)
- 优化器: Adam
- 学习率: 0.001
- 批次大小: 64
- 训练轮数: 10
- 目标准确率: >98%

## API接口

### 预测接口

**URL**: `/predict/`

**方法**: POST

**参数**:
- `image_data`: Base64编码的图片数据（手写板）
- `image_file`: 上传的图片文件

**响应**:
```json
{
  "success": true,
  "digit": 5,
  "confidence": 0.9823,
  "probabilities": [0.0001, 0.0002, ..., 0.9823, ...],
  "message": "识别成功"
}
```

## 开发说明

### 目录说明
- `main.py`: 程序入口，启动Django服务器
- `django_project/`: Django项目根目录
- `models/`: 模型训练和权重文件
- `DESIGN.md`: 详细设计文档

### 自定义训练
修改`models/train_model.py`中的参数：
```python
train_model(
    epochs=10,          # 训练轮数
    batch_size=64,      # 批次大小
    learning_rate=0.001 # 学习率
)
```

## 常见问题

**Q: 首次运行提示"模型未加载"？**  
A: 需要先运行`python models/train_model.py`训练模型。

**Q: 识别准确率低？**  
A: 确保绘制的数字清晰、居中，尽量填满画布。

**Q: 如何更换端口？**  
A: 修改`main.py`中的端口号：`subprocess.run([sys.executable, 'manage.py', 'runserver', '0.0.0.0:端口号'])`

## 许可证

MIT License

## 作者

202330451531_饶小峰

## 更新日志

### v1.0.0 (2025-11-12)
- 初始版本发布
- 实现手写板绘制功能
- 实现图片上传功能
- 实现CNN模型训练和预测
- 实现结果可视化展示