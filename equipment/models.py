from django.db import models

# Create your models here.








class info(models.Model):
    #设备信息

    equipment_id = models.CharField(max_length=20, verbose_name="设备编号", primary_key=True)#unique改为主键
    is_register = models.BooleanField(default=False,verbose_name="注册状态")
    workArea_id = models.IntegerField(max_length=9, verbose_name="工程编号",null=True)
    bind = models.BooleanField(default=False, verbose_name="绑定状态")
    online_status = models.BooleanField(default=False, verbose_name="在线状态")
    long_lat_itude = models.CharField(max_length=50, verbose_name="设备经纬度")
    data_AQI = models.IntegerField(max_length=10, verbose_name="AQI(阈值，校准)",null=True)
    data_PM2_5 = models.IntegerField(max_length=10, verbose_name="PM2.5(阈值，校准)",null=True)
    data_PM10 = models.IntegerField(max_length=10, verbose_name="PM10(阈值，校准)",null=True)
    data_O3 = models.IntegerField(max_length=10, verbose_name="O2(阈值，校准)",null=True)
    data_SO2 = models.IntegerField(max_length=10, verbose_name="SO2(阈值，校准)",null=True)
    data_NO2 = models.IntegerField(max_length=10, verbose_name="NO2(阈值，校准)",null=True)
    data_CO = models.IntegerField(max_length=10, verbose_name="CO(阈值，校准)",null=True)
    register_time = models.DateTimeField(auto_now_add=True, verbose_name="设备注册时间")
    active_time = models.DateTimeField(verbose_name="设备激活时间", null=True)
    last_logout_time = models.DateTimeField(verbose_name="设备最后离线时间", null=True)
    last_login_time = models.DateTimeField(verbose_name="设备最后上线时间", null=True)
    equipment_frozen = models.BooleanField(default=False, verbose_name="冻结状态")


class his(models.Model):
    #采集历史数据

    #equipment_id = models.OneToOneField(info, on_delete=models.PROTECT) 这里 不是一对一的关系 历史数据可以有多个对应一个设备
    equipment_id = models.ForeignKey(info, on_delete=models.PROTECT)
    y_time = models.DateTimeField(auto_now_add=True, verbose_name="数据采集时间", null=True)
    y_location = models.CharField(max_length=50, verbose_name="数据采集位置")
    y_weather = models.CharField(max_length=10, verbose_name="数据采集天气")
    y_AQI = models.IntegerField(max_length=3, verbose_name="每日空气质量参数",null=True)
    y_PM10 = models.IntegerField(max_length=3, verbose_name="PM10含量")
    y_PM2_5 = models.IntegerField(max_length=3, verbose_name="PM2.5含量")
    y_O3 = models.IntegerField(max_length=3, verbose_name="氧气含量")
    y_SO2 = models.IntegerField(max_length=3, verbose_name="二氧化硫含量")
    y_NO2 = models.IntegerField(max_length=3, verbose_name="二氧化氮含量")
    y_CO = models.IntegerField(max_length=3, verbose_name="一氧化碳含量")
    y_temperature = models.IntegerField(verbose_name="温度")
    y_humidity = models.IntegerField(verbose_name="湿度")
    y_wind_speed = models.IntegerField(verbose_name="风速")
    y_light = models.IntegerField(verbose_name="光照强度")
    y_Pa = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="大气压强")
    y_wind_direction = models.CharField(max_length=5, verbose_name="风向")

class realtime(models.Model):
    #采集实时数据 这里就是一对一的关系

    equipment_id = models.OneToOneField(info, on_delete=models.PROTECT)
    #time = models.DateTimeField(auto_now_add=True, verbose_name="数据采集时间", null=True)采集数据时间不可以为空 只要加进去了 就是有时间的
    n_time = models.DateTimeField(auto_now_add=True, verbose_name="数据采集时间")
    location = models.CharField(max_length=50, verbose_name="数据采集位置")
    weather = models.CharField(max_length=10, verbose_name="数据采集天气")
    AQI = models.IntegerField(max_length=3, verbose_name="每日空气质量参数",null=True)
    PM10 = models.IntegerField(max_length=3, verbose_name="PM10含量")
    PM2_5 = models.IntegerField(max_length=3, verbose_name="PM2.5含量")
    O3 = models.IntegerField(max_length=3, verbose_name="氧气含量")
    SO2 = models.IntegerField(max_length=3, verbose_name="二氧化硫含量")
    NO2 = models.IntegerField(max_length=3, verbose_name="二氧化氮含量")
    CO = models.IntegerField(max_length=3, verbose_name="一氧化碳含量")
    temperature = models.IntegerField(verbose_name="温度")
    humidity = models.IntegerField(verbose_name="湿度")
    wind_speed = models.IntegerField(verbose_name="风速")
    light = models.IntegerField(verbose_name="光照强度")
    Pa = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="大气压强")
    wind_direction = models.CharField(max_length=5, verbose_name="风向")