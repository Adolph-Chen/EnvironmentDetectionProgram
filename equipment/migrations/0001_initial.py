# Generated by Django 3.0.8 on 2020-07-21 09:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='info',
            fields=[
                ('equipment_id', models.CharField(max_length=20, primary_key=True, serialize=False, verbose_name='设备编号')),
                ('workArea_id', models.IntegerField(default=1, max_length=9, verbose_name='工程编号')),
                ('bind', models.BooleanField(default=False, verbose_name='绑定状态')),
                ('online_status', models.BooleanField(default=False, verbose_name='在线状态')),
                ('long_lat_itude', models.CharField(max_length=20, verbose_name='设备经纬度')),
                ('data_AQI', models.IntegerField(max_length=10, verbose_name='AQI(阈值，校准)')),
                ('data_PM2_5', models.IntegerField(max_length=10, verbose_name='PM2.5(阈值，校准)')),
                ('data_PM10', models.IntegerField(max_length=10, verbose_name='PM10(阈值，校准)')),
                ('data_O2', models.IntegerField(max_length=10, verbose_name='O2(阈值，校准)')),
                ('data_SO2', models.IntegerField(max_length=10, verbose_name='SO2(阈值，校准)')),
                ('data_NO2', models.IntegerField(max_length=10, verbose_name='NO2(阈值，校准)')),
                ('data_CO', models.IntegerField(max_length=10, verbose_name='CO(阈值，校准)')),
                ('register_time', models.DateTimeField(auto_now_add=True, null=True, verbose_name='设备注册时间')),
                ('active_time', models.DateTimeField(null=True, verbose_name='设备激活时间')),
                ('last_logout_time', models.DateTimeField(null=True, verbose_name='设备最后离线时间')),
                ('last_login_time', models.DateTimeField(null=True, verbose_name='设备最后上线时间')),
                ('equipment_frozen', models.BooleanField(default=False, verbose_name='冻结状态')),
            ],
        ),
        migrations.CreateModel(
            name='realtime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True, verbose_name='数据采集时间')),
                ('location', models.CharField(max_length=20, verbose_name='数据采集位置')),
                ('weather', models.CharField(max_length=10, verbose_name='数据采集天气')),
                ('AQI', models.IntegerField(max_length=3, verbose_name='每日空气质量参数')),
                ('PM10', models.IntegerField(max_length=3, verbose_name='PM10含量')),
                ('PM2_5', models.IntegerField(max_length=3, verbose_name='PM2.5含量')),
                ('O2', models.IntegerField(max_length=3, verbose_name='氧气含量')),
                ('SO2', models.IntegerField(max_length=3, verbose_name='二氧化硫含量')),
                ('NO2', models.IntegerField(max_length=3, verbose_name='二氧化氮含量')),
                ('CO', models.IntegerField(max_length=3, verbose_name='一氧化碳含量')),
                ('temperature', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='温度')),
                ('humidity', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='湿度')),
                ('wind_speed', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='风速')),
                ('light', models.IntegerField(max_length=5, verbose_name='光照强度')),
                ('Pa', models.DecimalField(decimal_places=3, max_digits=7, verbose_name='大气压强')),
                ('wind_direction', models.CharField(max_length=5, verbose_name='风向')),
                ('equipment_id', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='equipment.info')),
            ],
        ),
        migrations.CreateModel(
            name='his',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('y_time', models.DateTimeField(auto_now_add=True, null=True, verbose_name='数据采集时间')),
                ('y_location', models.CharField(max_length=20, verbose_name='数据采集位置')),
                ('y_weather', models.CharField(max_length=10, verbose_name='数据采集天气')),
                ('y_AQI', models.IntegerField(max_length=3, verbose_name='每日空气质量参数')),
                ('y_PM10', models.IntegerField(max_length=3, verbose_name='PM10含量')),
                ('y_PM2_5', models.IntegerField(max_length=3, verbose_name='PM2.5含量')),
                ('y_O2', models.IntegerField(max_length=3, verbose_name='氧气含量')),
                ('y_SO2', models.IntegerField(max_length=3, verbose_name='二氧化硫含量')),
                ('y_NO2', models.IntegerField(max_length=3, verbose_name='二氧化氮含量')),
                ('y_CO', models.IntegerField(max_length=3, verbose_name='一氧化碳含量')),
                ('y_temperature', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='温度')),
                ('y_humidity', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='湿度')),
                ('y_wind_speed', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='风速')),
                ('y_light', models.IntegerField(max_length=5, verbose_name='光照强度')),
                ('y_Pa', models.DecimalField(decimal_places=3, max_digits=7, verbose_name='大气压强')),
                ('y_wind_direction', models.CharField(max_length=5, verbose_name='风向')),
                ('equipment_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='equipment.info')),
            ],
        ),
    ]
