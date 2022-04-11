from calendar import c
from email.mime import image
from django.db import models

# Create your models here.

# 데이터 베이스 테이블 목차에 대한 변수 설정


class Feed(models.Model):        # models라는 모듈을 상속받는 Feed라는 클래스 생성
    content = models.TextField()  # 글내용
    image = models.TextField()   # 피드 이미지
    profile = models.TextField()  # 프로필이미지
    user_id = models.TextField()  # 글쓴이
    like_count = models.IntegerField()  # 좋아요 수
