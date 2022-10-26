from django.contrib import admin
from WebVul.models import VulInfo
from WebVul.models import LoginUsers
# Register your models here.


class VulInfoAdmin(admin.ModelAdmin):
    list_display = ['vul_id', 'vul_name', 'vul_desc']


class LoginUsersAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'user_name', 'user_pwd', 'user_level']


# 注册类模型
admin.site.register(VulInfo, VulInfoAdmin)
admin.site.register(LoginUsers, LoginUsersAdmin)
