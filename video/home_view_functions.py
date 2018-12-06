from django.shortcuts import render
from django.http import HttpResponse
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

def get_info(flag):
    flag = flag
    while flag == True:
        aid_1 = 36500943
        video1 = Usage_of_API.extract_video_info(aid_1)
        print('av号"%s" \t up主"%s" \t up主ID"%s" \t 播放量:%s \t 评论数:%s \t 弹幕数:%s \t 点赞数:%s \t 收藏数:%s \t 硬币数:%s \t 分享数:%s \t 当前排名:%s \t 历史排名:%s' % (video1.aid, video1.upName, video1.upID, video1.guankan, video1.commentNumber, video1.danmu, video1.like, video1.shoucang, video1.coin, video1.share, video1.nowRank, video1.hisRank))
        video1_dict = biclass.to_video_dict(video1)
        index = [0]
        video1_df = pd.DataFrame(video1_dict,index=index)
        print(video1_df)
        aid_2 = 36946239
        video3 = Usage_of_API.extract_video_info(aid_2)
        time.sleep(10)
        flag = False
        video2 = Usage_of_API.extract_video_info(aid_1)
        video4 = Usage_of_API.extract_video_info(aid_2)
        video2_dict = biclass.to_video_dict(video2)
        index = [0]
        video2_df = pd.DataFrame(video2_dict,index=index)
        print(video2_df)
        video_df = pd.concat([video1_df,video2_df],ignore_index=True)
        video_df['guankan_change'] = 0
        video_df['guankan_change'].iloc[len(video_df)-1] = video_df['guankan'].iloc[len(video_df)-1] - video_df['guankan'].iloc[len(video_df)-2]
        print(video_df)
        video_instance = Video.objects.create(aid=video1.aid, upName=video1.upName, upID=video1.upID, guankan=video1.guankan, commentNumber=video1.commentNumber, danmu=video1.danmu, like=video1.like, shoucang=video1.shoucang, coin=video1.coin, share=video1.share, nowRank=video1.nowRank, hisRank=video1.hisRank, guankan_new=video2.guankan, commentNumber_new=video2.commentNumber, danmu_new=video2.danmu, like_new=video2.like, shoucang_new=video2.shoucang, coin_new=video2.coin, share_new=video2.share, nowRank_new=video2.nowRank, guankan_change=video2.guankan-video1.guankan, commentNumber_change=video2.commentNumber-video1.commentNumber, danmu_change=video2.danmu-video1.danmu, like_change=video2.like-video1.like, shoucang_change=video2.shoucang-video1.shoucang, coin_change=video2.coin-video1.coin, share_change=video2.share-video1.share, nowRank_change=video2.nowRank-video1.nowRank)
        video_instance = Video.objects.create(aid=video3.aid, upName=video3.upName, upID=video3.upID, guankan=video3.guankan, commentNumber=video3.commentNumber, danmu=video3.danmu, like=video3.like, shoucang=video3.shoucang, coin=video3.coin, share=video3.share, nowRank=video3.nowRank, hisRank=video3.hisRank, guankan_new=video4.guankan, commentNumber_new=video4.commentNumber, danmu_new=video4.danmu, like_new=video4.like, shoucang_new=video4.shoucang, coin_new=video4.coin, share_new=video4.share, nowRank_new=video4.nowRank, guankan_change=video4.guankan-video3.guankan, commentNumber_change=video4.commentNumber-video3.commentNumber, danmu_change=video4.danmu-video3.danmu, like_change=video4.like-video3.like, shoucang_change=video4.shoucang-video3.shoucang, coin_change=video4.coin-video3.coin, share_change=video4.share-video3.share, nowRank_change=video4.nowRank-video3.nowRank)
        break

        #for vi in video_df.itertuples():
            #video_ins = Video.objects.create(aid=vi.aid, upName=vi.upName, upID=vi.upID, guankan=vi.guankan, commentNumber=vi.commentNumber, danmu=vi.danmu, like=vi.like, shoucang=vi.shoucang, coin=vi.coin, share=vi.share, nowRank=vi.nowRank, hisRank=vi.hisRank)
