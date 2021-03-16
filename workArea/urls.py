from django.conf.urls import url

from .views import WorkArea,WorkAreaBind,SearchWorkArea,Census,Active
urlpatterns = [


    url("^create$",WorkArea.as_view(),name="workArea/create"),
    url("^getAll$",WorkArea.as_view(),name="workArea/getAll"),
    url("^update$",WorkArea.as_view(),name="workArea/update"),
    url("^delete$",WorkArea.as_view(),name="workArea/delete"),
    url("^bindEquipment$",WorkAreaBind.as_view(),name="workArea/bindEquipment"),
    url("^searchWorkArea$",SearchWorkArea.as_view(),name="workArea/searchWorkArea"),
    #getCensus
    url("^getCensus$",Census.as_view(),name="workArea/getCensus"),
    url("^getActive$",Active.as_view(),name="workArea/getActive"),
]