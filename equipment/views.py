import re
import urllib

from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from requests import Response
from rest_framework.serializers import ModelSerializer

from equipment import  myserializers
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import BaseAuthentication
from rest_framework_jwt.settings import api_settings

from utils.sendCmd import SendCmd
from .models import info,his
from user.models import info as userinfo
from rest_framework import exceptions, status
from rest_framework.utils import json
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from workArea.models import manage

jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
from rest_framework import serializers

class GoodsPagination(PageNumberPagination):
    page_size = 3                       #每页的记录数
    page_size_query_param = 'page_size'   #获取url参数中设置的每页显示数据条数
    page_query_param = "page"                #传递的参数：页码
    max_page_size = 20


class equipmentAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.data.get("token")
        if not token:
            token = request.query_params.get("token")
        if not token:
            raise exceptions.AuthenticationFailed("没有token")
        token = token.replace("\"","")
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



class equipmentView(APIView):
    authentication_classes = [equipmentAuthentication,]
    #serializer_class = myserializers.equipmentSerialzer
    pagination_class = GoodsPagination
    def get(self,request,*args,**kwargs):
        work = info.objects.filter(equipment_frozen=False)
        pg = GoodsPagination()
        pager = pg.paginate_queryset(view = self,request = request,queryset=work)
        print("------------")
        print(pager)
        print("------------")
        myser = myserializers.equipmentSerialzer(instance=pager, many=True)
        print(myser.data)
        return HttpResponse(json.dumps(myser.data))
    def put(self,request,*args,**kwargs):
        equipment_id = request.data.get("equipment_id")
        work = info.objects.filter(equipment_id=equipment_id).first()
        if not work:
            ret = {
                "code": 410,
                "msg": "找不到"
            }
            return HttpResponse(json.dumps(ret))
        work.workArea_id = request.data.get("workArea_id", work.workArea_id)
        work.data_PM10 = request.data.get("data_PM10", work.data_PM10)
        work.data_O3 = request.data.get("data_O3", work.data_O3)
        work.data_SO2 = request.data.get("data_SO2", work.data_SO2)
        work.data_NO2 = request.data.get("data_NO2", work.data_NO2)
        work.data_CO = request.data.get("data_CO", work.data_CO)
        work.data_PM2_5 = request.data.get("data_PM2_5", work.data_PM2_5)
        work.save()
        th = SendCmd(option="updateconf", serialnum=equipment_id)
        th.start()
        ret = {
            "code": 200,
            "msg": "保存成功"
        }
        return HttpResponse(json.dumps(ret))
        #work.data_PM2_5 = request.data.get("data_PM2_5", work.data_PM2_5)
        #myser = myserializers.equipmentSerialzer(instance=work, data=request.data)
        # if myser.is_valid():
        #     try:
        #         myser.save()
        #     except Exception as e:
        #         print(e)
        #         ret = {
        #             "code": 410,
        #             "msg": "更新失败"
        #         }
        #         return HttpResponse(e)
        #     ret = {
        #         "code": 200,
        #         "msg": "更新成功"
        #     }
        #     return HttpResponse(json.dumps(ret))
        # else:

    def delete(self,request,*args,**kwargs):
        equipment_id = request.data.get("equipment_id")
        work = info.objects.filter(equipment_id=equipment_id).first()
        if not work:
            ret = {
                "code":410,
                "msg":"设备不存在"
            }
            return HttpResponse(json.dumps(ret))
        else:
            work.equipment_frozen = True
            work.save()
            ret = {
                "code": 200,
                "msg": "删除成功"
            }
            return HttpResponse(json.dumps(ret))



class SearchEquipment(APIView):
    authentication_classes = [equipmentAuthentication]
    def get(self,request,*args,**kwargs):
        #模糊查询工程名字
        workArea_id = request.query_params.get("workArea_id")
        work = info.objects.filter(workArea_id=workArea_id,equipment_frozen=False)
        if work.not_valid():
            work1 = manage.objects.filter(workArea_name=workArea_id)
            work = info.objects.filter(workArea_id=work1.first().workArea_id, equipment_frozen=False)
        pg = GoodsPagination()
        pager = pg.paginate_queryset(view=self, request=request, queryset=work)
        myser = myserializers.equipmentSerialzer(instance=pager, many=True)
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
    # authentication_classes = [CensusAuthentication,]
    def get(self,request,*args,**kwargs):
        ret = {
            "code":200,
            "msg":"获取成功",
            "equipment_num":len(info.objects.filter(equipment_frozen=False)),
            "equipment_online_num":len(info.objects.filter(equipment_frozen=False,online_status=True))
        }
        return HttpResponse(json.dumps(ret))





class MiniequipmentAuthentication(BaseAuthentication):
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
            # else:
            #     if user.user_permission=="user":
            #         ret = {
            #             "code": 410,
            #             "msg": "权限不够"
            #         }
            #         raise exceptions.AuthenticationFailed(ret)
            else:
                return (user, None)


class MiniequipmentView(APIView):
    authentication_classes = [MiniequipmentAuthentication]
    def get(self,request,*args,**kwargs):
        work = info.objects.filter(equipment_frozen=False).all()
        pr = MySerializer(instance=work,many=True)

        ret = {
            "code": 200,
            "msg": "获取成功",
            "data":pr.data,
            # "location":myser.data
        }
        return HttpResponse(json.dumps(ret))

        # work = info.objects.filter( equipment_frozen=False).values("equipment_id","online_status","long_lat_itude")
        # # myser = work.his_set.values("location")
        # myser = serializers.MiniSerialzer(data=work,many=True)
        #
        # return HttpResponse(json.dumps(myser))


class MySerializer(ModelSerializer):
    location = serializers.SerializerMethodField(label='地点')
    longitude = serializers.SerializerMethodField(label='经度')
    latitude = serializers.SerializerMethodField(label='纬度')
    class Meta:
        fields = ['equipment_id', 'workArea_id', "location", 'online_status', 'last_login_time',"longitude","latitude"]
        model = info

    def get_location(self, obj):

        loc = obj.long_lat_itude
        if loc:
            # print(loc)
            y = re.split(r"[),(]", loc)
            url = "http://api.map.baidu.com/reverse_geocoding/v3/?ak=eAMNZ2ifZrKVL1CskD6hpy5HY3nVrVu4&output=json&coordtype=wgs84ll&location=" + \
                  y[1] + "," + y[0]
            # 打开需要爬取的网页
            resp = urllib.request.urlopen(url)
            # 读取网页代码
            html = resp.read()
            x = json.loads(html)
            # 打印读取的内容
            return x.get("result").get("formatted_address")
        else:
            return "无"
    def get_longitude(self,obj):
        loc = obj.long_lat_itude
        if loc:
            # print(loc)
            y = re.split(r"[),(]", loc)


            return y[0]
        else:
            return "无"
    def get_latitude(self,obj):
        loc = obj.long_lat_itude
        if loc:
            # print(loc)
            y = re.split(r"[),(]", loc)

            return y[1]
        else:
            return "无"



class MySerializer1(ModelSerializer):
    class Meta:
        fields = ['workArea_id','duty_person']
        model = manage


# class MiniGetOneView(APIView):
#     authentication_classes = [MiniequipmentAuthentication]
#     def get(self, request, *args, **kwargs):
#         device_id = request.data.get('equipment_id')
#         workArea_id = request.data.get('workArea_id')
#         # work=info.objects.filter(equipment_id=device_id).first()
#         # person = manage.objects.filter(workArea_id=work.workArea_id).first().only('duty_person')
#         person = manage.objects.filter(workArea_id=workArea_id).first()
#         res = info.objects.filter(equipment_id=device_id).all()
#         myser = MySerializer(instance=res, many=True)
#         person = MySerializer1(instance=person,many=True)
#         ret = {}
#         ret.update(myser.data)
#         ret.update(person.data)
#         if not res:
#             ret={
#                 "code": 410,
#                 "msg": "设备不存在"
#             }
#             raise exceptions.AuthenticationFailed(ret)
#         # return HttpResponse(json.dumps(myser.data))
#         return JsonResponse(ret,safe=False)
class MiniGetOneView(APIView):
    # authentication_classes = [MiniequipmentAuthentication]
    def get(self, request, *args, **kwargs):
        device_id = request.query_params.get('equipment_id')
        # work=info.objects.filter(equipment_id=device_id).first()
        # person = manage.objects.filter(workArea_id=work.workArea_id).first().only('duty_person')
        res = info.objects.filter(equipment_id=device_id).first()
        myser = MySerializer(instance=res, many=False)
        workArea_id = res.workArea_id
        if  workArea_id:
            ma = manage.objects.filter(workArea_id=workArea_id).first()
            duty_person = ma.duty_person
            dict1 = dict(myser.data)
            dict1["duty_person"] = duty_person
            return HttpResponse(json.dumps(dict1))
        else:
            return HttpResponse(json.dumps(myser.data))

class GetequipmentList(APIView):
    #authentication_classes = [MiniequipmentAuthentication]
    def get(self, request, *args, **kwargs):
        equipment = info.objects.filter(equipment_frozen=False).all()
        ret = MySerializer2(instance=equipment, many=True)
        return HttpResponse(json.dumps(ret.data))


class MySerializer2(ModelSerializer):
    longitude = serializers.SerializerMethodField(label='经度')
    latitude = serializers.SerializerMethodField(label='纬度')
    class Meta:
        fields = ["equipment_id","longitude","latitude"]
        model = info

    def get_longitude(self, obj):
        loc = obj.long_lat_itude
        if loc:
            # print(loc)
            y = re.split(r"[),(]", loc)

            return y[0]
        else:
            return "无"

    def get_latitude(self, obj):
        loc = obj.long_lat_itude
        if loc:
            # print(loc)
            y = re.split(r"[),(]", loc)

            return y[1]
        else:
            return "无"


########################################################################################
