from django.db import models

# Create your models here.


class journal(models.Model):
    #用户日志

    #user_name = models.ForeignKey(info, on_delete=models.PROTECT, max_length=20,verbose_name="操作用户名") 这个表是独立的  不管用户存在否 都要存在
    user_name = models.CharField(max_length=20,verbose_name="操作用户名")
    user_ip = models.CharField(max_length=20, verbose_name="用户ip")
    model = models.CharField(max_length=20, verbose_name="访问模块")
    require_time = models.DateTimeField(auto_now_add=True, verbose_name="访问请求时间", null=True)
    #diary_id = models.IntegerField(max_length=10, verbose_name="日志id")  primary_key=True   主键  让他自增
    diary_id = models.AutoField(verbose_name="日志id",primary_key=True)