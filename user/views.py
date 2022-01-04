import os
from uuid import uuid4

from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from django.contrib.auth.hashers import make_password
from Real_Sion_Stargram.settings import MEDIA_ROOT

class Join(APIView):
    def get(self, request):
        return render(request, "user/join.html")

    def post(self, request):
        # TODO 회원가입

        email = request.data.get('email', None)
        nickname = request.data.get('nickname', None)
        name = request.data.get('name', None)

        password = request.data.get('password', None)

        User.objects.create(email=email,
                            nickname=nickname,
                            name=name,
                            password=make_password(password),
                            profile_image="default_profile.png")

        return Response(status=200)


class Login(APIView):
    def get(self, request):
        return render(request, "user/login.html")

    def post(self, request):
        email = request.data.get('email', None)
        password = request.data.get('password', None)

        user= User.objects.filter(email=email).first() #first면 하나로할수있기때문

        if user is None :
            return Response(status=400,data=dict(message="회원정보가 잘못되었습니다."))

        if user.check_password(password):
            #TODO 로그인했다. 세션 or 쿠키에 넣는다
            request.session['email']=email
            #session['email']
            return Response(status=200)
        else:
            return Response(status=400, data=dict(message="회원정보가 잘못되었습니다."))

class LogOut(APIView):
    def get(self, request):
        request.session.flush()
        return render(request, "user/login.html")


class UploadProfile(APIView):
    def post(self, request):
        # 일단 파일불러옴
        file = request.FILES['file']
        email = request.data.get('email')
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

        profile_image = uuid_name
        email = request.data.get('email')

        user=User.objects.filter(email=email).first()

        user.profile_image=profile_image

        user.save()
        return Response(status=200)
