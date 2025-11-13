# 项目打包与部署指南

## ✅ 能否直接打包运行？

**答案：可以！** 但需要满足以下条件：

---

## 📦 打包前的检查清单

### 必需文件清单

✅ **必须包含的文件**：
```
源代码/
├── main.py                          ✅ 程序入口
├── requirements.txt                 ✅ 依赖列表
├── environment_gpu.yml              ✅ GPU环境配置
├── environment.yml                  ✅ CPU环境配置
├── README.md                        ✅ 使用说明
│
├── setup_windows.bat                ✅ 安装脚本
├── setup_gpu.bat                    ✅ GPU安装脚本
│
├── django_project/                  ✅ Django项目
│   ├── manage.py
│   ├── mnist_project/
│   └── recognition/
│
└── models/
    ├── train_model.py               ✅ 训练脚本
    └── mnist_cnn.pth                ⚠️ 需要先训练生成
```

⚠️ **可选但建议包含**：
- `models/mnist_cnn.pth` - 训练好的模型（避免重新训练）
- `models/data/` - MNIST数据集（避免重新下载）
- 所有文档文件（.md文件）

❌ **不需要包含**：
- `django_project/db.sqlite3` - 数据库（会自动生成）
- `__pycache__/` - Python缓存
- `.pyc` 文件
- `models/data/` - MNIST数据（如果网络好可以重新下载）

---

## 🚀 三种部署方案

### 方案1: 完整打包（推荐）

**适用场景**：迁移到其他Windows电脑

#### 步骤1: 打包项目

```bash
# 在当前项目根目录
# 复制整个项目文件夹
源代码/ → 复制到USB或网盘
```

#### 步骤2: 在新电脑上部署

```bash
# 1. 复制项目到新电脑
# 2. 确保安装了Anaconda
# 3. 打开Anaconda Prompt，进入项目目录

# 4. 如果有GPU，运行:
setup_gpu.bat

# 如果只有CPU，运行:
setup_windows.bat

# 5. 激活环境
conda activate mnist_env_gpu  # 或 mnist_env

# 6. 如果包含了模型文件，直接启动
python main.py

# 7. 如果没有模型文件，先训练
cd models
python train_model.py
cd ..
python main.py
```

#### 优点
- ✅ 完全离线运行（如果包含模型和数据）
- ✅ 配置简单
- ✅ 一键安装

#### 缺点
- ❌ 需要目标机器有相同的操作系统（Windows）
- ❌ 需要安装Anaconda

---

### 方案2: 轻量打包（不含模型）

**适用场景**：网络环境好，目标机器配置不同

#### 打包内容
```
源代码/
├── main.py
├── requirements.txt
├── environment_gpu.yml
├── setup_gpu.bat
├── README.md
├── django_project/
└── models/
    └── train_model.py  # 不包含.pth和data/
```

#### 部署步骤
```bash
# 1. 安装环境
setup_gpu.bat

# 2. 激活环境
conda activate mnist_env_gpu

# 3. 训练模型（首次需要下载MNIST数据集）
cd models
python train_model.py

# 4. 启动应用
cd ..
python main.py
```

#### 优点
- ✅ 文件体积小（几MB vs 几百MB）
- ✅ 适应不同硬件配置

#### 缺点
- ❌ 首次需要联网下载数据集
- ❌ 需要等待模型训练（2-15分钟）

---

### 方案3: Docker打包（跨平台）

**适用场景**：Linux服务器部署，或需要跨平台

#### 创建Dockerfile

```dockerfile
# Dockerfile
FROM python:3.10-slim

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /app

# 复制项目文件
COPY requirements.txt .
COPY main.py .
COPY django_project/ django_project/
COPY models/ models/

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["python", "main.py"]
```

#### 构建和运行

```bash
# 构建镜像
docker build -t mnist-recognition .

# 运行容器
docker run -p 8000:8000 mnist-recognition
```

#### 优点
- ✅ 跨平台（Windows/Linux/macOS）
- ✅ 环境完全隔离
- ✅ 易于部署到云服务器

#### 缺点
- ❌ 需要Docker环境
- ❌ GPU支持需要NVIDIA Docker

---

## 📋 部署前的准备工作

### 1. 检查模型文件

```bash
# 检查模型是否存在
dir models\mnist_cnn.pth  # Windows
ls models/mnist_cnn.pth   # Linux/Mac
```

如果不存在，先训练：
```bash
cd models
python train_model.py
```

### 2. 测试项目完整性

```bash
# 激活环境
conda activate mnist_env_gpu

# 测试导入
python -c "import torch; import django; print('环境正常')"

# 测试模型加载
python -c "from django_project.recognition.ml_model import load_model; model = load_model('models/mnist_cnn.pth'); print('模型加载成功')"
```

### 3. 清理不必要的文件

```bash
# 删除Python缓存
del /s /q __pycache__        # Windows
find . -type d -name __pycache__ -exec rm -r {} +  # Linux/Mac

# 删除.pyc文件
del /s /q *.pyc              # Windows
find . -name "*.pyc" -delete # Linux/Mac
```

---

## 🎯 快速部署流程

### 目标：从零到运行（新电脑）

```bash
# === 第1步：复制项目 ===
# 将整个"源代码"文件夹复制到新电脑

# === 第2步：安装Anaconda ===
# 下载并安装Anaconda (如果还没有)
# https://www.anaconda.com/download

# === 第3步：配置环境 ===
# 打开 Anaconda Prompt，进入项目目录
cd 你的项目路径\源代码

# 运行安装脚本
setup_gpu.bat      # 如果有GPU
# 或
setup_windows.bat  # 如果只有CPU

# === 第4步：启动项目 ===
conda activate mnist_env_gpu
python main.py

# === 第5步：访问应用 ===
# 浏览器打开: http://127.0.0.1:8000
```

**预计时间**：
- 有模型文件：5-10分钟
- 无模型文件：15-25分钟（包含训练）

---

## ⚠️ 常见问题

### Q1: 在新电脑上运行报错？

**A**: 按顺序检查：
1. 是否安装了Anaconda？
2. 是否激活了正确的环境？
3. 是否有`mnist_cnn.pth`模型文件？
4. 运行 `fix_torch_compatibility.bat` 修复依赖

### Q2: 模型文件很大吗？

**A**: 
- 模型文件 (`mnist_cnn.pth`): ~5MB
- MNIST数据集 (`models/data/`): ~50MB
- 总计：~55MB

### Q3: 能在没有GPU的电脑上运行吗？

**A**: 可以！
```bash
# 使用CPU环境
setup_windows.bat
conda activate mnist_env
python main.py
```
只是训练和推理会慢一些。

### Q4: 能在Linux/Mac上运行吗？

**A**: 可以！
```bash
# 给脚本添加执行权限
chmod +x setup_unix.sh

# 运行安装
./setup_unix.sh

# 启动项目
conda activate mnist_env
python main.py
```

### Q5: 不想安装Anaconda，能用pip吗？

**A**: 可以！
```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 启动项目
python main.py
```

---

## 📊 打包大小参考

| 内容 | 大小 | 必需 |
|------|------|------|
| 源代码（不含模型） | ~5MB | ✅ 是 |
| 训练好的模型 | ~5MB | ⚠️ 推荐 |
| MNIST数据集 | ~50MB | ❌ 可选 |
| 文档文件 | ~1MB | ❌ 可选 |
| **总计（完整）** | **~61MB** | - |
| **总计（最小）** | **~5MB** | - |

---

## 🔒 安全建议

### 生产环境部署

如果要部署到公网服务器，需要修改：

1. **修改SECRET_KEY**
```python
# django_project/mnist_project/settings.py
SECRET_KEY = '生成一个新的随机密钥'
```

2. **关闭DEBUG模式**
```python
DEBUG = False
```

3. **限制ALLOWED_HOSTS**
```python
ALLOWED_HOSTS = ['your-domain.com', '你的IP地址']
```

4. **使用生产级服务器**
```bash
pip install gunicorn
gunicorn mnist_project.wsgi:application --bind 0.0.0.0:8000
```

---

## ✅ 打包检查清单

部署前确认：

- [ ] 所有必需文件都已包含
- [ ] 模型文件存在（或准备重新训练）
- [ ] README.md包含完整的使用说明
- [ ] 测试过能正常启动
- [ ] 清理了__pycache__和.pyc文件
- [ ] 更新了requirements.txt（如果有新依赖）

---

## 🎁 一键打包脚本

### Windows打包脚本

创建 `package.bat`:
```batch
@echo off
echo 正在打包项目...

REM 清理缓存
del /s /q __pycache__ 2>nul
del /s /q *.pyc 2>nul

REM 创建打包目录
mkdir release
xcopy /E /I /Y *.* release\
xcopy /E /I /Y django_project release\django_project\
xcopy /E /I /Y models release\models\

echo 打包完成！
echo 打包文件位于: release\
pause
```

---

**总结**: 您的项目可以直接打包到其他电脑运行！只需要：
1. 复制整个项目文件夹
2. 在新电脑上安装Anaconda
3. 运行 `setup_gpu.bat` 或 `setup_windows.bat`
4. 执行 `python main.py`

最简单的方式就是把整个"源代码"文件夹打包，确保包含`models/mnist_cnn.pth`模型文件！