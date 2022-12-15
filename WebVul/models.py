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
    # 用户密
    user_pwd = models.CharField(max_length=100)
    # 用户级别
    user_level = models.IntegerField()
    # 用户邮箱
    user_email = models.CharField(max_length=100)

    def __str__(self):
        return self.user_name


# 用户留言的类
class UserComments(models.Model):
    # 用户名字
    user_name = models.OneToOneField(LoginUsers, on_delete=models.CASCADE)
    # 留言标题
    comment_title = models.CharField(max_length=100)
    # 留言详细内容
    comment_details = models.CharField(max_length=100)


# 漏洞文章的类
class Vul_Pages(models.Model):
    # 漏洞编号
    vul_id = models.IntegerField()
    # 漏洞名字
    vul_name = models.CharField(max_length=30)
    # 文章名字
    vul_title = models.CharField(max_length=100)
    # 文章描述
    vul_page = models.CharField(max_length=500)


# 用于越权页面的类
class Auth_Infos(models.Model):
    # 信息ID
    info_id = models.IntegerField()
    # 信息内容
    info_content = models.CharField(max_length=300)
    # 信息所属人
    info_owner = models.CharField(max_length=300)
