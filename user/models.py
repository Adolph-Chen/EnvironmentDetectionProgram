import datetime


from django.db import models

# Create your models here.


class info(models.Model):
    #用户信息

    #user_workid = models.IntegerField(max_length=10, verbose_name="用户工号",  unique=True)  primary_key=True 改成字符串
    user_workid = models.CharField(max_length=10, verbose_name="用户工号", primary_key=True)
    #user_password = models.CharField(default="123456", max_length=20, verbose_name="用户登陆密码")
    password = models.CharField(default="123456", max_length=200, verbose_name="用户登陆密码")
    username = models.CharField(max_length=20, verbose_name="用户名")
    name = models.CharField(max_length=20, verbose_name="用户姓名")
    sex = models.CharField(max_length=3, verbose_name="性别")
    telephone_number = models.CharField(max_length=20, verbose_name="用户联系电话")
    user_mail = models.CharField(max_length=20, verbose_name="用户邮箱")
    user_permission = models.CharField(default="user", max_length=20, verbose_name="用户权限")
    user_frozen = models.BooleanField(default=False, verbose_name="冻结状态")

