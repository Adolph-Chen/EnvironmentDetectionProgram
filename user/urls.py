from django.conf.urls import url

from .views import User,UserSearch
from .views import MiniUser
urlpatterns = [


    #url("^create$",WorkArea.as_view(),name="workArea/create"),
    url("^user$",User.as_view(),name="user/user"),
    url("^userSearch$",UserSearch.as_view(),name="user/userSearch"),
    url("^Miniuser$",MiniUser.as_view()),
]