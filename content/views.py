import os
from uuid import uuid4

from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Feed
from user.models import User
from Real_Sion_Stargram.settings import MEDIA_ROOT


class Main(APIView):
    def get(self, request):
        feed_list = Feed.objects.all().order_by('-id')

        email = request.session.get('email', None)

        if email is None:
            return render(request, "user/login.html")
        # request.session['email']로 뜸
        user = User.objects.filter(email=email).first()

        if user is None:
            return render(request, "user/login/html")

        return render(request, "Real_Sion_Stargram/main.html", context=dict(feeds=feed_list, user=user))


# 이렇게 함으로써 더 편하게
# 화면에 표시할 html, w전달할 데이터를 줌


class UploadFeed(APIView):
    def post(self, request):
        # 일단 파일불러옴
        file = request.FILES['file']
        # 대문자로 부름

        # 데이터는 request.data.get() 이고 파일은 request.FILES[ ㅇㅇ]
        uuid_name = uuid4().hex  # 고유한 값을 주기 위해서. 랜덤하게 글자 만들어줌
        save_path = os.path.join(MEDIA_ROOT, uuid_name)
        # MEDIA_ROOT =>베이스에다가 media 붙인경로 + uuid_name 도 쓰겠다
        # ~/media/uuid로 생성된...

        with open(save_path, 'wb+') as destination:  # 파일 열어서
            for chunk in file.chunks():  # 파일 읽어서 그냥 쓰는거다
                destination.write(chunk)

        # 보통은 파일을 위한 서버가 따로 있음.

        # image=request.data.get('image')
        # 파일 이미지가 필요없음 이미 주어진건. uuid쓰면됨

        image = uuid_name
        content = request.data.get('content')
        user_id = request.data.get('user_id')
        profile_image = request.data.get('profile_image')

        Feed.objects.create(image=image, content=content, user_id=user_id, profile_image=profile_image, like_count=0)

        return Response(status=200)


class Profile(APIView):
    def get(self, request):
        return render(request, 'content/profile.html')