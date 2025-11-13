"""
recognition应用路由配置
"""
from django.urls import path
from . import views

app_name = 'recognition'

urlpatterns = [
    path('', views.index, name='index'),
    path('predict/', views.predict, name='predict'),
]