from django.db import models

# Create your models here.
class Feed(models.Model):
    content=models.TextField() #글내용
    image=models.TextField() #피드이미지
    email=models.EmailField(default='')



class Like(models.Model):
    feed_id = models.IntegerField(default=0) # 뭘 좋아하는지
    email=models.EmailField(default='') #누른 사람
    is_like = models.BooleanField(default=True)

# 1번 이메일 OK

class Reply(models.Model):
    feed_id = models.IntegerField(default=0)
    email=models.EmailField(default='')
    reply_content = models.TextField()

class Bookmark(models.Model):
    feed_id = models.IntegerField(default=0)
    email = models.EmailField(default='')
    is_marked = models.BooleanField(default=True)