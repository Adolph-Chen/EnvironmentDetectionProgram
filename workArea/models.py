from django.db import models

# Create your models here.

'''
"workArea_id"id,
"workArea_name":name,
"workArea_type":xxx,
"long_lat_itude":(xxx,xxx),
"area_size":xxx,"time":xxx,
"location":xxx,"status":xxx,
"company":xxx
'''

from equipment.models import info

class manage(models.Model):
    #工程管理

    #workArea_id = models.IntegerField(max_length=9, verbose_name="工程编号", unique=True)  primary_key  改成了字符串型
    workArea_id = models.CharField(max_length=9, verbose_name="工程编号", primary_key=True)
    workArea_name = models.CharField(max_length=20, verbose_name="工程名称")
    workArea_time = models.CharField(max_length=20, verbose_name="工程时间")
    duty_person = models.CharField(max_length=15, verbose_name="负责人员")
    company = models.CharField(max_length=20, verbose_name="施工单位")
    workArea_status = models.BooleanField(default=False, verbose_name="工程状态")
    location = models.CharField(max_length=50, verbose_name="工程地址")
    long_lat_itude = models.CharField(max_length=20, verbose_name="工程经纬度")
    workArea_type = models.CharField(max_length=10, verbose_name="工程类型")
    area_size = models.CharField(max_length=15, verbose_name="占地面积")
    workArea_frozen = models.BooleanField(default=False, verbose_name="冻结状态")


class load(models.Model):
    #设备激活

    equipment_id = models.OneToOneField(info, on_delete=models.CASCADE)
    #equipment_password = models.CharField(max_length=20, verbose_name="设备密码") 加密后就会成为长的字符串
    equipment_password = models.CharField(max_length=255, verbose_name="设备密码")
    dev_key = models.CharField(max_length=255,null=True)