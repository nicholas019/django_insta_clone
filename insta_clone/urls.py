from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path, include


from .view import Sub  # view에서 만들었던 sub클래스를 불러온다.
# content폴더 안에 있는 view폴더에서 만들었던 Main클래스를 불러온다.
from content.views import Main, UploadFeed

urlpatterns = [
    path('admin/', admin.site.urls),
    path('main/', Main.as_view()),
    path('1', Sub.as_view()),
    # path('content/upload', UploadFeed.as_view()),
    # 위의 UploadFeed를 불러오려고하려면 content폴더로 urls.py가 이동했으므로 include를 이용해 불러와야한다.
    path('content/', include('content.urls')),
    path('user/', include('user.urls')),
]

# 이미지파일을 media폴더에서 조회할수 있는 코드
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#
