from django.urls import path


# content폴더 안에 있는 view폴더에서 만들었던 Main클래스를 불러온다.
from .views import Join, Login, LogOut, UploadProfile

urlpatterns = [
    path('join', Join.as_view()),
    path('login', Login.as_view()),
    path('logout', LogOut.as_view()),
    path('profile/upload', UploadProfile.as_view()),
]
