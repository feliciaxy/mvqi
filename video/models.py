from django.db import models
from django.utils import timezone
#from django.contrib.auth.models import User

class Video(models.Model):
    aid = models.CharField(max_length=300)
    score = models.IntegerField(default=0)
    upName = models.CharField(max_length=300)
    upID = models.CharField(max_length=300)
    guankan = models.IntegerField()
    commentNumber = models.IntegerField()
    danmu = models.IntegerField()
    like = models.IntegerField()
    shoucang = models.IntegerField()
    coin = models.IntegerField()
    share = models.IntegerField()
    nowRank = models.IntegerField()
    hisRank = models.IntegerField()
    data_posted = models.DateTimeField(default=timezone.now)