from django.db import models

# Create your models here.

from equipment.models import info
class warning(models.Model):
    #报警信息

    #warn_id = models.IntegerField(max_length=10, verbose_name="报警编号")
    warn_id = models.AutoField(primary_key=True,verbose_name="报警编号")#设置id为主键 并且自增
    equip = models.ForeignKey(info, on_delete=models.PROTECT, max_length=20, verbose_name="设备编号")
    workName = models.CharField(max_length=20, verbose_name="工程名称")
    #warn_time = models.DateTimeField(auto_now_add=True, verbose_name="报警时间", null=True)
    warn_time = models.DateTimeField(auto_now_add=True, verbose_name="报警时间")
    location = models.CharField(max_length=50, verbose_name="报警位置")
    warn_type = models.CharField(max_length=20, verbose_name="报警类型")
    warn_value = models.CharField(max_length=20, verbose_name="报警值/报警问题")
    deal = models.BooleanField(default=False, verbose_name="处理状态")
    #dealPerson = models.CharField(max_length=20, verbose_name="处理人名称")
    dealPerson = models.CharField(max_length=20, verbose_name="处理人名称",null=True)
    #dealPersonPhone = models.CharField(max_length=20, verbose_name="处理人联系电话")
    dealPersonPhone = models.CharField(max_length=20, verbose_name="处理人联系电话",null=True)
    #dealTime = models.DateTimeField(auto_now_add=True, verbose_name="处理时间", null=True)
    dealTime = models.DateTimeField(verbose_name="处理时间", null=True)
    #remark = models.CharField(max_length=50, verbose_name="备注信息")
    remark = models.CharField(max_length=50, verbose_name="备注信息",null=True)