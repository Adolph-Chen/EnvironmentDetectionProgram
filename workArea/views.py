from django.shortcuts import render

# Create your views here.
from rest_framework import exceptions
from rest_framework.utils import json
from rest_framework.views import APIView
from rest_framework.serializers import ModelSerializer
from rest_framework.authentication import BaseAuthentication
from rest_framework.pagination import PageNumberPagination

from utils.sendCmd import SendCmd
from .models import manage as WorkAreaModel
from .models import load as BindEquipment
from equipment.models import info as EquipmentInfo
from django.http import HttpResponse

from rest_framework_jwt.settings import api_settings

jwt_decode_handler = api_settings.JWT_DECODE_HANDLER

'''
{
"token":token,
"workArea_id"id,
"workArea_name":name,
"workArea_type":xxx,
"long_lat_itude":(xxx,xxx),
"area_size":xxx,
"time":xxx,
"location":xxx,
"status":xxx,
"duty_person":xxx
"company":xxx
}
'''

from user.models import info as userinfo

class WorkAreaAuthentication(BaseAuthentication):
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
                if user.user_permission=="user":
                    ret = {
                        "code": 410,
                        "msg": "权限不够"
                    }
                    raise exceptions.AuthenticationFailed(ret)
                else:
                    return (user, None)


class WorkAreaSerializer(ModelSerializer):
    class Meta:
        model = WorkAreaModel
        fields = ["workArea_id","workArea_name","workArea_type","long_lat_itude","area_size","workArea_time","location","workArea_status","duty_person","company"]
        #exclude = ["time",]
    def validate(self, attrs):

        return attrs
    def create(self, validated_data):
        print(validated_data)
        work = WorkAreaModel(**validated_data)
        work.save()
        return work
    def update(self, instance, validated_data):

        instance.workArea_id = validated_data.get("workArea_id",instance.workArea_id)
        instance.workArea_name = validated_data.get("workArea_name", instance.workArea_name)
        instance.workArea_type = validated_data.get("workArea_type",instance.workArea_type)
        instance.long_lat_itude = validated_data.get("long_lat_itude", instance.long_lat_itude)
        instance.area_size = validated_data.get("area_size",instance.area_size)
        instance.workArea_time = validated_data.get("workArea_time",instance.workArea_time)
        instance.location = validated_data.get("location",instance.location)
        instance.workArea_status = validated_data.get("workArea_status",instance.workArea_status)
        instance.duty_person = validated_data.get("duty_person",instance.duty_person)
        instance.company = validated_data.get("company",instance.company)
        instance.save()
        return instance

class MyPagination(PageNumberPagination):
    page_size = 5
    page_query_param = "page"
    page_size_query_param = "size"
    max_page_size = 5

class WorkArea(APIView):
    authentication_classes = [WorkAreaAuthentication,]

    def post(self,request,*args,**kwargs):
        print(request.data)
        myser = WorkAreaSerializer(data=request.data)
        if myser.is_valid():
            try:
                myser.save()
            except Exception as e:
                print(e)
                ret = {
                    "code": 410,
                    "msg": "工程id已经存在"
                }
                return HttpResponse(json.dumps(ret))
            ret = {
                "code":200,
                "msg":"添加成功"
            }
            return HttpResponse(json.dumps(ret))
        else:
            ret = {
                "code":500,
                "msg":"数据添加失败"
            }
            return HttpResponse(json.dumps(ret))

    def get(self,request,*args,**kwargs):
        work = WorkAreaModel.objects.filter(workArea_frozen=False)
        print("hhhhhh")
        pg = MyPagination()
        pager = pg.paginate_queryset(view = self,request = request,queryset = work)
        print("------------")
        print(pager)
        print("------------")
        myser = WorkAreaSerializer(instance=pager,many=True)
        print(myser.data)

        work1 = WorkAreaModel.objects.filter(company__contains="")
        print(work1)
        return HttpResponse(json.dumps(myser.data))

    def put(self,request,*args,**kwargs):
        workArea_id = request.data.get("workArea_id")
        work = WorkAreaModel.objects.filter(workArea_id=workArea_id).first()

        myser = WorkAreaSerializer(instance=work,data=request.data)
        if myser.is_valid():
            try:
                myser.save()
            except Exception as e:
                print(e)
                ret = {
                    "code": 410,
                    "msg": "跟新失败"
                }
                return HttpResponse(json.dumps(ret))
            ret = {
                "code": 200,
                "msg": "跟新成功"
            }
            return HttpResponse(json.dumps(ret))
        else:
            ret = {
                "code":400,
                "msg":"信息格式不正确"
            }
            return HttpResponse(json.dumps(ret))
    def delete(self,request,*args,**kwargs):
        workArea_id = request.data.get("workArea_id")
        work = WorkAreaModel.objects.filter(workArea_id=workArea_id).first()
        if not work:
            ret = {
                "code":410,
                "msg":"工程不存在"
            }
            return HttpResponse(json.dumps(ret))
        else:
            work.workArea_frozen = True
            work.save()
            ret = {
                "code": 200,
                "msg": "删除成功"
            }
            return HttpResponse(json.dumps(ret))
class WorkAreaBind(APIView):
    authentication_classes = [WorkAreaAuthentication,]

    def post(self,request,*args,**kwargs):
        equipment_id = request.data.get("equipment_id")
        equipment_password = request.data.get("equipment_password")
        workArea_id = request.data.get("workArea_id")
        bind = request.data.get("bind")

        bind_status = True
        if bind=="0":
            bind_status = False
            workArea_id = -1
        if equipment_id and equipment_password and workArea_id:
            bind1 = BindEquipment.objects.filter(equipment_id_id=equipment_id).first()

            if not bind1:
                ret = {
                    "code":410,
                    "msg":"设备不存在"
                }
                return HttpResponse(json.dumps(ret))
            else:
                bind2 = BindEquipment.objects.filter(equipment_id_id=equipment_id,
                                                     equipment_password=equipment_password).first()
                if not bind2:
                    ret = {
                        "code": 411,
                        "msg": "密码错误"
                    }
                    return HttpResponse(json.dumps(ret))
                else:
                    equip = EquipmentInfo.objects.filter(equipment_id=equipment_id).first()
                    equip.workArea_id = workArea_id
                    equip.bind = bind_status
                    equip.save()
                    th = SendCmd(option="active",serialnum=equipment_id)
                    th.start()
                    ret = {
                        "code": 200,
                        "msg": "绑定/解绑成功"
                    }
                    return HttpResponse(json.dumps(ret))

        else:
            ret = {
                "code":400,
                "msg":"信息格式有误"
            }
            return HttpResponse(json.dumps(ret))

class SearchWorkArea(APIView):
    authentication_classes = [WorkAreaAuthentication,]
    def get(self,request,*args,**kwargs):
        #模糊查询工程名字
        workArea_name = request.query_params.get("workArea_name")
        work = WorkAreaModel.objects.filter(workArea_name__contains=workArea_name)
        pg = MyPagination()
        pager = pg.paginate_queryset(view=self, request=request, queryset=work)
        myser = WorkAreaSerializer(instance=pager, many=True)
        return HttpResponse(json.dumps(myser.data))


class CensusAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.data.get("token")
        if not token:
            token = request.query_params.get("token")
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
                return (user, None)

class Census(APIView):
    #authentication_classes = [CensusAuthentication,]
    def get(self,request,*args,**kwargs):
        ret = {
            "code":200,
            "msg":"获取成功",
            "workArea_num":len(WorkAreaModel.objects.all())
        }
        return HttpResponse(json.dumps(ret))

class ActiveSerializer(ModelSerializer):
    class Meta:
        fields = ["workArea_name",]
        model = WorkAreaModel
    def validate(self, attrs):
        return attrs

class Active(APIView):
    #authentication_classes = [CensusAuthentication,]
    def get(self,request,*args,**kwargs):
        work = WorkAreaModel.objects.filter(workArea_status=True)
        myser = ActiveSerializer(instance=work,many=True)

        return HttpResponse(json.dumps(myser.data))