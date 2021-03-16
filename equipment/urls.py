from django.conf.urls import url
from .views import equipmentView,SearchEquipment,Census,MiniequipmentView,MiniGetOneView,GetequipmentList
from monitor import views as dataMonitorViews
urlpatterns = [


    #url("^create$",equipmentView.as_view(),name="equipment/create"),
    url("^getAll$",equipmentView.as_view(),name="equipment/getAll"),
    url("^update$",equipmentView.as_view(),name="equipment/update"),
    url("^delete$",equipmentView.as_view(),name="equipment/delete"),

    url("^searchequipment$",SearchEquipment.as_view(),name="equipment/searchequipment"),
    url("^Miniget$",MiniequipmentView.as_view()),
    url("^getCensus$",Census.as_view(),name="workArea/getCensus"),
    url("^Minigetdetail$", MiniGetOneView.as_view()),
    url("^getequipmentlist$",GetequipmentList.as_view()),
    url("^get1$",dataMonitorViews.DataMonitor1.as_view(),name="equipment/get1"),
    url("^get2$",dataMonitorViews.DataMonitor2.as_view(),name="equipment/get2"),
    url("^get3$",dataMonitorViews.DataMonitor3.as_view(),name="equipment/get3"),
    url("^get4$",dataMonitorViews.DataMonitor4.as_view(),name="equipment/get4"),

    # url("^Miniget3$",dataMonitorViews.MiniDataMonitor3.as_view()),
    url("^bigScreen/Miniget$",dataMonitorViews.MiniDataMonitor2.as_view()),#通过设备id来获取设备气象信息
    url("^Miniget1$",dataMonitorViews.MiniDataMonitor1.as_view()),
]