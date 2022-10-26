from django.db import models


# Create your models here.
# 漏洞模型的类
class VulInfo(models.Model):
    # 漏洞编号
    vul_id = models.IntegerField()
    # 漏洞名字
    vul_name = models.CharField(max_length=30)
    # 漏洞描述
    vul_desc = models.CharField(max_length=300)

    def __str__(self):
        return self.vul_name


# 登录用户模型的类
class LoginUsers(models.Model):
    # 用户编号
    user_id = models.IntegerField()
    # 用户名字
    user_name = models.CharField(max_length=30)
    # 用户密码
    user_pwd = models.CharField(max_length=100)
    # 用户级别
    user_level = models.IntegerField()

    def __str__(self):
        return self.user_name

