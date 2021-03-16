import datetime

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.serializers import ModelSerializer
from rest_framework.utils import json
from rest_framework.views import APIView
from user.models import info as userinfo
from rest_framework_jwt.settings import api_settings
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
from .models import journal
class MyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.GET.get("token")
        if not token:
            token = request.data.get("token")
        if not token:
            token = request.query_params.get("token")
        if not token:
            raise exceptions.AuthenticationFailed("没有token")
        else:
            print(token)
            print(request.data.get("diary_id"))


            token = token.replace("\"", "")
            user = jwt_decode_handler(token)

            user1 = userinfo.objects.filter(username=user.get("username")).first()
            if not user1:
                ret = {
                    "code":410,
                    "msg":"用户不存在"
                }
                raise exceptions.AuthenticationFailed(json.dumps(ret))
            else:
                if user1.user_frozen:
                    ret = {
                        "code": 400,
                        "msg": "用户已经冻结"
                    }
                    raise exceptions.AuthenticationFailed(ret)
                else:

                    if user1.user_permission=="admin" or user1.user_permission=="user":
                        if request.method == "DELETE":
                            ret = {
                                "code": 410,
                                "msg": "权限不足"
                            }
                            raise exceptions.AuthenticationFailed(json.dumps(ret))
                        else:
                            return (user1,None)
                    else:
                        return (user1,None)

'''
"user_name":"cyx"
  "user_ip":"192.168.0.1"
  "model":"工程管理"
  "require_time":"2020/7/17 14:28"
  "diary_id":123456
'''

class MyPagination(PageNumberPagination):
    page_size = 5
    page_query_param = "page"
    page_size_query_param = "size"
    max_page_size = 5
class MySerializer1(ModelSerializer):
    class Meta:
        fields = ["user_name","user_ip","model","require_time","diary_id"]
        #read_only_fields = ('warn_id',)
        model = journal

class Diary(APIView):
    authentication_classes = [MyAuthentication,]
    def get(self,request,*args,**kwargs):
        diary = journal.objects.all()
        pg = MyPagination()
        pager = pg.paginate_queryset(view=self,request=request,queryset=diary)
        myser = MySerializer1(instance=pager,many=True)
        print(myser.data)
        return HttpResponse(json.dumps(myser.data))

    def delete(self,request,*args,**kwargs):
        diary_id = request.data.get("diary_id")
        print(diary_id)
        diary = journal.objects.filter(diary_id=diary_id).first()
        if not diary:
            ret = {
                "code":410,
                "msg":"日志不存在"
            }
            return HttpResponse(json.dumps(ret))
        else:
            diary.delete()
            ret = {
                "code": 200,
                "msg": "删除成功"
            }
            return HttpResponse(json.dumps(ret))
    def post(self, request, *args, **kwargs):
        user_ip = None
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            user_ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            user_ip = request.META['REMOTE_ADDR']
        model = request.data.get("model")
        require_time = datetime.datetime.now()
        user_name = request.user.username
        #user_name = request.data.get("username")
        journal.objects.create(user_ip=user_ip,model=model,require_time=require_time,user_name=user_name)
        ret = {
            "code":200,
            "msg":"创建成功"
        }
        return HttpResponse(json.dumps(ret))

    #这里用来搜索
    # def put(self, request, *args, **kwargs):
    #     user_name = request.data.get("username","")
    #     print(user_name)
    #     diary = journal.objects.filter(user_name__contains=user_name)
    #     pg = MyPagination()
    #     pager = pg.paginate_queryset(view=self, request=request, queryset=diary)
    #     myser = MySerializer1(instance=pager, many=True)
    #     return HttpResponse(json.dumps(myser.data))