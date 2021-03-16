from django.conf.urls import url

from .views import *
urlpatterns = [


    #url("^create$",WorkArea.as_view(),name="workArea/create"),
    url("^diary$",Diary.as_view(),name="diary/diary")
]