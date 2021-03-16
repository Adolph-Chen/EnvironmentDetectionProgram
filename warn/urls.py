from django.conf.urls import url

from .views import *
urlpatterns = [


    #url("^create$",WorkArea.as_view(),name="workArea/create"),
    url("^warn$",Warn.as_view(),name="warn/warn"),
    url("^warnNum$",WarnNum.as_view(),name="warn/warnNum"),
    url("^noDealWarn$",NoDealWarn.as_view(),name="warn/noDealWarn"),
    url("^MininoDealWarn$",MiniNoDealWarn.as_view()),
    url("^Miniwarnsearch$",MiniWarnSearch.as_view()),
    url("^Miniwarn$",MiniWarn.as_view()),
]