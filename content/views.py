import os
from uuid import uuid4

from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Feed, Reply, Like, Bookmark
from user.models import User
from Real_Sion_Stargram.settings import MEDIA_ROOT


class Main(APIView):
    def get(self, request):
        email = request.session.get('email', None)

        if email is None:
            return render(request, "user/login.html")
        # request.session['email']로 뜸
        user = User.objects.filter(email=email).first()

        if user is None:
            return render(request, "user/login/html")


        feed_object_list = Feed.objects.all().order_by('-id')

        feed_list = []

        for feed in feed_object_list:
            user1 = User.objects.filter(email=feed.email).first()
            reply_object_list = Reply.objects.filter(feed_id=feed.id)
            reply_list = []

            for reply in reply_object_list:
                user1 = User.objects.filter(email=reply.email).first()
                reply_list.append(dict(
                    reply_content=reply.reply_content,
                    nickname=user1.nickname
                ))
            like_count = Like.objects.filter(feed_id=feed.id, is_like=True).count()
            is_like = Like.objects.filter(feed_id=feed.id, email=email, is_like=True).exists()  # 있으면 true가됨
            is_marked = Bookmark.objects.filter(feed_id=feed.id, email=email, is_marked=True).exists()  # 있으면 true가됨
            feed_list.append(dict(
                id=feed.id,

                image=feed.image,
                content=feed.content,
                like_count=like_count,
                profile_image=user1.profile_image,
                nickname=user1.nickname,
                reply_list=reply_list,
                is_like=is_like,
                is_marked=is_marked
            ))

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
        email = request.session.get('email', None)

        Feed.objects.create(image=image, content=content, email=email)

        return Response(status=200)


class Profile(APIView):
    def get(self, request):
        email = request.session.get('email', None)

        if email is None:
            return render(request, "user/login.html")
        # request.session['email']로 뜸
        user = User.objects.filter(email=email).first()

        if user is None:
            return render(request, "user/login.html")

        feed_list= Feed.objects.filter(email=email).all()

        feed_nums= len(feed_list)

        like_list= list(Like.objects.filter(email=email,is_like=True).values_list('feed_id',flat=True)) #리스트로
        like_feed_list= Feed.objects.filter(id__in=like_list)


        bookmark_list = list(Bookmark.objects.filter(email=email, is_marked=True).values_list('feed_id', flat=True))
        bookmark_feed_list = Feed.objects.filter(id__in=bookmark_list)


        return render(request, 'content/profile.html', context=dict(feed_list=feed_list ,
                                                                    like_feed_list=like_feed_list,
                                                                    bookmark_feed_list=bookmark_feed_list,
                                                                    user=user,
                                                                    feed_nums=feed_nums
                                                                ))


class UploadReply(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id', None)
        reply_content = request.data.get('reply_content', None)
        email = request.session.get('email', None)

        Reply.objects.create(feed_id=feed_id, reply_content=reply_content, email=email)

        return Response(status=200)


class ToggleLike(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id', None)
        favorite_text = request.data.get('favorite_text', True)  # 안올라오면 트루

        if favorite_text == 'favorite_border':
            is_like = True
        else:
            is_like = False

        email = request.session.get('email', None)

        like= Like.objects.filter(feed_id=feed_id,email=email).first()

        if like:
            like.is_like=is_like
            like.save()
        else:
            Like.objects.create(feed_id=feed_id, is_like=is_like, email=email)

        return Response(status=200)


class ToggleBookmark(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id', None)
        bookmark_text = request.data.get('bookmark_text', True)  # 안올라오면 트루

        if bookmark_text == 'bookmark_border':
            is_marked = True
        else:
            is_marked = False

        email = request.session.get('email', None)

        bookmark= Bookmark.objects.filter(feed_id=feed_id,email=email).first()

        if bookmark:
            bookmark.is_marked=is_marked
            bookmark.save()
        else:
            Bookmark.objects.create(feed_id=feed_id, is_marked=is_marked, email=email)

        return Response(status=200)