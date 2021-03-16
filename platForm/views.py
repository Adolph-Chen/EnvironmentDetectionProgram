import datetime

from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import JSONParser, FormParser
from rest_framework.permissions import BasePermission
from rest_framework.serializers import ModelSerializer
from rest_framework.pagination import PageNumberPagination

# Create your views here.

from django.http import HttpResponse
from rest_framework.utils import json
from rest_framework.views import APIView
from utils.sendEmail import SendEmail
from platForm.models import UserInfo,UserTable
from rest_framework_jwt.settings import api_settings


import re

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER

def open(request):
    return render(request,"开放平台首页.html");

class MyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        if request.method == "GET":

            token = request.GET.get("token")
            if not token:
                raise exceptions.AuthenticationFailed("没有token")
            token = token.replace("\"","")
            decode_token = jwt_decode_handler(token)

            obj = UserInfo.objects.filter(username=decode_token.get("username")).first()
            if not obj:
                raise exceptions.AuthenticationFailed("没有该用户")
            else:
                return (obj,None)
        else:
            print("登录")
            return (None,None)

class MyPermission(BasePermission):
    message = "reject"
    def has_permission(self, request, view):
        if request.user.id==2:
            return False;
        else:
            return True
class MySerializer(ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ["username","password"]

class MySerializer1(ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ["username","server_ip","port","request_count","all_count"]

class MySerializer2(ModelSerializer):
    class Meta:
        model = UserTable
        fields = ["request_count","client_ip","request_time"]

class MyPagination(PageNumberPagination):
    page_size_query_param = "size";
    max_page_size = 5;
    page_size = 5;
    page_query_param = "page";


class TokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        pass




class OpenUserLogin(APIView):
    authentication_classes = [MyAuthentication,]
    #permission_classes = [MyPermission,]
    #parser_classes = [JSONParser, FormParser, ]


    def post(self,request,*args,**kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        if username == None or password == None:
            username = request.data.get("user_name")
            password = request.data.get("user_password")
        print(username)
        print(password)
        user = UserInfo.objects.filter(username=username, password=password).first()
        print("xxxx-----------------")
        if not user:

            ret = {
                "code": 410,
                "msg": "用户不存在或密码错误",
            }
            raise exceptions.AuthenticationFailed(HttpResponse(json.dumps(ret)))
        else:

                user1 = UserInfo()
                user1.username = username
                payload = jwt_payload_handler(user1)
                token = jwt_encode_handler(payload)
                ret = {
                    "code": 200,
                    "msg": "succeed",
                    "token": token
                }
                return HttpResponse(json.dumps(ret))



    def get(self,request,*args,**kwargs):
        obj = request.user
        myser1 = MySerializer1(instance=obj,many=False)
        return HttpResponse(json.dumps(myser1.data))


class OpenUserTable(APIView):
    authentication_classes = [MyAuthentication,]

    def get(self,request,*args,**kwargs):

        user = request.user

        tables = UserTable.objects.filter(user_id=user.id)
        pg = MyPagination()
        pager = pg.paginate_queryset(view=self,request=request,queryset=tables)

        myser = MySerializer2(instance=pager,many=True)
        print("-----------------------")
        print(len(myser.data))
        if len(myser.data)==0:
            ret = {
                "code":410,
                "msg":"没有找到"
            }
            return HttpResponse("no")
        else:
            for x in myser.data:
                x["code"] = 200
                x["msg"] = "获得成功"

        return HttpResponse(json.dumps(myser.data),status=200)





class SignUpAuthentication(BaseAuthentication):
    def authenticate(self, request):
        if request.method=="POST":
            username = request.data.get("username")
            password = request.data.get("password")
            if re.match(r'[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z_]{0,19}.com',username):
                tempuser = UserInfo.objects.filter(username=username).first()
                if tempuser:
                    ret = {
                        "code":502,
                        "msg":"用户已存在!"
                    }
                    raise exceptions.AuthenticationFailed(json.dumps(ret))
                else:
                    if len(password) < 6:
                        ret = {
                            "code":504,
                            "msg": "密码长度至少为6位!"
                        }
                        raise exceptions.AuthenticationFailed(json.dumps(ret))
                    else:
                        user = UserInfo.objects.create(username=username, password=password,
                                                       all_count=5000, request_count=0)

                        return (user, None)
            else:
                ret = {
                    "code":503,
                    "msg":"用户名需要为邮箱"
                }
                raise exceptions.AuthenticationFailed(json.dumps(ret))



class OpenUserSignUp(APIView):
    authentication_classes = [SignUpAuthentication,]


    def post(self,request,*args,**kwargs):
        user1 = request.user
        user = UserInfo()
        user.username = user1.username
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        ret = {
            "code":200,
            "msg":"注册成功",
            "token":token
        }
        return HttpResponse(json.dumps(ret))


class ResetPasswordAuthentication(BaseAuthentication):
    def authenticate(self, request):
        if request.method=="POST":
            username = request.data.get("username")
            user = UserInfo.objects.filter(username=username).first()
            if user:
                return (user,None)
            else:
                ret = {
                    "code":500,
                    "msg":"用户不存在!"
                }
                raise exceptions.AuthenticationFailed(json.dumps(ret))
        else:
            ret = {
                "code":400,
                "msg": "请求方法错误"
            }
            raise exceptions.AuthenticationFailed(json.dumps(ret))

class OpenSendMail(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        user1 = UserInfo()
        user1.username = username
        payload = jwt_payload_handler(user1)
        token = jwt_encode_handler(payload)
        SendEmail(username,token).sendEmail()
        ret = {
            "code":200,
            "msg":"发送成功"
        }
        return HttpResponse(json.dumps(ret),status=200)


class OpenResetPassword(APIView):
    #authentication_classes = [ResetPasswordAuthentication,]
    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        token = request.data.get("token")
        user1 = None
        try:
            user1 = jwt_decode_handler(token)
        except Exception as e:
            raise exceptions.AuthenticationFailed(e)

        if user1.get("username")!=username:
            raise exceptions.AuthenticationFailed("用户token不正确")
        if len(password)<6:
            raise exceptions.AuthenticationFailed("密码至少为6位")
        user = UserInfo.objects.filter(username=username).first()
        user.password = password
        user.save()
        ret = {
            "code":200,
            "msg":"重设成功！"
        }
        return HttpResponse(json.dumps(ret),status=200)


from equipment.models import realtime
from rest_framework import serializers
import urllib
class MySerializer(ModelSerializer):
    location = serializers.SerializerMethodField(label='地点')
    class Meta:
        fields = ["n_time","location","weather","temperature","humidity","wind_speed","light","Pa","wind_direction"]
        model = realtime
    def get_location(self,obj):

        loc = obj.location
        if loc:
            y = re.split(r"[),(]", loc)
            url = "http://api.map.baidu.com/reverse_geocoding/v3/?ak=eAMNZ2ifZrKVL1CskD6hpy5HY3nVrVu4&output=json&coordtype=wgs84ll&location="+y[1]+","+y[0]
            # 打开需要爬取的网页
            resp = urllib.request.urlopen(url)
            # 读取网页代码
            html = resp.read()
            x = json.loads(html)
            # 打印读取的内容
            return x.get("result").get("formatted_address")
        else:
            return "无"

class OpenData(APIView):
    #authentication_classes = [MyAuthentication,]
    def post(self,request,*args,**kwargs):
        username = request.POST.get("username")
        password = request.POST.get("password")

        #获得用户的ip
        user_ip = None
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            user_ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            user_ip = request.META['REMOTE_ADDR']

        now = datetime.datetime.now()




        user = UserInfo.objects.filter(username=username,password=password).first()
        if not user:
            ret = {
                "code": 410,
                "msg": "账户或者密码错误！"
            }
            return HttpResponse(json.dumps(ret))

        UserTable.objects.create(user_id=user.id,request_time=now,request_count=1,client_ip=user_ip)
        user.request_count = user.request_count + 1
        user.save()
        n_data = realtime.objects.all()
        myser = MySerializer(instance=n_data, many=True)
        return HttpResponse(json.dumps(myser.data))