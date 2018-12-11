from django.urls import path
from . import views

urlpatterns = [
    path('', views.bilibili_video_home, name = 'bilibili-video-home'),
    path('totalRank/', views.bilibili_totalRank_home, name='bilibili-totalRank-home'),
    path('click/', views.bilibili_click_home, name='bilibili-click-home'),
    path('vote/', views.baidu_vote_home, name='baidu-vote-home'),
]