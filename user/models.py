from django.db import models
# 기본유저관리모델을 기반으로한 커스텀 유저 관리모델을 만드는 모델
from django.contrib.auth.base_user import AbstractBaseUser

# Create your models here.

# 데이터베이스 테이블 목차에 대한 변수 설정

# Mata 클래스에 선언된 User이라는 커스텀유저관리 데이터베이스 에 User클래스를 이용해서 들어온 정보를 각 필드에 담아 데이터베이스에 저장한다.


class User(AbstractBaseUser):
    # 유저 프로파일 사진
    # 유저 닉네임 : 화면에 표기되는 이름
    # 유저 이름 : 실제 사용자 이름
    # 유저 이메일주소 : 회원가입시 사용하는 아이디
    # 유저 비밀번호 : 디폴트 값 사용

    profile = models.TextField()   # TextField는 글자수 제한없는 필드
    nickname = models.CharField(
        max_length=24, unique=True)   # CharField는 글자수 제한있는 필드
    name = models.CharField(max_length=24)
    email = models.EmailField(unique=True)

    # 실제로 User 클래스를 사용해서 불러올때 이름을 무엇으로 쓰는지 설정(항상 겹치지 않는 것으로 설정해야함.)
    USERNAME_FIELD = 'nickname'

    class Meta:  # 데이터베이스 테이블명 설정(커스텀 유저 사용시 사용)
        db_table = "User"
