"""WVR URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from WebVul import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index),
    path('login/', views.login),
    path('login_handle/', views.login_handle),
    path('main_page/', views.main_page),
    path('logout/', views.log_out),

    path('sqli/', views.sqli),
    path('xssi/', views.xssi),
    path('cmdi/', views.cmdi),
    path('insert_vul/', views.insert_vul),
    path('query_vul/', views.query_vul),

    path('login_b_submit/', views.login_b_submit),
    path('login_b/', views.login_b),
    path('cookie_set/', views.cookie_set),
    path('cookie_get/', views.cookie_get),
    path('session_set/', views.session_set),
    path('session_get/', views.session_get),

]


handler404 = views.page_not_found