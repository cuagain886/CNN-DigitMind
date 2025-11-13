#!/usr/bin/env python
"""
MNIST手写数字识别Web应用 - 程序入口
启动Django开发服务器
"""
import os
import sys
import subprocess

def main():
    """主函数：启动Django开发服务器"""
    # 设置Django项目路径
    django_project_path = os.path.join(os.path.dirname(__file__), 'django_project')
    
    # 设置Django设置模块
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mnist_project.settings')
    
    # 切换到Django项目目录
    os.chdir(django_project_path)
    
    # 添加Django项目路径到系统路径
    sys.path.insert(0, django_project_path)
    
    # 启动Django开发服务器
    print("=" * 50)
    print("MNIST手写数字识别Web应用")
    print("=" * 50)
    print("正在启动Django开发服务器...")
    print("访问地址: http://127.0.0.1:8000")
    print("按 Ctrl+C 停止服务器")
    print("=" * 50)
    
    # 执行Django runserver命令
    subprocess.run([sys.executable, 'manage.py', 'runserver', '0.0.0.0:8000'])

if __name__ == '__main__':
    main()