from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework.views import APIView
from .models import Feed

class Main(APIView):
    def get(self,request):
        feed_list=Feed.objects.all().order_by('-id')
        return render(request, "Real_Sion_Stargram/main.html",context=dict(feeds=feed_list))

    #화면에 표시할 html, w전달할 데이터를 줌