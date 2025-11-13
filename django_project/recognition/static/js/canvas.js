// Canvas绘图功能
const canvas = document.getElementById('drawCanvas');
const ctx = canvas.getContext('2d');
let isDrawing = false;
let lastX = 0;
let lastY = 0;

// 设置画布样式
ctx.strokeStyle = '#000';
ctx.lineWidth = 15;
ctx.lineCap = 'round';
ctx.lineJoin = 'round';

// 初始化画布为白色
ctx.fillStyle = '#fff';
ctx.fillRect(0, 0, canvas.width, canvas.height);

// 鼠标事件
canvas.addEventListener('mousedown', startDrawing);
canvas.addEventListener('mousemove', draw);
canvas.addEventListener('mouseup', stopDrawing);
canvas.addEventListener('mouseout', stopDrawing);

// 触摸事件
canvas.addEventListener('touchstart', handleTouchStart);
canvas.addEventListener('touchmove', handleTouchMove);
canvas.addEventListener('touchend', stopDrawing);

function startDrawing(e) {
    isDrawing = true;
    [lastX, lastY] = [e.offsetX, e.offsetY];
}

function draw(e) {
    if (!isDrawing) return;
    
    ctx.beginPath();
    ctx.moveTo(lastX, lastY);
    ctx.lineTo(e.offsetX, e.offsetY);
    ctx.stroke();
    
    [lastX, lastY] = [e.offsetX, e.offsetY];
}

function stopDrawing() {
    isDrawing = false;
}

function handleTouchStart(e) {
    e.preventDefault();
    const touch = e.touches[0];
    const rect = canvas.getBoundingClientRect();
    lastX = touch.clientX - rect.left;
    lastY = touch.clientY - rect.top;
    isDrawing = true;
}

function handleTouchMove(e) {
    if (!isDrawing) return;
    e.preventDefault();
    
    const touch = e.touches[0];
    const rect = canvas.getBoundingClientRect();
    const x = touch.clientX - rect.left;
    const y = touch.clientY - rect.top;
    
    ctx.beginPath();
    ctx.moveTo(lastX, lastY);
    ctx.lineTo(x, y);
    ctx.stroke();
    
    [lastX, lastY] = [x, y];
}

// 清除画布
document.getElementById('clearBtn').addEventListener('click', () => {
    ctx.fillStyle = '#fff';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    clearResult();
});

// 识别按钮
document.getElementById('recognizeBtn').addEventListener('click', () => {
    const imageData = canvas.toDataURL('image/png');
    recognizeImage(imageData);
});

// Tab切换
document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        const tabName = btn.dataset.tab;
        
        // 切换按钮状态
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        
        // 切换内容
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.remove('active');
        });
        document.getElementById(`${tabName}-tab`).classList.add('active');
        
        clearResult();
    });
});

// 文件上传
const fileInput = document.getElementById('fileInput');
const uploadArea = document.getElementById('uploadArea');
const previewImage = document.getElementById('previewImage');

uploadArea.addEventListener('click', () => {
    fileInput.click();
});

uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.style.background = '#f0f4ff';
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.style.background = 'white';
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.style.background = 'white';
    
    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {
        handleFileSelect(file);
    }
});

fileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        handleFileSelect(file);
    }
});

function handleFileSelect(file) {
    const reader = new FileReader();
    reader.onload = (e) => {
        previewImage.src = e.target.result;
        previewImage.style.display = 'block';
        uploadArea.style.display = 'none';
    };
    reader.readAsDataURL(file);
}

document.getElementById('uploadBtn').addEventListener('click', () => {
    const file = fileInput.files[0];
    if (!file) {
        showError('请先选择图片');
        return;
    }
    
    const formData = new FormData();
    formData.append('image_file', file);
    
    fetch('/predict/', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            displayResult(data);
        } else {
            showError('识别失败: ' + data.error);
        }
    })
    .catch(error => {
        showError('请求失败: ' + error);
    });
});

// 识别图片
function recognizeImage(imageData) {
    const formData = new FormData();
    formData.append('image_data', imageData);
    
    fetch('/predict/', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            displayResult(data);
        } else {
            showError('识别失败: ' + data.error);
        }
    })
    .catch(error => {
        showError('请求失败: ' + error);
    });
}

// 显示结果
function displayResult(data) {
    // 移除错误提示（如果存在）
    const errorDiv = document.getElementById('errorMessage');
    if (errorDiv) {
        errorDiv.remove();
    }
    
    document.getElementById('predictedDigit').textContent = data.digit;
    document.getElementById('confidenceValue').textContent =
        (data.confidence * 100).toFixed(2) + '%';
    
    // 显示概率分布
    const probabilityBars = document.getElementById('probabilityBars');
    probabilityBars.innerHTML = '';
    
    data.probabilities.forEach((prob, index) => {
        const probItem = document.createElement('div');
        probItem.className = 'prob-item';
        
        const label = document.createElement('span');
        label.className = 'prob-label';
        label.textContent = index;
        
        const barContainer = document.createElement('div');
        barContainer.className = 'prob-bar-container';
        
        const bar = document.createElement('div');
        bar.className = 'prob-bar';
        bar.style.width = (prob * 100) + '%';
        bar.textContent = (prob * 100).toFixed(1) + '%';
        
        barContainer.appendChild(bar);
        probItem.appendChild(label);
        probItem.appendChild(barContainer);
        probabilityBars.appendChild(probItem);
    });
}

// 清除结果显示
function clearResult() {
    document.getElementById('predictedDigit').textContent = '-';
    document.getElementById('confidenceValue').textContent = '-';
    document.getElementById('probabilityBars').innerHTML = '';
    
    // 移除错误提示（如果存在）
    const errorDiv = document.getElementById('errorMessage');
    if (errorDiv) {
        errorDiv.remove();
    }
}

// 显示错误信息
function showError(message) {
    // 清除当前结果
    clearResult();
    
    // 创建或更新错误提示
    let errorDiv = document.getElementById('errorMessage');
    if (!errorDiv) {
        errorDiv = document.createElement('div');
        errorDiv.id = 'errorMessage';
        errorDiv.style.cssText = 'background: #fee; border: 2px solid #f88; border-radius: 10px; padding: 20px; text-align: center; color: #c33; margin: 20px 0;';
        document.getElementById('resultDisplay').appendChild(errorDiv);
    }
    
    errorDiv.textContent = '❌ ' + message;
    errorDiv.style.display = 'block';
    
    // 3秒后自动隐藏错误信息
    setTimeout(() => {
        errorDiv.style.display = 'none';
    }, 3000);
}