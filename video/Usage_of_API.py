import math
from . import bilibili
from . import support
from . import biclass
import requests
from bs4 import BeautifulSoup
import time
import datetime
from html.parser import HTMLParser
from lxml import html

def extract_up_information(aid):
    aid = str(aid)
    url = 'https://www.bilibili.com/video/av'+aid
    header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}
    response = requests.get(url, headers=header)
    response.encoding = 'utf-8'
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    up_name = soup.find('a', class_='name').string
    up_url = 'https:' + soup.find('a', class_='name')['href']
    up_id = str(soup.find('a', class_='name')['href']).split('/')[-1]
    up_data_url = 'https://api.bilibili.com/x/web-interface/card?mid=%s&jsonp=jsonp' % up_id
    response = requests.get(up_data_url, headers=header)
    response.encoding = 'utf-8'
    html = response.json()
    up_isApproved = html['data']['card']['approve']
    up_gender = html['data']['card']['sex']
    up_rank = html['data']['card']['rank']
    up_face = html['data']['card']['face']
    up_DisplayRank = html['data']['card']['DisplayRank']
    up_registration_time = html['data']['card']['regtime']
    up_birthday = html['data']['card']['birthday']
    up_place = html['data']['card']['place']
    up_description = html['data']['card']['description']
    up_attentions = html['data']['card']['attentions']
    up_fans = html['data']['card']['fans']
    up_friend = html['data']['card']['friend']
    up_follow = html['data']['card']['attention']
    up_sign = html['data']['card']['sign']
    up_level = html['data']['card']['level_info']['current_level']
    up_contribute = html['data']['archive_count']
    up_follower = html['data']['follower']
    print('up主"%s" \t up主ID"%s" \t 用户排名"%s" \t 视频排名"%s" \t 投稿数:%s \t 粉丝数:%s \t 关注数:%s \t 级别:%s \t 注册时间:%s \t 简介:%s \t 签名:%s \t 所在地:%s \t 空间地址:%s' % (up_name, up_id, up_rank, up_DisplayRank, up_contribute, up_fans, up_follow, str(up_level), up_registration_time, up_description, up_sign, up_place, up_url))

def extract_user_info_by_mid(mid):
    user = User()
    mid = str(mid)
    url = 'https://api.bilibili.com/x/web-interface/card?mid=%s&jsonp=jsonp' % mid
    header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}
    response = requests.get(url, headers=header)
    response.encoding = 'utf-8'
    html = response.json()
    user.mid = html['data']['card']['mid']
    user.name = html['data']['card']['name']
    #user.isApproved = html['data']['card']['approve']
    #user.sex = html['data']['card']['sex']
    #user.rank = html['data']['card']['rank']
    #user.avatar = html['data']['card']['face']
    #user.DisplayRank = html['data']['card']['DisplayRank']
    #user.place = html['data']['card']['place']
    #user.description = html['data']['card']['description']
    user.fans = html['data']['card']['fans']
    #user.friend = html['data']['card']['friend']
    user.follow = html['data']['card']['attention']
    user.article = html['data']['archive_count']
    #user.message = html['message']
    user.levelInfo = html['data']['card']['level_info']['current_level']
    #user.vipType = html['data']['card']['vip']['vipType']
    url = "https://api.bilibili.com/x/space/upstat?mid=%s" % (mid)
    response = requests.get(url, headers=header)
    response.encoding = 'utf-8'
    html = response.json()
    user.totalVideoView = html['data']['archive']['view']
    user.totalarticleView = html['data']['article']['view']
    return user

def extract_upInfo(aid):
    aid = str(aid)
    url = 'https://www.bilibili.com/video/av'+aid
    header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}
    response = requests.get(url, headers=header)
    response.encoding = 'utf-8'
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    up_name = soup.find('a', class_='name').string
    up_url = 'https:' + soup.find('a', class_='name')['href']
    up_id = str(soup.find('a', class_='name')['href']).split('/')[-1]
    user = extract_user_info_by_mid(up_id)
    return user

def get_user_followingList(mid,page, numberPerPage):
    mid = str(mid)
    page = str(page)
    numberPerPage = str(numberPerPage)
    header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}
    url = "https://api.bilibili.com/x/relation/followings?vmid=%s&pn=%s&ps=%s" % (mid, page, numberPerPage)
    response = requests.get(url, headers=header)
    response.encoding = 'utf-8'
    html = response.json()
    followList_info = html['data']['list']
    user_mid = [x['mid'] for x in followList_info]
    user_name = [x['uname'] for x in followList_info]
    user_mtime = [datetime.datetime.fromtimestamp(x['mtime']).strftime('%Y-%m-%d %H:%M:%S') for x in followList_info]
    user_tag = [x['tag'] for x in followList_info]
    user_avatar = [x['face'] for x in followList_info]
    user_sign = [x['sign'] for x in followList_info]
    numberPerPage = int(numberPerPage)
    followList = [User() for i in range(numberPerPage)]
    for i in range(numberPerPage):
        followList[i].mid = user_mid[i]
        followList[i].name = user_name[i]
        followList[i].mtime = user_mtime[i]
        followList[i].tag = user_tag[i]
        followList[i].avatar = user_avatar[i]
        followList[i].sign = user_sign[i]
    return followList

def get_user_followerList(mid,page, numberPerPage):
    mid = str(mid)
    page = str(page)
    numberPerPage = str(numberPerPage)
    header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}
    url = "https://api.bilibili.com/x/relation/followers?vmid=%s&pn=%s&ps=%s" % (mid, page, numberPerPage)
    response = requests.get(url, headers=header)
    response.encoding = 'utf-8'
    html = response.json()
    followList_info = html['data']['list']
    user_mid = [x['mid'] for x in followList_info]
    user_name = [x['uname'] for x in followList_info]
    user_mtime = [datetime.datetime.fromtimestamp(x['mtime']).strftime('%Y-%m-%d %H:%M:%S') for x in followList_info]
    user_tag = [x['tag'] for x in followList_info]
    user_avatar = [x['face'] for x in followList_info]
    user_sign = [x['sign'] for x in followList_info]
    numberPerPage = int(numberPerPage)
    fansList = [User() for i in range(numberPerPage)]
    for i in range(numberPerPage):
        fansList[i].mid = user_mid[i]
        fansList[i].name = user_name[i]
        fansList[i].mtime = user_mtime[i]
        fansList[i].tag = user_tag[i]
        fansList[i].avatar = user_avatar[i]
        fansList[i].sign = user_sign[i]
    return fansList

def extract_some_comments(aid,page,order):
    aid = aid
    page = page
    order = order
    comment_list = GetComment_v2(aid, page, order)
    comment_length = comment_list.commentLen
    comment = comment_list.comments
    for i in range(len(comment)):
        comment_now = comment[i]
        message = comment_now.msg
        floor = comment_now.lv
        comment_id = math.floor(comment_now.fbid)
        status = comment_now.ad_check
        like = comment_now.like
        user = comment_now.post_user
        user_name = user.name.decode("utf-8")
        user_id = user.mid
        user_info = extract_user_info_by_mid(user_id)
        user_sex = user_info.sex
        user_follow = user_info.follow
        user_fans = user_info.fans
        user_article = user_info.article
        user_place = user_info.place
        print("总评论数：%s, 评论内容: %s, 评论用户名：%s, 评论用户ID: %s, 评论ID: %s, 评论楼层: %s， 评论点赞数：%s, 评论用户性别： %s, 评论用户关注数: %s, 评论用户粉丝数: %s, 评论用户投稿数： %s, 评论用户所在地: %s" % (str(comment_length),message, user_name, user_id, str(comment_id), str(floor), str(like), str(user_sex), str(user_follow), str(user_fans), str(user_article), str(user_place)))

def extract_all_comments(aid,order):
    aid = aid
    comment_list = GetComment_v2(aid,page = 1,order = 0)
    comment_length = comment_list.commentLen
    MaxPageSize = math.ceil(comment_length / 20)
    order = order
    commentList = GetComment_v2(aid, MaxPageSize, order)
    if MaxPageSize == 1:
        return commentList
    for p in range(2,MaxPageSize+1):
        t_commentlist = GetComment_v2(aid, p, order)
        for liuyan in t_commentlist.comments:
            commentList.comments.append(liuyan)
        time.sleep(0.5)
    return commentList

def display_all_comments(aid,order):
    aid = aid
    order = order
    allcomment = extract_all_comments(aid,order)
    total_number_comment = allcomment.commentLen
    comment = allcomment.comments
    for i in range(len(comment)):
        comment_now = comment[i]
        message = comment_now.msg
        floor = comment_now.lv
        comment_id = math.floor(comment_now.fbid)
        status = comment_now.ad_check
        like = comment_now.like
        user = comment_now.post_user
        user_name = user.name.decode("utf-8")
        user_id = user.mid
        user_info = extract_user_info_by_mid(user_id)
        user_sex = user_info.sex
        user_follow = user_info.follow
        user_fans = user_info.fans
        user_article = user_info.article
        user_place = user_info.place
        print("总评论数：%s, 评论内容: %s, 评论用户名：%s, 评论用户ID: %s, 评论ID: %s, 评论楼层: %s， 评论点赞数：%s, 评论用户性别： %s, 评论用户关注数: %s, 评论用户粉丝数: %s, 评论用户投稿数： %s, 评论用户所在地: %s" % (str(total_number_comment),message, user_name, user_id, str(comment_id), str(floor), str(like), str(user_sex), str(user_follow), str(user_fans), str(user_article), str(user_place)))

def extract_video_info(aid):
    aid = str(aid)
    url = 'https://api.bilibili.com/x/web-interface/archive/stat?aid=' + aid
    header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}
    response = requests.get(url, headers=header)
    response.encoding = 'utf-8'
    html = response.json()
    video = biclass.Video()
    video.aid = aid
    video.guankan = html['data']['view']
    video.shoucang = html['data']['favorite']
    video.danmu = html['data']['danmaku']
    video.commentNumber = html['data']['reply']
    video.coin = html['data']['coin']
    video.share = html['data']['share']
    video.like = html['data']['like']
    video.nowRank = html['data']['now_rank']
    video.hisRank = html['data']['his_rank']
    url = 'https://www.bilibili.com/video/av'+aid
    response = requests.get(url, headers=header)
    response.encoding = 'utf-8'
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    up_name = soup.find('a', class_='name').string
    up_url = 'https:' + soup.find('a', class_='name')['href']
    up_id = str(soup.find('a', class_='name')['href']).split('/')[-1]
    video.upName = up_name
    video.upID = up_id
    video.now = datetime.datetime.now()
    video.score = (video.commentNumber)*10+(video.coin)*20+(video.shoucang)*10+(video.danmu)*5+(video.guankan)*0.5
    url = 'https://api.bilibili.com/x/web-interface/view/detail?aid=' + aid
    response = requests.get(url, headers=header)
    response.encoding = 'utf-8'
    html = response.json()
    video.title = html['data']['View']['title']
    video.tid = html['data']['View']['tid']
    video.tname = html['data']['View']['tname']
    video.date = datetime.datetime.fromtimestamp(html['data']['View']['pubdate']).strftime('%Y-%m-%d %H:%M:%S')
    video.duration = html['data']['View']['duration']
    return video

def extract_video_tag(aid):
    aid = str(aid)
    url = 'https://api.bilibili.com/x/tag/archive/tags?&aid='+aid
    header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}
    response = requests.get(url, headers=header)
    response.encoding = 'utf-8'
    html = response.json()
    html_data = html['data']
    tag_id = [x['tag_id'] for x in html_data]
    tag_name = [x['tag_name'] for x in html_data]
    tag_cover = [x['cover'] for x in html_data]
    tag_head_cover = [x['head_cover'] for x in html_data]
    tag_content = [x['content'] for x in html_data]
    tag_short_content = [x['short_content'] for x in html_data]
    tag_type = [x['type'] for x in html_data]
    tag_state = [x['state'] for x in html_data]
    tag_ctime = [x['ctime'] for x in html_data]
    tag_view = [x['count']['view'] for x in html_data]
    tag_use = [x['count']['use'] for x in html_data]
    tag_atten = [x['count']['atten'] for x in html_data]
    tag_is_atten = [x['is_atten'] for x in html_data]
    tag_likes = [x['likes'] for x in html_data]
    tag_hates = [x['hates'] for x in html_data]
    tag_attribute = [x['attribute'] for x in html_data]
    tag_liked = [x['liked'] for x in html_data]
    tag_hated = [x['hated'] for x in html_data]
    tag_number = len(tag_id)
    tagList = [Tag() for i in range(tag_number)]
    for i in range(tag_number):
        tagList[i].id = tag_id[i]
        tagList[i].name = tag_name[i]
        tagList[i].cover = tag_cover[i]
        tagList[i].head_cover = tag_head_cover[i]
        tagList[i].content = tag_content[i]
        tagList[i].short_content = tag_short_content[i]
        tagList[i].type = tag_type[i]
        tagList[i].state = tag_state[i]
        tagList[i].ctime = tag_ctime[i]
        tagList[i].view = tag_view[i]
        tagList[i].use = tag_use[i]
        tagList[i].atten = tag_atten[i]
        tagList[i].is_atten = tag_is_atten[i]
        tagList[i].likes= tag_likes[i]
        tagList[i].hates= tag_hates[i]
        tagList[i].attribute = tag_attribute[i]
        tagList[i].liked = tag_liked[i]
        tagList[i].hated = tag_hated[i]
    return tagList, tag_number

def get_cid(aid):
    aid = str(aid)
    url = 'https://www.bilibili.com/widget/getPageList?aid='+aid
    header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}
    response = requests.get(url, headers=header)
    response.encoding = 'utf-8'
    html = response.json()
    cid = html[0]['cid']
    return cid

def get_danmu(aid):
    aid = str(aid)
    cid = get_cid(aid)
    cid = str(cid)
    url = 'https://api.bilibili.com/x/v1/dm/list.so?oid='+cid
    xml = urllib.request.urlopen(url)
    xml = xml.read()
    xml = xml.decode("utf-8")
    header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}
    response = requests.get(url, headers=header)
    response.encoding = 'utf-8'
    html = response.json()

def get_latestVideo_info(page, numberPerPage):
    page = str(page)
    numberPerPage = str(numberPerPage) 
    header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}
    url = "https://api.bilibili.com/x/web-interface/newlist?&pn=%s&ps=%s" % (page, numberPerPage)
    response = requests.get(url, headers=header)
    response.encoding = 'utf-8'
    html = response.json()
    videoList_info = html['data']['archives']
    video_aid = [x['aid'] for x in videoList_info]
    video_title = [x['title'] for x in videoList_info]
    video_cid = [x['cid'] for x in videoList_info]
    video_tid = [x['tid'] for x in videoList_info]
    video_tname = [x['tname'] for x in videoList_info]
    video_ctime = [datetime.datetime.fromtimestamp(x['ctime']).strftime('%Y-%m-%d %H:%M:%S') for x in videoList_info]
    video_desc = [x['desc'] for x in videoList_info]
    video_attribute = [x['attribute'] for x in videoList_info]
    video_duration = [str(datetime.timedelta(seconds = x['duration'])) for x in videoList_info]
    video_mid = [x['owner']['mid'] for x in videoList_info]
    video_upname = [x['owner']['name'] for x in videoList_info]
    video_guankan = [x['stat']['view'] for x in videoList_info]
    video_danmu = [x['stat']['danmaku'] for x in videoList_info]
    video_commentNumber = [x['stat']['reply'] for x in videoList_info]
    video_shoucang = [x['stat']['favorite'] for x in videoList_info]
    video_coin = [x['stat']['coin'] for x in videoList_info]
    video_share = [x['stat']['share'] for x in videoList_info]
    video_nowRank = [x['stat']['now_rank'] for x in videoList_info]
    video_hisRank = [x['stat']['his_rank'] for x in videoList_info]
    video_like = [x['stat']['like'] for x in videoList_info]
    video_dislike = [x['stat']['dislike'] for x in videoList_info]
    video_nowRank = [x['stat']['now_rank'] for x in videoList_info]
    numberPerPage = int(numberPerPage)
    videoList = [Video() for i in range(numberPerPage)]
    for i in range(numberPerPage):
        videoList[i].aid = video_aid[i]
        videoList[i].title = video_title[i]
        videoList[i].cid = video_cid[i]
        videoList[i].tid = video_tid[i]
        videoList[i].tname = video_tname[i]
        videoList[i].ctime = video_ctime[i]
        videoList[i].desc = video_desc[i]
        videoList[i].attribute = video_attribute[i]
        videoList[i].duration = video_duration[i]
        videoList[i].mid = video_mid[i]
        videoList[i].upname = video_upname[i]
        videoList[i].guankan = video_guankan[i]
        videoList[i].danmu = video_danmu[i]
        videoList[i].commentNumber = video_commentNumber[i]
        videoList[i].shoucang = video_shoucang[i]
        videoList[i].coin = video_coin[i]
        videoList[i].share = video_share[i]
        videoList[i].nowRank = video_nowRank[i]
        videoList[i].hisRank = video_hisRank[i]
        videoList[i].like = video_like[i]
        videoList[i].dislike = video_dislike[i]
    return videoList

def get_latestVideo_info_by_rid(rid, page, numberPerPage):
    rid = str(rid)
    page = str(page)
    numberPerPage = str(numberPerPage) 
    header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}
    url = "https://api.bilibili.com/x/web-interface/newlist?&rid=%s&pn=%s&ps=%s" % (rid, page, numberPerPage)
    response = requests.get(url, headers=header)
    response.encoding = 'utf-8'
    html = response.json()
    videoList_info = html['data']['archives']
    video_aid = [x['aid'] for x in videoList_info]
    video_title = [x['title'] for x in videoList_info]
    video_cid = [x['cid'] for x in videoList_info]
    video_tid = [x['tid'] for x in videoList_info]
    video_tname = [x['tname'] for x in videoList_info]
    video_ctime = [datetime.datetime.fromtimestamp(x['ctime']).strftime('%Y-%m-%d %H:%M:%S') for x in videoList_info]
    video_desc = [x['desc'] for x in videoList_info]
    video_attribute = [x['attribute'] for x in videoList_info]
    video_duration = [str(datetime.timedelta(seconds = x['duration'])) for x in videoList_info]
    video_mid = [x['owner']['mid'] for x in videoList_info]
    video_upname = [x['owner']['name'] for x in videoList_info]
    video_guankan = [x['stat']['view'] for x in videoList_info]
    video_danmu = [x['stat']['danmaku'] for x in videoList_info]
    video_commentNumber = [x['stat']['reply'] for x in videoList_info]
    video_shoucang = [x['stat']['favorite'] for x in videoList_info]
    video_coin = [x['stat']['coin'] for x in videoList_info]
    video_share = [x['stat']['share'] for x in videoList_info]
    video_nowRank = [x['stat']['now_rank'] for x in videoList_info]
    video_hisRank = [x['stat']['his_rank'] for x in videoList_info]
    video_like = [x['stat']['like'] for x in videoList_info]
    video_dislike = [x['stat']['dislike'] for x in videoList_info]
    video_nowRank = [x['stat']['now_rank'] for x in videoList_info]
    numberPerPage = int(numberPerPage)
    videoList = [Video() for i in range(numberPerPage)]
    for i in range(numberPerPage):
        videoList[i].aid = video_aid[i]
        videoList[i].title = video_title[i]
        videoList[i].cid = video_cid[i]
        videoList[i].tid = video_tid[i]
        videoList[i].tname = video_tname[i]
        videoList[i].ctime = video_ctime[i]
        videoList[i].desc = video_desc[i]
        videoList[i].attribute = video_attribute[i]
        videoList[i].duration = video_duration[i]
        videoList[i].mid = video_mid[i]
        videoList[i].upname = video_upname[i]
        videoList[i].guankan = video_guankan[i]
        videoList[i].danmu = video_danmu[i]
        videoList[i].commentNumber = video_commentNumber[i]
        videoList[i].shoucang = video_shoucang[i]
        videoList[i].coin = video_coin[i]
        videoList[i].share = video_share[i]
        videoList[i].nowRank = video_nowRank[i]
        videoList[i].hisRank = video_hisRank[i]
        videoList[i].like = video_like[i]
        videoList[i].dislike = video_dislike[i]
    return videoList

def get_latestDynamic_info(rid, page, numberPerPage):
    rid = str(rid)
    page = str(page)
    numberPerPage = str(numberPerPage) 
    header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}
    url = "https://api.bilibili.com/x/web-interface/dynamic/region?&rid=%s&pn=%s&ps=%s" % (rid, page, numberPerPage)
    response = requests.get(url, headers=header)
    response.encoding = 'utf-8'
    html = response.json()
    videoList_info = html['data']['archives']
    video_aid = [x['aid'] for x in videoList_info]
    video_title = [x['title'] for x in videoList_info]
    video_cid = [x['cid'] for x in videoList_info]
    video_tid = [x['tid'] for x in videoList_info]
    video_tname = [x['tname'] for x in videoList_info]
    video_ctime = [datetime.datetime.fromtimestamp(x['ctime']).strftime('%Y-%m-%d %H:%M:%S') for x in videoList_info]
    video_desc = [x['desc'] for x in videoList_info]
    video_attribute = [x['attribute'] for x in videoList_info]
    video_duration = [str(datetime.timedelta(seconds = x['duration'])) for x in videoList_info]
    video_mid = [x['owner']['mid'] for x in videoList_info]
    video_upname = [x['owner']['name'] for x in videoList_info]
    video_guankan = [x['stat']['view'] for x in videoList_info]
    video_danmu = [x['stat']['danmaku'] for x in videoList_info]
    video_commentNumber = [x['stat']['reply'] for x in videoList_info]
    video_shoucang = [x['stat']['favorite'] for x in videoList_info]
    video_coin = [x['stat']['coin'] for x in videoList_info]
    video_share = [x['stat']['share'] for x in videoList_info]
    video_nowRank = [x['stat']['now_rank'] for x in videoList_info]
    video_hisRank = [x['stat']['his_rank'] for x in videoList_info]
    video_like = [x['stat']['like'] for x in videoList_info]
    video_dislike = [x['stat']['dislike'] for x in videoList_info]
    video_nowRank = [x['stat']['now_rank'] for x in videoList_info]
    numberPerPage = int(numberPerPage)
    videoList = [Video() for i in range(numberPerPage)]
    for i in range(numberPerPage):
        videoList[i].aid = video_aid[i]
        videoList[i].title = video_title[i]
        videoList[i].cid = video_cid[i]
        videoList[i].tid = video_tid[i]
        videoList[i].tname = video_tname[i]
        videoList[i].ctime = video_ctime[i]
        videoList[i].desc = video_desc[i]
        videoList[i].attribute = video_attribute[i]
        videoList[i].duration = video_duration[i]
        videoList[i].mid = video_mid[i]
        videoList[i].upname = video_upname[i]
        videoList[i].guankan = video_guankan[i]
        videoList[i].danmu = video_danmu[i]
        videoList[i].commentNumber = video_commentNumber[i]
        videoList[i].shoucang = video_shoucang[i]
        videoList[i].coin = video_coin[i]
        videoList[i].share = video_share[i]
        videoList[i].nowRank = video_nowRank[i]
        videoList[i].hisRank = video_hisRank[i]
        videoList[i].like = video_like[i]
        videoList[i].dislike = video_dislike[i]
    return videoList

def get_allVideoInfo_about_MMQ():   #missing video name
    url = 'https://search.bilibili.com/all?keyword=%E5%AD%9F%E7%BE%8E%E5%B2%90'
    content = getURLContent(url)
    html_info = html.fromstring(content)
    span = [td.text for td in html_info.xpath("//span")]
    span = [str(i) for i in span]
    sub = 'av'
    av = [s for s in span if sub in s]
    for i in range(len(av)):
        aid = av[i][2:]
        video = extract_video_info(aid)
        print('av号"%s" \t up主"%s" \t up主ID"%s" \t 播放量:%s \t 评论数:%s \t 弹幕数:%s \t 点赞数:%s \t 收藏数:%s \t 硬币数:%s \t 分享数:%s \t 当前排名:%s \t 历史排名:%s' % (video.aid, video.upName, video.upID, video.guankan, video.commentNumber, video.danmu, video.like, video.shoucang, video.coin, video.share, video.nowRank, video.hisRank))
        tagList, tag_number= extract_video_tag(aid)
        for i in range(tag_number):
            tag = tagList[i]
            print('tag名"%s" \t tag ID:%s \t 使用次数:%s \t 关注数:%s \t 顶:%s \t 踩:%s \t 简介:%s' % (tag.name, tag.id, tag.use, tag.atten, tag.likes, tag.hates, tag.content)) 

def get_latestVideoInfo_about_MMQ_per_page(page):
    page = str(page)
    url = "https://search.bilibili.com/all?keyword=%E5%AD%9F%E7%BE%8E%E5%B2%90&order=pubdate&duration=0&tids_1=0&page=" + page
    content = support.getURLContent(url)
    html_info = html.fromstring(content)
    span = [td.text for td in html_info.xpath("//span")]
    span = [str(i) for i in span]
    sub = 'av'
    av = [s for s in span if sub in s]
    videoAIDList = []
    for i in range(len(av)):
        aid = av[i][2:]
        #video = extract_video_info(aid)
        #videoAIDList.append(video.aid)
        videoAIDList.append(aid)
    return videoAIDList

def get_latestVideoInfo_about_MMQ():
    videoAIDListALL=[]
    for i in range(1,3):
        videoAIDList = get_latestVideoInfo_about_MMQ_per_page(i)
        videoAIDListALL.extend(videoAIDList)
    return videoAIDListALL

def get_totalRankVideoInfo_about_MMQ_per_page(page):
    page = str(page)
    url = "https://search.bilibili.com/all?keyword=%E5%AD%9F%E7%BE%8E%E5%B2%90&order=totalrank&duration=0&tids_1=0&page=" + page
    content = support.getURLContent(url)
    html_info = html.fromstring(content)
    span = [td.text for td in html_info.xpath("//span")]
    span = [str(i) for i in span]
    sub = 'av'
    av = [s for s in span if sub in s]
    videoAIDList = []
    for i in range(len(av)):
        aid = av[i][2:]
        #video = extract_video_info(aid)
        #videoAIDList.append(video.aid)
        videoAIDList.append(aid)
    return videoAIDList

def get_totalRankVideoInfo_about_MMQ():
    videoAIDListALL=[]
    for i in range(1,3):
        videoAIDList = get_totalRankVideoInfo_about_MMQ_per_page(i)
        videoAIDListALL.extend(videoAIDList)
    return videoAIDListALL

def get_clickVideoInfo_about_MMQ_per_page(page):
    page = str(page)
    url = "https://search.bilibili.com/all?keyword=%E5%AD%9F%E7%BE%8E%E5%B2%90&order=click&duration=0&tids_1=0&page=" + page
    content = support.getURLContent(url)
    html_info = html.fromstring(content)
    span = [td.text for td in html_info.xpath("//span")]
    span = [str(i) for i in span]
    sub = 'av'
    av = [s for s in span if sub in s]
    videoAIDList = []
    for i in range(len(av)):
        aid = av[i][2:]
        #video = extract_video_info(aid)
        #videoAIDList.append(video.aid)
        videoAIDList.append(aid)
    return videoAIDList

def get_clickVideoInfo_about_MMQ():
    videoAIDListALL=[]
    for i in range(1,3):
        videoAIDList = get_clickVideoInfo_about_MMQ_per_page(i)
        videoAIDListALL.extend(videoAIDList)
    return videoAIDListALL

def get_allUpInfo():
    videoAIDListALL = get_latestVideoInfo_about_MMQ()
    upInfoList = []
    for i in videoAIDListALL:
        user = extract_upInfo(i)
        upInfoList.append(user)
    return upInfoList

def get_baidu():
    url = "https://mbd.baidu.com/webpage?type=starhit&action=home&format=json&uk=2IhtQWM6eZUH0JR86UqkcQ&queryType=femaleStar"
    header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}
    response = requests.get(url, headers=header)
    response.encoding = 'utf-8'
    html = response.json()
    pageInfo = html['data']['femaleStar']
    name = [x['name'] for x in pageInfo]
    vote = [x['vote'] for x in pageInfo]
    number = len(name)
    Baiduvote = [biclass.BaiduVote() for i in range(number)]
    for i in range(number):
        Baiduvote[i].name = name[i]
        Baiduvote[i].vote = vote[i]
    return Baiduvote

#############################Get Number of People Online Now ############################################
def online_number():
    mainUrl="http://www.bilibili.com/online.js"
    resp = urllib.request.urlopen(url = mainUrl)
    resp = resp.read()
    return resp

def get_page_source(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return "failed"

def getViewInfo(url, fpath):
    html = get_page_source(url)
    try:
        json_data = json.loads(html)
        all_count = (json_data['data']['all_count'])
        web_online = (json_data['data']['web_online'])
        play_online = (json_data['data']['play_online'])
        with open(fpath, 'a', encoding='utf-8') as f:
            nowTime = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M'))
            f.write(nowTime + "     " + "在线人数：" + str(web_online) + "     " + "最新投稿数: "+ str(all_count) + '\n')
    except:
        traceback.print_exc()

def onlineNumberContinuously():
    count = 0
    while 1:
        url = "https://api.bilibili.com/x/web-interface/online"
        output_path = "E://bilibiliInfo.txt"
        getViewInfo(url, output_path)
        count = count + 1
        print(count)
        time.sleep(60)

############################################################################################################
'''
'https://api.bilibili.com/x/v2/reply/web/emojis?callback=emoji&jsonp=jsonp'
'https://api.bilibili.com/x/web-interface/elec/show?&aid=36500943&mid=777536'
'https://api.bilibili.com/x/v2/reply?&pn=1&type=1&oid=36500943&sort=0&_=1543148735860'
'https://api.bilibili.com/x/player/videoshot?aid=36500943&cid=64093308&index=1&jsonp=jsonp'
弹幕：'https://api.bilibili.com/x/v1/dm/list.so?oid=64093308'
'''