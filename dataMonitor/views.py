import datetime

from django.db.models import Avg
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from rest_framework import exceptions, serializers
from rest_framework.utils import json
from rest_framework.views import APIView

from rest_framework_jwt.settings import api_settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.pagination import BasePagination, PageNumberPagination
from rest_framework.serializers import ModelSerializer
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
from user.models import info as userinfo
from equipment.models import his,realtime
import re
import urllib.request
from utils.calculatorAQI import *
'''
{"code":200,"msg":"获取成功",

"y_AQI":xxx,
"y_PM10":xxx,
"y_PM2.5":xxx,
"y_O2":xxx,
"y_SO2":xxx,
"y_NO2":xxx,
"y_CO":xxx,
"AQI":xxx,
"PM10":xxx,
"PM2.5":xxx,
"O2":xxx,
"SO2":xxx,
"NO2":xxx,
"CO":xxx,

"time":1949,"
location":"xxx",
"weather":"sunny",
"temperature":xxx,
"humidity":xxx,
"wind_speed":xxx,
"light":xxx,
"Pa":xxx,
"wind_direction":xxx}
'''
class MyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.GET.get("token")
        if not token:
            ret = {
                "code":400,
                "msg":"请带上token"
            }
            raise exceptions.AuthenticationFailed(json.dumps(ret))
        else:
            user = None
            try:
                user = jwt_decode_handler(token)
            except Exception as e:
                ret = {
                    "code":410,
                    "msg":e
                }
                raise exceptions.AuthenticationFailed(json.dumps(ret)) #这里就终止了
            user1 = userinfo.objects.filter(username=user.get("username")).first()
            if not user1:
                ret = {
                    "code":410,
                    "msg":"用户不存在"
                }
                return HttpResponse(json.dumps(ret))
            else:
                if user1.user_frozen:
                    ret = {
                        "code": 400,
                        "msg": "用户已经冻结"
                    }
                    raise exceptions.AuthenticationFailed(ret)
                else:
                    return (user1,None)

class MyPagination(BasePagination):
    page_size = 2
    page_query_param = "page"
    page_size_query_param = "size"
    max_page_size = 5




class MySerializer(ModelSerializer):
    location = serializers.SerializerMethodField(label='地点')
    class Meta:
        fields = ["equipment_id_id","n_time","location","weather","temperature","humidity","wind_speed","light","Pa","wind_direction"]
        model = realtime
    def get_location(self,obj):

        loc = obj.location
        if loc:
            #print(loc)
            y = re.split(r"[),(]", loc)
            print(y)
            url = "http://api.map.baidu.com/reverse_geocoding/v3/?ak=eAMNZ2ifZrKVL1CskD6hpy5HY3nVrVu4&output=json&coordtype=wgs84ll&location="+y[1]+","+y[0]
            # 打开需要爬取的网页
            resp = urllib.request.urlopen(url)
            # 读取网页代码
            html = resp.read()
            x = json.loads(html)
            # 打印读取的内容
            return x.get("result").get("formatted_address")
            #return "gggggggg"
        else:
            return "无"


class MyPagination(PageNumberPagination):
    page_size = 2
    page_query_param = "page"
    page_size_query_param = "size"
    max_page_size = 5


'''
"time":1949,"
location":"xxx",
"weather":"sunny",
"temperature":xxx,
"humidity":xxx,
"wind_speed":xxx,
"light":xxx,
"Pa":xxx,
"wind_direction":xxx
'''

class DataMonitor2(APIView):
    #authentication_classes = [MyAuthentication,]
    def get(self,request,*args,**kwargs):
        equipment_id = request.GET.get("equipment_id")
        print("hhhhhh")
        now = datetime.datetime.now()
        time_point1 = datetime.datetime.now() - datetime.timedelta(hours=now.hour, minutes=now.minute)
        time_point2 = time_point1 - datetime.timedelta(days=1)
        t = his.objects.filter(equipment_id_id=equipment_id,y_time__gte=time_point1)
        for a in t:
            if not a.y_AQI:
                if a.y_CO and a.y_PM2_5:
                   a.y_AQI=calculator(PM2_5=a.y_PM2_5,CO=a.y_CO)
                   a.save()
                else:
                   a.y_AQI = 0
                   a.save()
        t = his.objects.filter(equipment_id_id=equipment_id,y_time__range=(time_point2,time_point1))
        for a in t:
            if not a.y_AQI:
                if a.y_CO and a.y_PM2_5:
                    a.y_AQI = calculator(PM2_5=a.y_PM2_5, CO=a.y_CO)
                    a.save()
                else:
                    a.y_AQI = 0
                    a.save()

        t_data = his.objects.filter(equipment_id_id=equipment_id,y_time__gte=time_point1).aggregate(AQI=Avg('y_AQI'),PM10=Avg('y_PM10'),PM2_5=Avg('y_PM2_5'),O2=Avg('y_O3'),SO2=Avg('y_SO2'),NO2=Avg('y_NO2'),CO=Avg('y_CO'))
        y_data = his.objects.filter(equipment_id_id=equipment_id,y_time__range=(time_point2,time_point1)).aggregate(y_AQI=Avg('y_AQI'),y_PM10=Avg('y_PM10'),y_PM2_5=Avg('y_PM2_5'),y_O2=Avg('y_O3'),y_SO2=Avg('y_SO2'),y_NO2=Avg('y_NO2'),y_CO=Avg('y_CO'))
        ret = {}
        ret.update(t_data)
        ret.update(y_data)
        return HttpResponse(json.dumps(ret))



class DataMonitor1(APIView):
    #authentication_classes = [MyAuthentication,]
    def get(self,request,*args,**kwargs):

        n_data = realtime.objects.all()
        pg = MyPagination()
        pager = pg.paginate_queryset(view=self,request=request,queryset=n_data)
        myser = MySerializer(instance=pager, many=True)
        return HttpResponse(json.dumps(myser.data))


class MiniDataMonitor1(APIView):
    #authentication_classes = [MyAuthentication,]
    def get(self, request, *args, **kwargs):
        equipment_id = request.GET.get("equipment_id")
        n_data = realtime.objects.filter(equipment_id=equipment_id).all()

        # pg = MyPagination()
        # pager = pg.paginate_queryset(view=self,request=request,queryset=n_data)
        myser = MySerializer(instance=n_data, many=True)
        return HttpResponse(json.dumps(myser.data))