from django.shortcuts import render

# Create your views here.
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication
from rest_framework.serializers import ModelSerializer
from rest_framework.utils import json
from rest_framework.views import APIView
from user.models import info as userinfo
from rest_framework_jwt.settings import api_settings
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
from django.http import HttpResponse
from rest_framework.pagination import PageNumberPagination


class UserAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.data.get("token")
        if not token:
            token = request.query_params.get("token")
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
        fields = ["password","user_permission","username"]

    def update(self, instance, validated_data):
        instance.password = validated_data.get("password", instance.password)
        instance.username = validated_data.get("username", instance.username)
        instance.user_permission = validated_data.get("user_permission", instance.user_permission)
        instance.save()
        return instance

class MyPagination(PageNumberPagination):
    page_size_query_param = "size"
    page_query_param = "page"
    page_size = 5
    max_page_size = 5

class Authority(APIView):
    authentication_classes = [UserAuthentication,]
    def get(self, request, *args, **kwargs):
        user = userinfo.objects.all()
        pg = MyPagination()
        pager = pg.paginate_queryset(view=self,request=request,queryset=user)
        myser = Myserializer1(instance=pager,many=True)
        return HttpResponse(json.dumps(myser.data))
    def delete(self, request, *args, **kwargs):
        username = request.data.get("username")
        user = userinfo.objects.filter(username=username).first()
        user.user_frozen = True
        user.save()
        ret = {
            "code":200,
            "msg":"冻结成功"
        }
        return HttpResponse(json.dumps(ret))

    def put(self, request, *args, **kwargs):
        username = request.data.get("username")
        print(username)
        user = userinfo.objects.filter(username=username).first()
        myser = Myserializer1(instance=user,data=request.data)
        if myser.is_valid():
            try:
                myser.save()
            except Exception as e:
                ret = {
                    "code": 400,
                    "msg": e
                }
                return HttpResponse(json.dumps(ret))
            ret = {
                "code": 200,
                "msg": "跟新成功"
            }
            return HttpResponse(json.dumps(ret))
        else:
            ret = {
                "code": 400,
                "msg": "格式不正确"
            }
            return HttpResponse(json.dumps(ret))