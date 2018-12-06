from django.urls import path
from . import views

urlpatterns = [
    path('', views.bilibili_video_home, name = 'bilibili-video-home'),
    path('upInfo/', views.bilibili_upInfo_home, name = 'bilibili-UpInfo-home'),
]