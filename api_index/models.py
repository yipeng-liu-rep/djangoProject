# import datetime
from django.db import models
# from django.utils import timezone





class UserInfo(models.Model):
    # 用户表
    username = models.CharField(max_length=200)
    openid = models.CharField(max_length=255)
    avatar = models.CharField(max_length=200, default="")
    language = models.CharField(max_length=50, default="")
    province = models.CharField(max_length=50, default="")
    city = models.CharField(max_length=50, default="")
    country = models.CharField(max_length=50, default="")
    creat_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.openid


class Article(models.Model):
    # 文章表
    article_title = models.CharField(max_length=200)
    article_content = models.TextField()
    article_photo_path = models.ImageField(upload_to='image/')
    article_owner = models.ForeignKey(UserInfo, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.article_title


class Collection(models.Model):
    # 收藏表
    collection_username = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    collection_article_name = models.ForeignKey(Article, on_delete=models.CASCADE)
