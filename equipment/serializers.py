from rest_framework import serializers
from equipment import models
import datetime
import random

from rest_framework.exceptions import APIException

class ServiceUnavailable(APIException):
    status_code = 503
    default_detail = 'Service temporarily unavailable, try again later.'
    default_code = 'service_unavailable'


class equipmentSerialzer(serializers.ModelSerializer):
    # token = serializers.CharField(max_length=200)
    # page = serializers.IntegerField()
    # page_size = serializers.IntegerField()
    class Meta:
        model = models.info
        # fields = ["equipment_id","workArea_id","long_lat_itude","data_AQI","data_O2","data_SO2",
        #           "data_NO2","data_CO","data_PM2_5","data_PM10"]
        fields = ["equipment_id", "workArea_id", "long_lat_itude", "data_O3", "data_SO2",
                  "data_NO2", "data_CO", "data_PM2_5", "data_PM10"]
        # exclude = ["long_lat_itude", ]
    def create(self, validated_data):
        print(validated_data)
        work = models.info(**validated_data)
        work.save()
        return work
    def update(self, instance, validated_data):

        instance.equipment_id= validated_data.get("equipment_id", instance.equipment_id)
        instance.workArea_id = validated_data.get("workArea_id", instance.workArea_id)
        # instance.bind = validated_data.get("bind",instance.bind)
        # instance.online_status = validated_data.get("online_status", instance.online_status)
        # instance.data_AQI = validated_data.get("AQI", instance.data_AQI)
        instance.data_PM2_5 = validated_data.get("PM25",instance.data_PM2_5)
        instance.data_PM10 = validated_data.get("PM10",instance.data_PM10)
        instance.data_O2 = validated_data.get("O2",instance.data_O2)
        instance.data_SO2 = validated_data.get("SO2",instance.data_SO2)
        instance.data_NO2 = validated_data.get("NO2",instance.data_NO2)
        instance.data_CO = validated_data.get("CO",instance.data_CO)
        # instance.register_time = validated_data.get("register_time",instance.register_time)
        # instance.active_time = validated_data.get("active_time", instance.active_time)
        # instance.last_logout_time = validated_data.get("last_logout_time", instance.last_logout_time)
        # instance.last_login_time = validated_data.get("last_login_time", instance.last_login_time)
        # instance.equipment_frozen = validated_data.get("equipment_frozen", instance.equipment_frozen)
        instance.save()
        return instance

class MiniSerialzer(serializers.ModelSerializer):

    class Meta:
        model = models.info,models.his
        field = ["equipment_id","online_status","long_lat_itude","location"]
    def get(self,data):
        return data

