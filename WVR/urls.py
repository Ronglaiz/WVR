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
from django.urls import path, include
from WebVul import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index),
    path('', views.main_page),
    path('login/', views.login),
    path('login_handle/', views.login_handle),
    path('main_page/', views.main_page),
    path('logout/', views.log_out),
    path('logout/', views.log_out),
    path('sqli/', views.sqli),
    path('query_vul_by_id/', views.query_vul_by_id),

    path('vul_pages/', views.vul_pages),
    path('query_pages/', views.query_pages),
    path('insert_page/', views.insert_page),



    path('xssi/', views.xssi),
    path('insert_vul/', views.insert_vul),
    path('query_vul/', views.query_vul),

    path('cmdi/', views.cmdi),
    path('query_server_status/', views.query_server_status),

    path('ssrf/', views.ssrf),
    path('query_vul_details/', views.query_vul_details),

    path('csrf/', views.csrf),
    path('insert_vul_csrf/',views.insert_vul_csrf),

    path('brutef/', views.brutef),
    path('query_with_captcha/', views.query_with_captcha),
    path('query_by_rainbow/', views.query_by_rainbow),
    path('query_normal/', views.query_normal),

    path('filed/', views.filed),
    path('filed_detail/', views.filed_detail),

    path('fileu/', views.fileu),
    path('fileu_detail_simple/', views.fileu_detail_simple),
    path('fileu_detail_form/', views.fileu_detail_form),

    path('unauth/', views.unauth_main),
    path('unauth_horizontal/', views.unauth_horizontal),
    path('unauth_vertical/', views.unauth_vertical),
    path('unauth_noaccess/', views.unauth_noaccess),

    path('data_leak/', views.data_leak),

    path('register/', views.register),
    path('register_admin/', views.register_admin),
    path('register_admin_detail/', views.register_admin_detail),
    path('register_normal_detail/', views.register_normal_detail),

    path('sessionm/', views.sessionm),
    path('login_b_submit/', views.login_b_submit),
    path('login_b/', views.login_b),
    path('cookie_set/', views.cookie_set),
    path('cookie_get/', views.cookie_get),
    path('session_set/', views.session_set),
    path('session_get/', views.session_get),

    path('captcha', include('captcha.urls')),
]


handler404 = views.page_not_found
