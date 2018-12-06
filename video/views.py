from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from .models import Video

import urllib.request
import urllib.error
import urllib

import requests
from bs4 import BeautifulSoup
import time
import datetime
from datetime import datetime
from datetime import timedelta
from html.parser import HTMLParser
from lxml import html
import math
import pandas as pd

from . import biclass
from . import support
from . import bilibili
from . import Usage_of_API
from . import home_view_functions
#from . import tasks


def get_latest_video_info():
    aids = Usage_of_API.get_latestVideoInfo_about_MMQ()
    posts = []
    for aid in aids:
        video = Usage_of_API.extract_video_info(aid)
        print('av号"%s" \t 得分"%s" \t up主"%s" \t up主ID"%s" \t 播放量:%s \t 评论数:%s \t 弹幕数:%s \t 点赞数:%s \t 收藏数:%s \t 硬币数:%s \t 分享数:%s \t 当前排名:%s \t 历史排名:%s' % (video.aid, video.score, video.upName, video.upID, video.guankan, video.commentNumber, video.danmu, video.like, video.shoucang, video.coin, video.share, video.nowRank, video.hisRank))
        video_instance = Video.objects.create(aid=video.aid, score=video.score, upName=video.upName, upID=video.upID, guankan=video.guankan, commentNumber=video.commentNumber, danmu=video.danmu, like=video.like, shoucang=video.shoucang, coin=video.coin, share=video.share, nowRank=video.nowRank, hisRank=video.hisRank)

        obj_latest = Video.objects.filter(aid=aid).order_by('-id')[0]
        obj_count = Video.objects.filter(aid=aid).count()
        if obj_count > 1:
            obj_2ndlast = Video.objects.filter(aid=aid).order_by('-id')[1]
            if obj_count > 6:
                obj_3hr = Video.objects.filter(aid=aid).order_by('-id')[6]
                if obj_count > 48:
                    obj_24hr = Video.objects.filter(aid=aid).order_by('-id')[48]
                    sub_post = {
                        'aid':obj_latest.aid,
                        'score':obj_latest.score,
                        'change_score':obj_latest.score-obj_2ndlast.score,
                        'change_score_3hr':obj_latest.score-obj_3hr.score,
                        'change_score_24hr':obj_latest.score-obj_24hr.score,
                        'upName':obj_latest.upName,
                        'upID':obj_latest.upID,
                        'latest_guankan':obj_latest.guankan,
                        'latest_like':obj_latest.like,
                        'latest_shoucang':obj_latest.shoucang,
                        'latest_coin':obj_latest.coin,
                        'latest_share':obj_latest.share,
                        'latest_commentNumber':obj_latest.commentNumber,
                        'latest_danmu':obj_latest.danmu,
                        'latest_nowRank':obj_latest.nowRank,
                        'latest_hisRank':obj_latest.hisRank,
                        'change_guankan':obj_latest.guankan-obj_2ndlast.guankan,
                        'change_like':obj_latest.like-obj_2ndlast.like,
                        'change_shoucang':obj_latest.shoucang-obj_2ndlast.shoucang,
                        'change_coin':obj_latest.coin-obj_2ndlast.coin,
                        'change_share':obj_latest.share-obj_2ndlast.share,
                        'change_commentNumber':obj_latest.commentNumber-obj_2ndlast.commentNumber,
                        'change_danmu':obj_latest.danmu-obj_2ndlast.danmu,
                        'change_nowRank':obj_latest.nowRank-obj_2ndlast.nowRank,
                        'change_guankan_3hr':obj_latest.guankan-obj_3hr.guankan,
                        'change_like_3hr':obj_latest.like-obj_3hr.like,
                        'change_shoucang_3hr':obj_latest.shoucang-obj_3hr.shoucang,
                        'change_coin_3hr':obj_latest.coin-obj_3hr.coin,
                        'change_share_3hr':obj_latest.share-obj_3hr.share,
                        'change_commentNumber_3hr':obj_latest.commentNumber-obj_3hr.commentNumber,
                        'change_danmu_3hr':obj_latest.danmu-obj_3hr.danmu,
                        'change_nowRank_3hr':obj_latest.nowRank-obj_3hr.nowRank,
                        'change_guankan_24hr':obj_latest.guankan-obj_24hr.guankan,
                        'change_like_24hr':obj_latest.like-obj_24hr.like,
                        'change_shoucang_24hr':obj_latest.shoucang-obj_24hr.shoucang,
                        'change_coin_24hr':obj_latest.coin-obj_24hr.coin,
                        'change_share_24hr':obj_latest.share-obj_24hr.share,
                        'change_commentNumber_24hr':obj_latest.commentNumber-obj_24hr.commentNumber,
                        'change_danmu_24hr':obj_latest.danmu-obj_24hr.danmu,
                        'change_nowRank_24hr':obj_latest.nowRank-obj_24hr.nowRank,
                        'data_posted':obj_latest.data_posted,
                    }
                else:
                    sub_post = {
                        'aid':obj_latest.aid,
                        'score':obj_latest.score,
                        'change_score':obj_latest.score-obj_2ndlast.score,
                        'change_score_3hr':obj_latest.score-obj_3hr.score,
                        'change_score_24hr':obj_latest.score,
                        'upName':obj_latest.upName,
                        'upID':obj_latest.upID,
                        'latest_guankan':obj_latest.guankan,
                        'latest_like':obj_latest.like,
                        'latest_shoucang':obj_latest.shoucang,
                        'latest_coin':obj_latest.coin,
                        'latest_share':obj_latest.share,
                        'latest_commentNumber':obj_latest.commentNumber,
                        'latest_danmu':obj_latest.danmu,
                        'latest_nowRank':obj_latest.nowRank,
                        'latest_hisRank':obj_latest.hisRank,
                        'change_guankan':obj_latest.guankan-obj_2ndlast.guankan,
                        'change_like':obj_latest.like-obj_2ndlast.like,
                        'change_shoucang':obj_latest.shoucang-obj_2ndlast.shoucang,
                        'change_coin':obj_latest.coin-obj_2ndlast.coin,
                        'change_share':obj_latest.share-obj_2ndlast.share,
                        'change_commentNumber':obj_latest.commentNumber-obj_2ndlast.commentNumber,
                        'change_danmu':obj_latest.danmu-obj_2ndlast.danmu,
                        'change_nowRank':obj_latest.nowRank-obj_2ndlast.nowRank,
                        'change_guankan_3hr':obj_latest.guankan-obj_3hr.guankan,
                        'change_like_3hr':obj_latest.like-obj_3hr.like,
                        'change_shoucang_3hr':obj_latest.shoucang-obj_3hr.shoucang,
                        'change_coin_3hr':obj_latest.coin-obj_3hr.coin,
                        'change_share_3hr':obj_latest.share-obj_3hr.share,
                        'change_commentNumber_3hr':obj_latest.commentNumber-obj_3hr.commentNumber,
                        'change_danmu_3hr':obj_latest.danmu-obj_3hr.danmu,
                        'change_nowRank_3hr':obj_latest.nowRank-obj_3hr.nowRank,
                        'change_guankan_24hr':obj_latest.guankan,
                        'change_like_24hr':obj_latest.like,
                        'change_shoucang_24hr':obj_latest.shoucang,
                        'change_coin_24hr':obj_latest.coin,
                        'change_share_24hr':obj_latest.share,
                        'change_commentNumber_24hr':obj_latest.commentNumber,
                        'change_danmu_24hr':obj_latest.danmu,
                        'change_nowRank_24hr':obj_latest.nowRank,
                        'data_posted':obj_latest.data_posted,
                    }
            else:
                sub_post = {
                    'aid':obj_latest.aid,
                    'score':obj_latest.score,
                    'change_score':obj_latest.score-obj_2ndlast.score,
                    'change_score_3hr':obj_latest.score,
                    'change_score_24hr':obj_latest.score,
                    'upName':obj_latest.upName,
                    'upID':obj_latest.upID,
                    'latest_guankan':obj_latest.guankan,
                    'latest_like':obj_latest.like,
                    'latest_shoucang':obj_latest.shoucang,
                    'latest_coin':obj_latest.coin,
                    'latest_share':obj_latest.share,
                    'latest_commentNumber':obj_latest.commentNumber,
                    'latest_danmu':obj_latest.danmu,
                    'latest_nowRank':obj_latest.nowRank,
                    'latest_hisRank':obj_latest.hisRank,
                    'change_guankan':obj_latest.guankan-obj_2ndlast.guankan,
                    'change_like':obj_latest.like-obj_2ndlast.like,
                    'change_shoucang':obj_latest.shoucang-obj_2ndlast.shoucang,
                    'change_coin':obj_latest.coin-obj_2ndlast.coin,
                    'change_share':obj_latest.share-obj_2ndlast.share,
                    'change_commentNumber':obj_latest.commentNumber-obj_2ndlast.commentNumber,
                    'change_danmu':obj_latest.danmu-obj_2ndlast.danmu,
                    'change_nowRank':obj_latest.nowRank-obj_2ndlast.nowRank,
                    'change_guankan_3hr':obj_latest.guankan,
                    'change_like_3hr':obj_latest.like,
                    'change_shoucang_3hr':obj_latest.shoucang,
                    'change_coin_3hr':obj_latest.coin,
                    'change_share_3hr':obj_latest.share,
                    'change_commentNumber_3hr':obj_latest.commentNumber,
                    'change_danmu_3hr':obj_latest.danmu,
                    'change_nowRank_3hr':obj_latest.nowRank,
                    'change_guankan_24hr':obj_latest.guankan,
                    'change_like_24hr':obj_latest.like,
                    'change_shoucang_24hr':obj_latest.shoucang,
                    'change_coin_24hr':obj_latest.coin,
                    'change_share_24hr':obj_latest.share,
                    'change_commentNumber_24hr':obj_latest.commentNumber,
                    'change_danmu_24hr':obj_latest.danmu,
                    'change_nowRank_24hr':obj_latest.nowRank,
                    'data_posted':obj_latest.data_posted,
                }
        else:
            sub_post = {
                'aid':obj_latest.aid,
                'score':obj_latest.score,
                'change_score':obj_latest.score,
                'change_score_3hr':obj_latest.score,
                'change_score_24hr':obj_latest.score,
                'upName':obj_latest.upName,
                'upID':obj_latest.upID,
                'latest_guankan':obj_latest.guankan,
                'latest_like':obj_latest.like,
                'latest_shoucang':obj_latest.shoucang,
                'latest_coin':obj_latest.coin,
                'latest_share':obj_latest.share,
                'latest_commentNumber':obj_latest.commentNumber,
                'latest_danmu':obj_latest.danmu,
                'latest_nowRank':obj_latest.nowRank,
                'latest_hisRank':obj_latest.hisRank,
                'change_guankan':obj_latest.guankan,
                'change_like':obj_latest.like,
                'change_shoucang':obj_latest.shoucang,
                'change_coin':obj_latest.coin,
                'change_share':obj_latest.share,
                'change_commentNumber':obj_latest.commentNumber,
                'change_danmu':obj_latest.danmu,
                'change_nowRank':obj_latest.nowRank,
                'change_guankan_3hr':obj_latest.guankan,
                'change_like_3hr':obj_latest.like,
                'change_shoucang_3hr':obj_latest.shoucang,
                'change_coin_3hr':obj_latest.coin,
                'change_share_3hr':obj_latest.share,
                'change_commentNumber_3hr':obj_latest.commentNumber,
                'change_danmu_3hr':obj_latest.danmu,
                'change_nowRank_3hr':obj_latest.nowRank,
                'change_guankan_24hr':obj_latest.guankan,
                'change_like_24hr':obj_latest.like,
                'change_shoucang_24hr':obj_latest.shoucang,
                'change_coin_24hr':obj_latest.coin,
                'change_share_24hr':obj_latest.share,
                'change_commentNumber_24hr':obj_latest.commentNumber,
                'change_danmu_24hr':obj_latest.danmu,
                'change_nowRank_24hr':obj_latest.nowRank,
                'data_posted':obj_latest.data_posted,
            }

        posts.append(sub_post)
    return posts

posts = get_latest_video_info()
#tasks.task_mail.delay()

def bilibili_video_home(request):
    context = {
        'posts': posts
    }
    return render(request, 'video/bilibili_video_home.html', context)

def bilibili_upInfo_home(request):
    return render(request, 'video/bilibili_upInfo_home.html')

    