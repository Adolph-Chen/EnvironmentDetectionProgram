from django.conf.urls import url

from .views import Authority
urlpatterns = [


    #url("^create$",WorkArea.as_view(),name="workArea/create"),
    url("^authority$",Authority.as_view(),name="authority/authority")
]