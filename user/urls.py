from django.contrib import admin
from django.urls import path
from .views import Join,Login,LogOut

urlpatterns = [
    path('join', Join.as_view()),
    path('login', Login.as_view()),
    path('logout', LogOut.as_view())
    # post로 호출할때는 뒤에 / 를 빼야함
]
