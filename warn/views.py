import datetime

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from rest_framework import exceptions, serializers
from rest_framework.authentication import BaseAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.utils import json
from rest_framework.views import APIView
from user.models import info as userinfo
from rest_framework_jwt.settings import api_settings
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
from .models import warning
from rest_framework.serializers import ModelSerializer
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


class WarnNum(APIView):
    def get(self,request,*args,**kwargs):
        warnings = warning.objects.filter(deal=False)
        ret = {
            "code":200,
            "msg":"获取成功",
            "warn_num":len(warnings)
        }
        return HttpResponse(json.dumps(ret))

class MySerializer(ModelSerializer):
    class Meta:
        fields = ["workName",]
        model = warning

class NoDealWarn(APIView):
    def get(self, request, *args, **kwargs):
        warnings = warning.objects.filter(deal=False)
        myser = MySerializer(instance=warnings,many=True)
        return HttpResponse(json.dumps(myser.data))


'''
{"warn_id":xxx,
"equip":equipemnt_id,
"workName":workName,
"time":time,
"locaton":location,
"warn_type":type,
"warn_value":value,
"deal":yes/no,
"dealPerson":name,
"dealPersonPhone":110,
"dealTime":time,
"remark":"xxx"}
'''
class MyPagination(PageNumberPagination):
    page_size = 3
    page_query_param = "page"
    page_size_query_param = "size"
    max_page_size = 8

import re
import urllib
class MySerializer1(ModelSerializer):
    location = serializers.SerializerMethodField(label='地点')
    class Meta:
        fields = ["warn_id","equip","workName","warn_time","location","warn_type","warn_value","deal","dealPerson","dealPersonPhone","dealTime","remark"]
        #read_only_fields = ('warn_id',)
        model = warning

    def get_location(self, obj):

        loc = obj.location
        if loc:
            # print(loc)
            y = re.split(r"[),(]", loc)
            print(y)
            url = "http://api.map.baidu.com/reverse_geocoding/v3/?ak=eAMNZ2ifZrKVL1CskD6hpy5HY3nVrVu4&output=json&coordtype=wgs84ll&location=" + \
                  y[1] + "," + y[0]
            # 打开需要爬取的网页
            resp = urllib.request.urlopen(url)
            # 读取网页代码
            html = resp.read()
            x = json.loads(html)
            # 打印读取的内容
            return x.get("result").get("formatted_address")
            # return "gggggggg"
        else:
            return "无"


'''
{"token":token,"warn_id":xxx,
"dealPerson":name,"dealPerPhone":110,"dealTime":time,"remark":"xxx"}
'''
class MySerializer2(ModelSerializer):
    class Meta:
        fields = ["warn_id","dealPerson","dealPersonPhone","remark"]
        read_only_fields = ('warn_id',)
        model = warning
    def update(self, instance, validated_data):
        instance.deal = True
        instance.dealPerson = validated_data.get("dealPerson",instance.dealPerson)
        instance.dealPersonPhone = validated_data.get("dealPersonPhone", instance.dealPersonPhone)
        instance.warn_time = datetime.datetime.now()
        instance.remark = validated_data.get("remark", instance.remark)
        instance.save()
        return instance

class Warn(APIView):
    def get(self, request, *args, **kwargs):
        warnings = warning.objects.all()
        pg = MyPagination()
        pager = pg.paginate_queryset(view=self,request=request,queryset=warnings)
        myser = MySerializer1(instance=pager,many=True)
        return HttpResponse(json.dumps(myser.data))
    def put(self, request, *args, **kwargs):
        warn_id = request.data.get("warn_id")
        if not warn_id:
            ret = {
                "code":400,
                "msg":"格式错误"
            }
            return HttpResponse(json.dumps(ret))
        else:
            a_warn = warning.objects.filter(warn_id=warn_id).first()
            if not a_warn:
                ret = {
                    "code": 410,
                    "msg": "找不到"
                }
                return HttpResponse(json.dumps(ret))
            else:
                myser = MySerializer2(instance=a_warn,data=request.data)
                if myser.is_valid():
                    myser.save()
                    ret = {
                        "code":200,
                        "msg":"保存成功"
                    }
                    return HttpResponse(json.dumps(ret))
                else:
                    myser.save()
                    ret = {
                        "code": 400,
                        "msg": "数据格式不正确"
                    }
                    return HttpResponse(json.dumps(ret),status=400)


class MiniMySerializer(ModelSerializer):
    location = serializers.SerializerMethodField(label='地点')
    class Meta:
        fields = ["warn_id","warn_type","warn_time","location"]
        model = warning
    def get_location(self, obj):

        loc = obj.location
        if loc:
            # print(loc)
            y = re.split(r"[),(]", loc)
            print(y)
            url = "http://api.map.baidu.com/reverse_geocoding/v3/?ak=eAMNZ2ifZrKVL1CskD6hpy5HY3nVrVu4&output=json&coordtype=wgs84ll&location=" + \
                  y[1] + "," + y[0]
            # 打开需要爬取的网页
            resp = urllib.request.urlopen(url)
            # 读取网页代码
            html = resp.read()
            x = json.loads(html)
            # 打印读取的内容
            return x.get("result").get("formatted_address")
            return "gggggggg"
        else:
            return "无"

class MiniNoDealWarn(APIView):
    def get(self, request, *args, **kwargs):
        warnings = warning.objects.filter(deal=False)
        myser = MiniMySerializer(instance=warnings,many=True)
        return HttpResponse(json.dumps(myser.data))


class MiniWarnSearch(APIView):
    def get(self, request, *args, **kwargs):
        equip_id = request.GET.get("equip_id",None)
        print(equip_id)
        if not equip_id:
            warnings = warning.objects.all()
        else:
            print("-----------")
            warnings = warning.objects.filter(equip_id=equip_id)

        print(warnings)
        pg = MyPagination()
        #pager = pg.paginate_queryset(view=self,request=request,queryset=warnings)
        myser = MySerializer1(instance=warnings,many=True)
        return HttpResponse(json.dumps(myser.data))

class MiniWarn(APIView):
    def get(self, request, *args, **kwargs):
        warn_id = request.GET.get("warn_id")
        warnings = warning.objects.filter(warn_id=warn_id).first()

        myser = MySerializer1(instance=warnings,many=False)
        return HttpResponse(json.dumps(myser.data))