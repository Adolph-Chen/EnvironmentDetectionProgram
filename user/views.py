from django.shortcuts import render

# Create your views here.
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication
from rest_framework.serializers import ModelSerializer
from rest_framework.utils import json
from rest_framework.views import APIView
from .models import info as userinfo
from rest_framework_jwt.settings import api_settings
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
from django.http import HttpResponse
from rest_framework.pagination import PageNumberPagination

class UserAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.data.get("token")

        if not token:
            token = request.query_params.get("token")
            print(token)
        if not token:
            token = request.POST.get("token")
            print(token)
        if not token:
            raise exceptions.AuthenticationFailed("没有token")
        token = token.replace("\"", "")


        user1 = jwt_decode_handler(token)

        user = userinfo.objects.filter(username=user1.get("username")).first()
        if not user:
            ret = {
                "code":410,
                "msg":"用户不存在"
            }
            raise exceptions.AuthenticationFailed(ret)

        else:
            if user.user_frozen==True:
                ret = {
                    "code": 400,
                    "msg": "用户已经冻结"
                }
                raise exceptions.AuthenticationFailed(ret)
            else:
                if user.user_permission=="user" or user.user_permission=="admin":
                    ret = {
                        "code": 410,
                        "msg": "权限不够"
                    }
                    raise exceptions.AuthenticationFailed(ret)
                else:
                    return (user, None)

class Myserializer1(ModelSerializer):
    class Meta:
        model = userinfo
        exclude = ["password",]
        extra_kwargs = {  # 类似于这种形式name=serializers.CharField(max_length=16,min_length=4)
            'user_permission': {'read_only': True},
        }
    def validate(self, attrs):
        return attrs
    def create(self, validated_data):
        user = userinfo(**validated_data)
        user.save()
        return user
    def update(self, instance, validated_data):
        instance.user_workid = validated_data.get("user_workid", instance.user_workid)
        print(instance.user_workid)
        #instance.password = validated_data.get("password", instance.password)
        instance.username = validated_data.get("username", instance.username)
        print(instance.username)
        instance.name = validated_data.get("name", instance.name)
        print(instance.name)
        instance.sex = validated_data.get("sex", instance.sex)
        print(instance.sex)
        instance.telephone_number = validated_data.get("telephone_number", instance.telephone_number)
        print(instance.telephone_number)
        instance.user_mail = validated_data.get("user_mail", instance.user_mail)
        print(instance.user_mail)
        instance.user_permission = validated_data.get("user_permission", instance.user_permission)
        print(instance.user_permission)
        temp = validated_data.get("user_frozen")
        print(temp)
        if temp==True:
            temp=True
        else:
            temp=False
        instance.user_frozen = temp
        #, instance.user_frozen instance.user_frozen
        instance.save()
        return instance

class MyPagination(PageNumberPagination):
    page_size_query_param = "size"
    page_query_param = "page"
    page_size = 5
    max_page_size = 5
class User(APIView):
    authentication_classes = [UserAuthentication,]
    def get(self,request,*args,**kwargs):
        users = userinfo.objects.all()
        pg = MyPagination()
        pager = pg.paginate_queryset(view=self,request=request,queryset=users)
        myser = Myserializer1(instance=pager,many=True)
        return HttpResponse(json.dumps(myser.data))

    def post(self,request,*args,**kwargs):
        myser = Myserializer1(data=request.data)
        if myser.is_valid():
            myser.save()
            ret = {
                "code": 200,
                "msg": "保存成功"
            }
            return HttpResponse(json.dumps(ret))
        else:
            ret = {
                "code": 400,
                "msg": "信息格式不正确"
            }
            return HttpResponse(json.dumps(ret))
    def put(self,request,*args,**kwargs):
        user_workid = request.data.get("user_workid")
        user = userinfo.objects.filter(user_workid=user_workid).first()
        print(request.data)
        myser = Myserializer1(instance=user,data = request.data)
        if myser.is_valid():
            try:
                myser.save()
            except Exception as e:
                ret = {
                    "code":410,
                    "msg":e
                }
                return HttpResponse(json.dumps(ret))
            ret = {
                "code":200,
                "msg":"保存成功"
            }
            return HttpResponse(json.dumps(ret))
        else:
            ret = {
                "code":400,
                "msg":"信息格式不正确"
            }
            return HttpResponse(json.dumps(ret))
    def delete(self,request,*args,**kwargs):
        user_workid = request.data.get("user_workid")
        print(user_workid)
        user = userinfo.objects.filter(user_workid=user_workid).first()
        if not user:
            ret = {
                "code": 410,
                "msg": "找不到用户"
            }
            return HttpResponse(json.dumps(ret),status=410)
        else:
            user.user_frozen = True
            user.save()
            ret = {
                "code": 200,
                "msg": "修改成功"
            }
            return HttpResponse(json.dumps(ret),status=200)

class UserSearch(APIView):
    authentication_classes = [UserAuthentication, ]
    def get(self,request,*args,**kwargs):
        search = None
        sex = None
        frozen = None

        search = request.GET.get("search","-1")
        print(search)
        sex = request.GET.get("sex")
        frozen = request.GET.get("frozen")
        if search == "-1":
            search = ""
        if sex == "-1":
            sex = ""
        if frozen == "-1":
            frozen = None


        user = None




        if frozen==None:
            user = userinfo.objects.filter(sex__contains=sex,username__contains=search)
        else:
            if frozen=="0":
                user = userinfo.objects.filter(sex__contains=sex, username__contains=search,user_frozen=False)
            else:
                user = userinfo.objects.filter(sex__contains=sex, username__contains=search,user_frozen=True)
        pg = MyPagination()
        pager = pg.paginate_queryset(view=self,request=request,queryset=user)
        myser = Myserializer1(instance=pager,many=True)
        return HttpResponse(json.dumps(myser.data))


class Myserializer2(ModelSerializer):
    class Meta:
        model = userinfo
        fields = ['user_workid','username','name','sex','telephone_number','user_mail']


class MiniUser(APIView):
    #authentication_classes = [UserAuthentication, ]
    def get(self,request,*args,**kwargs):
        username=request.GET.get("username")
        users = userinfo.objects.filter(username=username).first()
        myser = Myserializer2(instance=users)
        print(myser.data)
        return HttpResponse(json.dumps(myser.data))