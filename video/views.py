#!/usr/bin/python3.7
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from .models import BaiduVote, LatestVideo, TotalRankVideo, MostClickVideo
#from .models import Video

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

import sys
import csv
import sqlite3

def get_latest_video_info():
    aids = Usage_of_API.get_latestVideoInfo_about_MMQ()
    posts = []
    for aid in aids:
        video = Usage_of_API.extract_video_info(aid)
        print('av号"%s" \t 得分"%s" \t up主"%s" \t up主ID"%s" \t 播放量:%s \t 评论数:%s \t 弹幕数:%s \t 点赞数:%s \t 收藏数:%s \t 硬币数:%s \t 分享数:%s \t 当前排名:%s \t 历史排名:%s' % (video.aid, video.score, video.upName, video.upID, video.guankan, video.commentNumber, video.danmu, video.like, video.shoucang, video.coin, video.share, video.nowRank, video.hisRank))
        #video_instance = Video.objects.create(aid=video.aid, score=video.score, upName=video.upName, upID=video.upID, guankan=video.guankan, commentNumber=video.commentNumber, danmu=video.danmu, like=video.like, shoucang=video.shoucang, coin=video.coin, share=video.share, nowRank=video.nowRank, hisRank=video.hisRank)
        video_instance = LatestVideo.objects.create(aid=video.aid, title=video.title, tid=video.tid, tname=video.tname, date=video.date, duration=video.duration, score=video.score, upName=video.upName, upID=video.upID, guankan=video.guankan, commentNumber=video.commentNumber, danmu=video.danmu, like=video.like, shoucang=video.shoucang, coin=video.coin, share=video.share, nowRank=video.nowRank, hisRank=video.hisRank)

        obj_latest = LatestVideo.objects.filter(aid=aid).order_by('-id')[0]
        obj_count = LatestVideo.objects.filter(aid=aid).count()
        if obj_count > 1:
            obj_2ndlast = LatestVideo.objects.filter(aid=aid).order_by('-id')[1]
            if obj_count > 4:
                obj_4hr = LatestVideo.objects.filter(aid=aid).order_by('-id')[4]
                if obj_count > 24:
                    obj_24hr = LatestVideo.objects.filter(aid=aid).order_by('-id')[24]
                    sub_post = {
                        'aid':obj_latest.aid,
                        'title':obj_latest.title,
                        'tid':obj_latest.tid,
                        'tname':obj_latest.tname,
                        'date':obj_latest.date,
                        'duration':obj_latest.duration,
                        'score':obj_latest.score,
                        'change_score':obj_latest.score-obj_2ndlast.score,
                        'change_score_4hr':obj_latest.score-obj_4hr.score,
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
                        'change_guankan_4hr':obj_latest.guankan-obj_4hr.guankan,
                        'change_like_4hr':obj_latest.like-obj_4hr.like,
                        'change_shoucang_4hr':obj_latest.shoucang-obj_4hr.shoucang,
                        'change_coin_4hr':obj_latest.coin-obj_4hr.coin,
                        'change_share_4hr':obj_latest.share-obj_4hr.share,
                        'change_commentNumber_4hr':obj_latest.commentNumber-obj_4hr.commentNumber,
                        'change_danmu_4hr':obj_latest.danmu-obj_4hr.danmu,
                        'change_nowRank_4hr':obj_latest.nowRank-obj_4hr.nowRank,
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
                        'title':obj_latest.title,
                        'tid':obj_latest.tid,
                        'tname':obj_latest.tname,
                        'date':obj_latest.date,
                        'duration':obj_latest.duration,
                        'score':obj_latest.score,
                        'change_score':obj_latest.score-obj_2ndlast.score,
                        'change_score_4hr':obj_latest.score-obj_4hr.score,
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
                        'change_guankan_4hr':obj_latest.guankan-obj_4hr.guankan,
                        'change_like_4hr':obj_latest.like-obj_4hr.like,
                        'change_shoucang_4hr':obj_latest.shoucang-obj_4hr.shoucang,
                        'change_coin_4hr':obj_latest.coin-obj_4hr.coin,
                        'change_share_4hr':obj_latest.share-obj_4hr.share,
                        'change_commentNumber_4hr':obj_latest.commentNumber-obj_4hr.commentNumber,
                        'change_danmu_4hr':obj_latest.danmu-obj_4hr.danmu,
                        'change_nowRank_4hr':obj_latest.nowRank-obj_4hr.nowRank,
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
                    'title':obj_latest.title,
                    'tid':obj_latest.tid,
                    'tname':obj_latest.tname,
                    'date':obj_latest.date,
                    'duration':obj_latest.duration,
                    'score':obj_latest.score,
                    'change_score':obj_latest.score-obj_2ndlast.score,
                    'change_score_4hr':obj_latest.score,
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
                    'change_guankan_4hr':obj_latest.guankan,
                    'change_like_4hr':obj_latest.like,
                    'change_shoucang_4hr':obj_latest.shoucang,
                    'change_coin_4hr':obj_latest.coin,
                    'change_share_4hr':obj_latest.share,
                    'change_commentNumber_4hr':obj_latest.commentNumber,
                    'change_danmu_4hr':obj_latest.danmu,
                    'change_nowRank_4hr':obj_latest.nowRank,
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
                'title':obj_latest.title,
                'tid':obj_latest.tid,
                'tname':obj_latest.tname,
                'date':obj_latest.date,
                'duration':obj_latest.duration,
                'score':obj_latest.score,
                'change_score':obj_latest.score,
                'change_score_4hr':obj_latest.score,
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
                'change_guankan_4hr':obj_latest.guankan,
                'change_like_4hr':obj_latest.like,
                'change_shoucang_4hr':obj_latest.shoucang,
                'change_coin_4hr':obj_latest.coin,
                'change_share_4hr':obj_latest.share,
                'change_commentNumber_4hr':obj_latest.commentNumber,
                'change_danmu_4hr':obj_latest.danmu,
                'change_nowRank_4hr':obj_latest.nowRank,
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

def get_totalRank_video_info():
    aids = Usage_of_API.get_totalRankVideoInfo_about_MMQ()
    posts = []
    for aid in aids:
        video = Usage_of_API.extract_video_info(aid)
        print('av号"%s" \t 得分"%s" \t up主"%s" \t up主ID"%s" \t 播放量:%s \t 评论数:%s \t 弹幕数:%s \t 点赞数:%s \t 收藏数:%s \t 硬币数:%s \t 分享数:%s \t 当前排名:%s \t 历史排名:%s' % (video.aid, video.score, video.upName, video.upID, video.guankan, video.commentNumber, video.danmu, video.like, video.shoucang, video.coin, video.share, video.nowRank, video.hisRank))
        #video_instance = Video_totalRank.objects.create(aid=video.aid, score=video.score, upName=video.upName, upID=video.upID, guankan=video.guankan, commentNumber=video.commentNumber, danmu=video.danmu, like=video.like, shoucang=video.shoucang, coin=video.coin, share=video.share, nowRank=video.nowRank, hisRank=video.hisRank)
        video_instance = TotalRankVideo.objects.create(aid=video.aid, title=video.title, tid=video.tid, tname=video.tname, date=video.date, duration=video.duration, score=video.score, upName=video.upName, upID=video.upID, guankan=video.guankan, commentNumber=video.commentNumber, danmu=video.danmu, like=video.like, shoucang=video.shoucang, coin=video.coin, share=video.share, nowRank=video.nowRank, hisRank=video.hisRank)

        obj_latest = TotalRankVideo.objects.filter(aid=aid).order_by('-id')[0]
        obj_count = TotalRankVideo.objects.filter(aid=aid).count()
        if obj_count > 1:
            obj_2ndlast = TotalRankVideo.objects.filter(aid=aid).order_by('-id')[1]
            if obj_count > 4:
                obj_4hr = TotalRankVideo.objects.filter(aid=aid).order_by('-id')[4]
                if obj_count > 24:
                    obj_24hr = TotalRankVideo.objects.filter(aid=aid).order_by('-id')[24]
                    sub_post = {
                        'aid':obj_latest.aid,
                        'title':obj_latest.title,
                        'tid':obj_latest.tid,
                        'tname':obj_latest.tname,
                        'date':obj_latest.date,
                        'duration':obj_latest.duration,
                        'score':obj_latest.score,
                        'change_score':obj_latest.score-obj_2ndlast.score,
                        'change_score_4hr':obj_latest.score-obj_4hr.score,
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
                        'change_guankan_4hr':obj_latest.guankan-obj_4hr.guankan,
                        'change_like_4hr':obj_latest.like-obj_4hr.like,
                        'change_shoucang_4hr':obj_latest.shoucang-obj_4hr.shoucang,
                        'change_coin_4hr':obj_latest.coin-obj_4hr.coin,
                        'change_share_4hr':obj_latest.share-obj_4hr.share,
                        'change_commentNumber_4hr':obj_latest.commentNumber-obj_4hr.commentNumber,
                        'change_danmu_4hr':obj_latest.danmu-obj_4hr.danmu,
                        'change_nowRank_4hr':obj_latest.nowRank-obj_4hr.nowRank,
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
                        'title':obj_latest.title,
                        'tid':obj_latest.tid,
                        'tname':obj_latest.tname,
                        'date':obj_latest.date,
                        'duration':obj_latest.duration,
                        'score':obj_latest.score,
                        'change_score':obj_latest.score-obj_2ndlast.score,
                        'change_score_4hr':obj_latest.score-obj_4hr.score,
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
                        'change_guankan_4hr':obj_latest.guankan-obj_4hr.guankan,
                        'change_like_4hr':obj_latest.like-obj_4hr.like,
                        'change_shoucang_4hr':obj_latest.shoucang-obj_4hr.shoucang,
                        'change_coin_4hr':obj_latest.coin-obj_4hr.coin,
                        'change_share_4hr':obj_latest.share-obj_4hr.share,
                        'change_commentNumber_4hr':obj_latest.commentNumber-obj_4hr.commentNumber,
                        'change_danmu_4hr':obj_latest.danmu-obj_4hr.danmu,
                        'change_nowRank_4hr':obj_latest.nowRank-obj_4hr.nowRank,
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
                    'title':obj_latest.title,
                    'tid':obj_latest.tid,
                    'tname':obj_latest.tname,
                    'date':obj_latest.date,
                    'duration':obj_latest.duration,
                    'score':obj_latest.score,
                    'change_score':obj_latest.score-obj_2ndlast.score,
                    'change_score_4hr':obj_latest.score,
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
                    'change_guankan_4hr':obj_latest.guankan,
                    'change_like_4hr':obj_latest.like,
                    'change_shoucang_4hr':obj_latest.shoucang,
                    'change_coin_4hr':obj_latest.coin,
                    'change_share_4hr':obj_latest.share,
                    'change_commentNumber_4hr':obj_latest.commentNumber,
                    'change_danmu_4hr':obj_latest.danmu,
                    'change_nowRank_4hr':obj_latest.nowRank,
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
                'title':obj_latest.title,
                'tid':obj_latest.tid,
                'tname':obj_latest.tname,
                'date':obj_latest.date,
                'duration':obj_latest.duration,
                'score':obj_latest.score,
                'change_score':obj_latest.score,
                'change_score_4hr':obj_latest.score,
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
                'change_guankan_4hr':obj_latest.guankan,
                'change_like_4hr':obj_latest.like,
                'change_shoucang_4hr':obj_latest.shoucang,
                'change_coin_4hr':obj_latest.coin,
                'change_share_4hr':obj_latest.share,
                'change_commentNumber_4hr':obj_latest.commentNumber,
                'change_danmu_4hr':obj_latest.danmu,
                'change_nowRank_4hr':obj_latest.nowRank,
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

def get_click_video_info():
    aids = Usage_of_API.get_clickVideoInfo_about_MMQ()
    posts = []
    for aid in aids:
        video = Usage_of_API.extract_video_info(aid)
        print('av号"%s" \t 得分"%s" \t up主"%s" \t up主ID"%s" \t 播放量:%s \t 评论数:%s \t 弹幕数:%s \t 点赞数:%s \t 收藏数:%s \t 硬币数:%s \t 分享数:%s \t 当前排名:%s \t 历史排名:%s' % (video.aid, video.score, video.upName, video.upID, video.guankan, video.commentNumber, video.danmu, video.like, video.shoucang, video.coin, video.share, video.nowRank, video.hisRank))
        #video_instance = Video_click.objects.create(aid=video.aid, score=video.score, upName=video.upName, upID=video.upID, guankan=video.guankan, commentNumber=video.commentNumber, danmu=video.danmu, like=video.like, shoucang=video.shoucang, coin=video.coin, share=video.share, nowRank=video.nowRank, hisRank=video.hisRank)
        video_instance = MostClickVideo.objects.create(aid=video.aid, title=video.title, tid=video.tid, tname=video.tname, date=video.date, duration=video.duration, score=video.score, upName=video.upName, upID=video.upID, guankan=video.guankan, commentNumber=video.commentNumber, danmu=video.danmu, like=video.like, shoucang=video.shoucang, coin=video.coin, share=video.share, nowRank=video.nowRank, hisRank=video.hisRank)

        obj_latest = MostClickVideo.objects.filter(aid=aid).order_by('-id')[0]
        obj_count = MostClickVideo.objects.filter(aid=aid).count()
        if obj_count > 1:
            obj_2ndlast = MostClickVideo.objects.filter(aid=aid).order_by('-id')[1]
            if obj_count > 4:
                obj_4hr = MostClickVideo.objects.filter(aid=aid).order_by('-id')[4]
                if obj_count > 24:
                    obj_24hr = MostClickVideo.objects.filter(aid=aid).order_by('-id')[24]
                    sub_post = {
                        'aid':obj_latest.aid,
                        'title':obj_latest.title,
                        'tid':obj_latest.tid,
                        'tname':obj_latest.tname,
                        'date':obj_latest.date,
                        'duration':obj_latest.duration,
                        'score':obj_latest.score,
                        'change_score':obj_latest.score-obj_2ndlast.score,
                        'change_score_4hr':obj_latest.score-obj_4hr.score,
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
                        'change_guankan_4hr':obj_latest.guankan-obj_4hr.guankan,
                        'change_like_4hr':obj_latest.like-obj_4hr.like,
                        'change_shoucang_4hr':obj_latest.shoucang-obj_4hr.shoucang,
                        'change_coin_4hr':obj_latest.coin-obj_4hr.coin,
                        'change_share_4hr':obj_latest.share-obj_4hr.share,
                        'change_commentNumber_4hr':obj_latest.commentNumber-obj_4hr.commentNumber,
                        'change_danmu_4hr':obj_latest.danmu-obj_4hr.danmu,
                        'change_nowRank_4hr':obj_latest.nowRank-obj_4hr.nowRank,
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
                        'title':obj_latest.title,
                        'tid':obj_latest.tid,
                        'tname':obj_latest.tname,
                        'date':obj_latest.date,
                        'duration':obj_latest.duration,
                        'score':obj_latest.score,
                        'change_score':obj_latest.score-obj_2ndlast.score,
                        'change_score_4hr':obj_latest.score-obj_4hr.score,
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
                        'change_guankan_4hr':obj_latest.guankan-obj_4hr.guankan,
                        'change_like_4hr':obj_latest.like-obj_4hr.like,
                        'change_shoucang_4hr':obj_latest.shoucang-obj_4hr.shoucang,
                        'change_coin_4hr':obj_latest.coin-obj_4hr.coin,
                        'change_share_4hr':obj_latest.share-obj_4hr.share,
                        'change_commentNumber_4hr':obj_latest.commentNumber-obj_4hr.commentNumber,
                        'change_danmu_4hr':obj_latest.danmu-obj_4hr.danmu,
                        'change_nowRank_4hr':obj_latest.nowRank-obj_4hr.nowRank,
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
                    'title':obj_latest.title,
                    'tid':obj_latest.tid,
                    'tname':obj_latest.tname,
                    'date':obj_latest.date,
                    'duration':obj_latest.duration,
                    'score':obj_latest.score,
                    'change_score':obj_latest.score-obj_2ndlast.score,
                    'change_score_4hr':obj_latest.score,
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
                    'change_guankan_4hr':obj_latest.guankan,
                    'change_like_4hr':obj_latest.like,
                    'change_shoucang_4hr':obj_latest.shoucang,
                    'change_coin_4hr':obj_latest.coin,
                    'change_share_4hr':obj_latest.share,
                    'change_commentNumber_4hr':obj_latest.commentNumber,
                    'change_danmu_4hr':obj_latest.danmu,
                    'change_nowRank_4hr':obj_latest.nowRank,
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
                'title':obj_latest.title,
                'tid':obj_latest.tid,
                'tname':obj_latest.tname,
                'date':obj_latest.date,
                'duration':obj_latest.duration,
                'score':obj_latest.score,
                'change_score':obj_latest.score,
                'change_score_4hr':obj_latest.score,
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
                'change_guankan_4hr':obj_latest.guankan,
                'change_like_4hr':obj_latest.like,
                'change_shoucang_4hr':obj_latest.shoucang,
                'change_coin_4hr':obj_latest.coin,
                'change_share_4hr':obj_latest.share,
                'change_commentNumber_4hr':obj_latest.commentNumber,
                'change_danmu_4hr':obj_latest.danmu,
                'change_nowRank_4hr':obj_latest.nowRank,
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

def get_baiduvote_info():
    baiduvote = Usage_of_API.get_baidu()
    posts = []
    for i in range(len(baiduvote)):
        voteInfo = baiduvote[i]
        name = str(voteInfo.name)
        BaiduVote_instance = BaiduVote.objects.create(name=voteInfo.name, vote=voteInfo.vote)

        obj_latest = BaiduVote.objects.filter(name=name).order_by('-id')[0]
        obj_count = BaiduVote.objects.filter(name=name).count()
        if obj_count > 1:
            obj_2ndlast = BaiduVote.objects.filter(name=name).order_by('-id')[1]
            if obj_count > 4:
                obj_4hr = BaiduVote.objects.filter(name=name).order_by('-id')[4]
                if obj_count > 24:
                    obj_24hr = BaiduVote.objects.filter(name=name).order_by('-id')[24]
                    sub_post = {
                        'name':obj_latest.name,
                        'vote':obj_latest.vote,
                        'change_vote':obj_latest.vote-obj_2ndlast.vote,
                        'change_vote_4hr':obj_latest.vote-obj_4hr.vote,
                        'change_vote_24hr':obj_latest.vote-obj_24hr.vote,
                        'data_posted':obj_latest.data_posted,
                    }
                else:
                    sub_post = {
                        'name':obj_latest.name,
                        'vote':obj_latest.vote,
                        'change_vote':obj_latest.vote-obj_2ndlast.vote,
                        'change_vote_4hr':obj_latest.vote-obj_4hr.vote,
                        'change_vote_24hr':obj_latest.vote,
                        'data_posted':obj_latest.data_posted,
                    }
            else:
                sub_post = {
                    'name':obj_latest.name,
                    'vote':obj_latest.vote,
                    'change_vote':obj_latest.vote-obj_2ndlast.vote,
                    'change_vote_4hr':obj_latest.vote,
                    'change_vote_24hr':obj_latest.vote,
                    'data_posted':obj_latest.data_posted,
                }
        else:
            sub_post = {
                'name':obj_latest.name,
                'vote':obj_latest.vote,
                'change_vote':obj_latest.vote,
                'change_vote_4hr':obj_latest.vote,
                'change_vote_24hr':obj_latest.vote,
                'data_posted':obj_latest.data_posted,
            }

        posts.append(sub_post)
    return posts

#posts = get_latest_video_info()
posts_totalRank = get_totalRank_video_info()
#posts_click = get_click_video_info()

posts_baiduvote = get_baiduvote_info()

def bilibili_video_home(request):
    context = {
        'posts': posts
    }
    return render(request, 'video/bilibili_video_home.html', context)

def bilibili_totalRank_home(request):
    context = {
        'posts': posts_totalRank
    }
    return render(request, 'video/bilibili_totalRank_home.html', context)

def bilibili_click_home(request):
    context = {
        #'posts': Video.objects.all()
        'posts': posts_click
    }
    return render(request, 'video/bilibili_click_home.html', context)

def baidu_vote_home(request):
    context = {
        #'posts': Video.objects.all()
        'posts': posts_baiduvote
    }
    return render(request, 'video/baidu_vote_home.html', context)