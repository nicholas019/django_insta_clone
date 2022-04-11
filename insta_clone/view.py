from django.shortcuts import render
from rest_framework.views import APIView


class Sub(APIView):
    def get(self, request):
        print('get로 호출')  # 사용자에게 출력하는것이아니라 서버 로그에 출력된다.
        return render(request, "insta_clone/main.html")

    def post(self, request):
        print('post로 호출')  # 사용자에게 출력하는것이아니라 서버 로그에 출력된다.
        return render(request, "insta_clone/main.html")
