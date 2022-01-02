from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser


# Create your models here.
# user->models.py에서 설정가능
class User(AbstractBaseUser):
    """
    유저 프로필사진
    유저 닉네임
    유저 이름
    유저 이메일주소 -> 회원가입할때 사용하는 아이디
    유저 비밀번호
    """
    profile_image = models.TextField()  # 프로필이미지
    nickname = models.CharField(max_length=24, unique=True)
    name = models.CharField(max_length=24)
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'nickname'

    class Meta:
        db_table = "User"
