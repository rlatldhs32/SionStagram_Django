from django.contrib import admin
from django.urls import path
from .views import UploadFeed,Profile
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('upload', UploadFeed.as_view()),
    path('profile',Profile.as_view())
    # post로 호출할때는 뒤에 / 를 빼야함
]
