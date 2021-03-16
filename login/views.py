from django.shortcuts import render

# Create your views here.
from rest_framework import exceptions
from rest_framework.utils import json
from rest_framework.views import APIView

from user.models import info as userinfo
from django.http import HttpResponse
from rest_framework_jwt.settings import api_settings

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER

'''
{
  "code":200,
  "msg":"successed"
  "token":token
}
'''
class LoginView(APIView):
    def post(self,request,*args,**kwargs):
        username = request.POST.get("user_name")
        password = request.POST.get("user_password")
        if username==None or password==None:
            username = request.data.get("user_name")
            password = request.data.get("user_password")
        print(username)
        print(password)
        user = userinfo.objects.filter(username=username, password=password).first()
        print("xxxx-----------------")
        if not user:

            ret = {
                "code": 410,
                "msg": "用户不存在或密码错误",
            }
            raise exceptions.AuthenticationFailed(HttpResponse(json.dumps(ret)))
        else:
            if user.user_frozen == True:
                ret = {
                    "code": 400,
                    "msg": "用户已冻结"
                }
                raise exceptions.AuthenticationFailed(HttpResponse(json.dumps(ret)))
            else:
                user1 = userinfo()
                user1.username = username
                payload = jwt_payload_handler(user1)
                token = jwt_encode_handler(payload)
                ret = {
                    "code": 200,
                    "msg": "succeed",
                    "token": token
                }
                return HttpResponse(json.dumps(ret))



class LogoutView(APIView):
    def post(self,request,*args,**kwargs):
        # 这里就不进行操作了  让前端把存在浏览器的缓存里删掉
        ret = {
            "code": 200,
            "msg": "successed"
        }
        return HttpResponse(json.dumps(ret))
