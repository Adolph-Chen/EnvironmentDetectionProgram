from django.db import models

# Create your models here.
from django.db import models

class UserInfo(models.Model):

    username = models.CharField(max_length=20);
    password = models.CharField(max_length=200);
    server_ip = models.CharField(max_length=20,default="120.55.193.78");
    port = models.IntegerField(default=80);
    request_count = models.IntegerField();
    all_count = models.IntegerField();


class UserTable(models.Model):

    user = models.ForeignKey(UserInfo,on_delete=models.CASCADE,related_name="table");
    request_count = models.IntegerField();
    client_ip = models.CharField(max_length=20);
    request_time = models.CharField(max_length=50);