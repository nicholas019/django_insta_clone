from django.urls import path

# content폴더 안에 있는 view폴더에서 만들었던 Main클래스를 불러온다.
from .views import UploadFeed

urlpatterns = [
    path('upload', UploadFeed.as_view()),
]
