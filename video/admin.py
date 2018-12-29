from django.contrib import admin
from .models import Video
from .models import BaiduVote, LatestVideo, TotalRankVideo, MostClickVideo

admin.site.register(Video)

admin.site.register(BaiduVote)
admin.site.register(LatestVideo)
admin.site.register(TotalRankVideo)
admin.site.register(MostClickVideo)

