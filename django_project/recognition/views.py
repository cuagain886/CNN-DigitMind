"""
视图函数
"""
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from PIL import Image
import os

from .ml_model import load_model
from .utils import preprocess_image, base64_to_image, predict_digit

# 全局模型变量（单例模式）
_model = None


def get_model():
    """获取模型实例（单例模式）"""
    global _model
    if _model is None:
        model_path = settings.MODEL_PATH
        if os.path.exists(model_path):
            _model = load_model(model_path)
        else:
            print(f"警告: 模型文件不存在 {model_path}")
    return _model


def index(request):
    """主页面"""
    return render(request, 'recognition/index.html')


@csrf_exempt
def predict(request):
    """处理预测请求"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': '仅支持POST请求'})
    
    try:
        # 获取模型
        model = get_model()
        if model is None:
            return JsonResponse({
                'success': False,
                'error': '模型未加载，请先训练模型'
            })
        
        # 获取图片
        image = None
        
        # 方式1: base64数据
        if 'image_data' in request.POST:
            base64_data = request.POST['image_data']
            image = base64_to_image(base64_data)
        
        # 方式2: 上传文件
        elif 'image_file' in request.FILES:
            image_file = request.FILES['image_file']
            image = Image.open(image_file)
        
        if image is None:
            return JsonResponse({
                'success': False,
                'error': '未找到图片数据'
            })
        
        # 预处理图片
        image_tensor = preprocess_image(image)
        
        # 预测
        digit, confidence, probabilities = predict_digit(model, image_tensor)
        
        # 返回结果
        return JsonResponse({
            'success': True,
            'digit': digit,
            'confidence': round(confidence, 4),
            'probabilities': [round(p, 4) for p in probabilities]
        })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'处理错误: {str(e)}'
        })