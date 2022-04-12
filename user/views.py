import email
import os
from django.shortcuts import render
from rest_framework.views import APIView
from .models import User
from django.contrib.auth.hashers import make_password  # 장고에서 기본적으로 제공하는 단방향 암호화 모듈
from rest_framework.response import Response
from uuid import uuid4
from insta_clone.settings import MEDIA_ROOT

# Create your views here.


class Join(APIView):
    def get(self, request):
        print('get로 호출')  # 사용자에게 출력하는것이아니라 서버 로그에 출력된다.
        return render(request, "user/join.html")

    def post(self, request):
        # 회원가입했을때 각각 변수에 데이터를 받아서 객체로만든다음 models모듈에 User클래스에 넣어라
        email = request.data.get('email', None)
        nickname = request.data.get('nickname', None)
        name = request.data.get('name', None)
        password = request.data.get('password', None)

        User.objects.create(email=email, nickname=nickname, name=name, password=make_password(
            password), profile="default_profile.jpg")

        return Response(status=200)


class Login(APIView):
    def get(self, request):
        print('get로 호출')  # 사용자에게 출력하는것이아니라 서버 로그에 출력된다.
        return render(request, "user/login.html")

    def post(self, request):
        # 로그인했을때 들어온 데이터를 각 변수에 넣고 User클래스를 통해 DB에 데이터를 불러와 filter함수로 동일한지 판별한뒤 user로 돌려준다.
        email = request.data.get('email', None)
        password = request.data.get('password', None)

        user = User.objects.filter(email=email).first()
        # filter함수는 리스트로 돌려주는데 뒤에 .first()을 넣어주면 가장 1번 리스트만 객체에 들어가게되어 리스트형객체가아닌 문자열객체가 된다.
        # first()함수를 넣는경우는 유니크한경우에 사용하며, 사용하지않을시 리스트형객체로와 인덱스로 끄집어내거나 for문을돌려서 하나씩 꺼내야되는것을 줄여준다.
        if user is None:  # 이메일을 비교햇는데 없는경우
            return Response(status=404, data=dict(message="회원정보가 잘못되었습니다."))

        if user.check_password(password):  # 이메일을 비교했는데 맞는경우 비밀번호와 비교해라
            # 로그인을 완료되었다. 세션 or 쿠키에 넣는다.
            request.session['email'] = email
            # 로그인이 성공했을때 session함수를 통해 models.py에 User클래스를 이용해서 DB에서 email을 조회해서
            # email을 이용해 가입당시에 넣었던 다른 세션정보(이름, 닉네임, 프로필사진 등)을 가져온다.
            return Response(status=200)  # 비밀번호 비교결과 맞으면 200코드

        else:
            # 비밀번호가 틀리면 메세지 를 보내라
            return Response(status=400, data=dict(message="회원정보가 잘못되었습니다."))


class LogOut(APIView):
    def get(self, request):
      # get방식의 로그아웃 : 로그아웃버튼을 누르는 이벤트 발생
        request.session.flush()
        # 가지고있는 세션정보를 지워라
        return render(request, "user/login.html")
        # 세션정보를 지우면 다시 로그인 페이지로 돌아가라


class UploadProfile(APIView):
    def post(self, request):

        # 해석 : 브라우저에 저장되어있는 파일과 이메일주소를 불러온다
        file = request.FILES['file']
        email = request.data.get('email')

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

        # 위의 uuid4().hex 함수로 랜덤하게 이름이바뀐 파일을 profile 변수를 넣는다.
        profile = uuid_name

        # 브라우저에서 불러온 이메일주소를 이용해서 User클래스에 접근해서 user정보를 찾고
        user = User.objects.filter(email=email).first()

        # profile에 있는 파일을 user의 profile에 넣고 저장한다.
        user.profile = profile
        user.save()
        # create의 경우 데이터배이스에서 생성 또는 추가여서 따로 저장할 필요는 없지만 지금처럼 수정하는 경우는 DB저장을 꼭 해줘야한다.

        return Response(status=200)
