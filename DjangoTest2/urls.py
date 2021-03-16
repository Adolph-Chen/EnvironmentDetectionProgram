"""DjangoTest2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from platForm import views as openPlatformViews
from workArea import urls as workAreaUrls
from warn import urls as warnUrls
from permission import urls as permissionUrls
from journal import urls as journalUrls
from user import urls as userUrls
from login import views as loginViews
# from monitor import views as dataMonitorViews

from equipment import views as equipmentViews

urlpatterns = [
    path('admin/', admin.site.urls),
    url("^open/$", openPlatformViews.open,name="open"),
    url("^openUser/login$", openPlatformViews.OpenUserLogin.as_view(), name="openUser/login"),
    url("^openUser/get$", openPlatformViews.OpenUserLogin.as_view(), name="openUser/get"),
    url("^openUser/getTable$",openPlatformViews.OpenUserTable.as_view(),name="openUser/getTable"),
    url("^openUser/signUp$",openPlatformViews.OpenUserSignUp.as_view(),name="openUser/signUp"),
    url("^open/sendEmail$",openPlatformViews.OpenSendMail.as_view(),name="open/sendEmail"),
    url("^open/resetPassword$",openPlatformViews.OpenResetPassword.as_view(),name="open/resetPassword"),
    url("^openData$",openPlatformViews.OpenData.as_view(),name="openData"),
    url("^user/login$",loginViews.LoginView.as_view(),name="user/login"),
    url("^user/logout$",loginViews.LogoutView.as_view(),name="user/logout"),

    url("^workArea/",include(workAreaUrls)),
    url("^warn/",include(warnUrls)),
    url("^diary/",include(journalUrls)),
    url("^user/",include(userUrls)),
    url("^equipment/",include('equipment.urls')),
    url("^authority/",include(permissionUrls)),
    # url("^equipment/get1/$",dataMonitorViews.DataMonitor1.as_view(),name="equipment/get1"),
    # url("^equipment/get2/$",dataMonitorViews.DataMonitor2.as_view(),name="equipment/get2"),

    #url("^equipment/Miniget1/$",dataMonitorViews.MiniDataMonitor1.as_view()),
]
#1515030817@qq.com