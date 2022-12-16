from django.contrib.auth.forms import AuthenticationForm
from django import forms
from captcha.fields import CaptchaField, CaptchaTextInput


class UserForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=16, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="密码", max_length=16, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    captcha = CaptchaField(label='验证码', widget=CaptchaTextInput(attrs={'class': 'form-control'}))


class RegisterForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=16, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="密码", max_length=16, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", max_length=16, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    captcha = CaptchaField(label='验证码', widget=CaptchaTextInput(attrs={'class': 'form-control'}))


class RainbowForm(forms.Form):
    plaintext = forms.CharField(label="明文", max_length=16, widget=forms.TextInput(attrs={'class': 'form-control'}))


class NormalLoginUserForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=16, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="密码", max_length=16, widget=forms.PasswordInput(attrs={'class': 'form-control'}))


# 文件上传的表单
class UploadFileForm(forms.Form):
    #title = forms.CharField(label="标题",max_length=50)
    file = forms.FileField(label="")
