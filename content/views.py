import os
from .models import Feed
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render
from uuid import uuid4
from insta_clone.settings import MEDIA_ROOT
from user.models import User

# Create your views here.


class Main(APIView):
    def get(self, request):
        # feed_list = Feed.objects.all() # DB의 ID순서대로 데이터를 가져온다
        feed_list = Feed.objects.all().order_by('-id')  # DB의 ID 역순으로 데이터를 가져온다
        # for feed in feed_list:      # feed_list에 Feed모듈이 관리하는 객체(데이터)들이 어떤것들이 담겼는지 for문을 통해 출력해보고
        #    print(feed.content)     # 확인해보는 작업, 이러한작업을 로그를 찍어본다하는데 중간중간 값을 확인하는 습관을 가지는 것이 좋다.

        # print('로그인한 사용자:', request.session['email']) # 세션정보 있는 email을 출력해라

        email = request.session.get('email', None)
        # 지금 접속해있는 세션정보를 email이라는 변수에 넣어라

        if email is None:  # 만약 이메일이 DB에 없다면 로그인화면으로 돌려보내라
            return render(request, "user/login.html")

        user = User.objects.filter(email=email).first()
        # email변수에 담긴 세션정보를 DB에 필터함수로 조회해서 결과를 user변수에 넣어라

        if user is None:  # 이메일이 맞는게 없어서 user변수에 넣을게 없다면 로그인페이지로 돌려보내라
            return render(request, "user/login.html")

        return render(request, "insta_clone/main.html", context=dict(feeds=feed_list))
        # context의 값을 넣을때는 딕셔너리형식으로 넣어야하는데 이유는 원래 우리가 필요한건 json형식인데 파이썬의 딕셔너리형식이랑 호환이된다.


class UploadFeed(APIView):
    def post(self, request):

        # 해석 : 파일을 불러온다
        file = request.FILES['file']
        # 파일명이 특수문자 한글 등 복잡하게 되어있으면 서버가 읽기 힘들어 고유한 id값으로 변경해주어야 서버가 읽기 편해진다.
        # uuid4.hex를 사용하면 랜덤한 글자를 생성해준다.
        uuid_name = uuid4().hex
        # settings.py에 설정한 미디어서버의 경로(midia폴더)로 uuid4함수를 사용해서 랜덤하게 이름을 바꾼 파일을 저장한다.
        save_path = os.path.join(MEDIA_ROOT, uuid_name)

        # 파일을 하나씩읽어서 저장한다.
        with open(save_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        file = request.data.get('file')

        image = uuid_name  # 위의 uuid4().hex 함수로 랜덤하게 바뀐 파일의 이름의 변수를 넣는다.
        content = request.data.get('content')
        user_id = request.data.get('user_id')
        profile = request.data.get('profile')

# 데이터베이스에는 파일이 실제로 들어가지않고 이미지서버에 파일이 저장되고 데이터베이스에서는 이미지서버의 파일의 위치 주소만 들어간다.
        Feed.objects.create(image=image, content=content,
                            user_id=user_id, profile=profile, like_count=0)

        return Response(status=200)


class Profile(APIView):
    def get(self, request):

        email = request.session.get('email', None)
        # 지금 접속해있는 세션정보를 email이라는 변수에 넣어라

        if email is None:  # 만약 이메일이 DB에 없다면 로그인화면으로 돌려보내라
            return render(request, "user/login.html")

        user = User.objects.filter(email=email).first()
        # email변수에 담긴 세션정보를 DB에 필터함수로 조회해서 결과를 user변수에 넣어라

        if user is None:  # 이메일이 맞는게 없어서 user변수에 넣을게 없다면 로그인페이지로 돌려보내라
            return render(request, "user/login.html")

        return render(request, "content/profile.html", context=dict(user=user))
