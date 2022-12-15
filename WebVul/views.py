import json
import os
import re
from pathlib import Path

import requests
from django.http import HttpResponse, JsonResponse, Http404, FileResponse
from django.shortcuts import render
from django.template import loader
from django.shortcuts import redirect
from WebVul.models import LoginUsers, Vul_Pages, VulInfo, Auth_Infos
from WebVul.Utils.CsrfImpl import *
from WebVul.forms import UserForm, RainbowForm, NormalLoginUserForm, UploadFileForm
import hashlib
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent
# Create your views here.
# 定义视图函数
def index(request):
    # 加载模板信息
    temp = loader.get_template('WebVul/index.html')
    # 给模板传递数据
    context = {'name': 'XSS'}
    # 渲染模板
    html = temp.render(context)
    # 返回给浏览器
    return HttpResponse(html)


def login(request):
    return render(request, "WebVul/login.html")


def login_handle(request):
    # 使用request.POST.get来获取相关的参数
    username = request.POST.get("username")
    password = request.POST.get("password")
    # 模拟判断账号密码是否正确
    try:
        # true_password = LoginUsers.objects.get(user_name=username).user_pwd
        user = LoginUsers.objects.filter(user_name=username, user_pwd=password)
        if user:
            # 设置session
            request.session['is_login'] = 'true'
            request.session['user_name'] = username
            return JsonResponse({"res": 1})
        else:
            return JsonResponse({"res": 0})
    except LoginUsers.DoesNotExist:
        return JsonResponse({"res": 0})


# 检查是否认证
def check_user_auth(request):
    # 获取session内容的真假bool
    is_login = request.session.get('is_login', False)
    if is_login:
        # 写入cookie
        # 获取字典的内容并传入页面文件
        cookie_content = request.COOKIES
        session_content = request.session
        username = request.session['user_name']
        return username
    else:
        return ""


# 主界面
def main_page(request):
    username = check_user_auth(request)
    if username == "":
        return render(request, "WebVul/login.html")
    else:
        return render(request, "WebVul/main.html", locals())


# 注销界面
def log_out(request):
    """
    直接通过request.session['is_login']回去返回的时候，
    如果is_login对应的value值不存在会导致程序异常。所以
    需要做异常处理
    """
    try:
        # 删除is_login对应的value值
        del request.session['is_login']
        # OR---->request.session.flush() # 删除django-session表中的对应一行记录

    except KeyError:
        pass
    # 点击注销之后，直接重定向回登录页面
    return redirect('/login/')


# 查询数据
def query_vul(request):
    vul_list = VulInfo.objects.all()
    username = check_user_auth(request)
    if username == "":
        return render(request, "WebVul/login.html")
    else:
        return render(request, "WebVul/xss.html", locals())


# 根据id查询vul信息
def query_vul_by_id(request):
    username = check_user_auth(request)
    vul_id = request.POST.get("vul_id")
    # 判断id是否为空
    if username == "":
        return render(request, "WebVul/login.html")
    else:
        if vul_id == "":
            return JsonResponse({"res": 2})
        else:
            try:
                # 根据id查询数据，使用原生sql查询
                query_sql = "SELECT * FROM WebVul_vulinfo WHERE vul_id=" + vul_id
                vul_list = VulInfo.objects.raw(query_sql)
                if len(vul_list) != 0:
                    html_return_string = ""
                    for i in range(len(vul_list)):
                        html_return_string = html_return_string + "<tr><td>" + str(vul_list[i].vul_id) + "</td><td>" + \
                                             str(vul_list[i].vul_name) + "</td><td>" + str(vul_list[i].vul_desc) + "</td></tr>"
                    return JsonResponse({"res": 1, "html_return_string": html_return_string})
                else:
                    return JsonResponse({"res": 0})
            except LoginUsers.DoesNotExist:
                return JsonResponse({"res": 0})


# 插入vulinfo表
def insert_vul(request):
    vul_name = request.POST.get("vul_name")
    vul_desc = request.POST.get("vul_desc")
    vul_count = VulInfo.objects.all().count()
    # 模拟判断账号密码是否正确
    if vul_name == "" or vul_desc == "":
        return JsonResponse({"res": 2})
    else:
        try:
            vul_info = VulInfo(vul_id=vul_count + 1, vul_name=vul_name, vul_desc=vul_desc)
            vul_info.save()
            return JsonResponse({"res": 1, "vul_name": vul_name})
        except LoginUsers.DoesNotExist:
            return JsonResponse({"res": 0})


def insert_vul_csrf(request):
    # 需要有一些 try cache
    vul_name = request.POST.get('vul_name')
    vul_desc = request.POST.get("vul_desc")
    vul_count = VulInfo.objects.all().count()
    csrf_token_from_page = request.POST.get("csrf_token")
    csrf_token_from_session = request.session['csrf_token']
    if csrf_token_from_page != csrf_token_from_session:
        server_response = "插入失败！-csrf"
    # 模拟判断账号密码是否正确
    elif vul_name == "" or vul_desc == "":
        server_response = "请输入数据！"
    else:
        try:
            vul_info = VulInfo(vul_id=vul_count + 1, vul_name=vul_name, vul_desc=vul_desc)
            vul_info.save()
            server_response = "插入成功！"
        except LoginUsers.DoesNotExist:
            server_response = "插入失败!"
    csrf_token = csrf_token_from_session
    return render(request, "WebVul/csrf.html", locals())


def query_server_status(request):
    username = check_user_auth(request)
    if username == "":
        return render(request, "WebVul/login.html")
    else:
        if request.method == 'POST':
            server_status = "REQUEST ERROR!"
            return render(request, "WebVul/cmdi.html", {'server_status': server_status})
        else:
            server_ip = request.GET.get("cmd")
            if server_ip == "":
                server_status = "请输入服务器地址"
            else:
                result = os.popen('ping ' + server_ip + ' -c 5')
                server_status = result.read()
        return render(request, "WebVul/cmdi.html", {'server_status': server_status, 'username': username})


def query_vul_details(request):
    username = check_user_auth(request)
    if username == "":
        return render(request, "WebVul/login.html")
    else:
        if request.method == 'POST':
            server_response = "REQUEST ERROR!"
            return render(request, "WebVul/ssrf.html", {'server_response': server_response, 'username': username})
        else:
            vul_info = request.GET.get("vul_info")
            if vul_info == "":
                server_response = "REQUEST ERROR!"
            else:
                # query wikipedia
                query_url = "https://en.wikipedia.org/wiki/" + vul_info
                print(query_url)
                header = {"Content-Type": "application/json"}
                response_s = requests.get(url=query_url, headers=header)
                server_response = response_s.text
            return render(request, "WebVul/ssrf.html", {'server_response': server_response, 'username': username})


'''
def main_page_handle(request):
    vul_part_name = request.POST.get("vul_name")
    try:
        vul_id = VulInfo.objects.filter(vul_name__contains=vul_part_name)[0].vul_id
        vul_name = VulInfo.objects.filter(vul_name__contains=vul_part_name)[0].vul_name
        vul_desc = VulInfo.objects.filter(vul_name__contains=vul_part_name)[0].vul_desc
        print(vul_id, vul_name, vul_desc)
        return JsonResponse({"vul_id": vul_id, "vul_name": vul_name, "vul_desc": vul_desc})
    except VulInfo.DoesNotExist:
        return JsonResponse({"vul_id": "", "vul_name": "", "vul_desc": ""})
'''


# 跳转到sqli
def sqli(request):
    username = check_user_auth(request)
    if username == "":
        return render(request, "WebVul/login.html")
    else:
        return render(request, "WebVul/sqli.html", locals())


# 跳转到xss
def xssi(request):
    username = check_user_auth(request)
    if username == "":
        return render(request, "WebVul/login.html")
    else:
        return render(request, "WebVul/xss.html", locals())


# 跳转到cmdi
def cmdi(request):
    username = check_user_auth(request)
    if username == "":
        return render(request, "WebVul/login.html")
    else:
        return render(request, "WebVul/cmdi.html", locals())


# ssrf
def ssrf(request):
    username = check_user_auth(request)
    if username == "":
        return render(request, "WebVul/login.html")
    else:
        return render(request, "WebVul/ssrf.html", locals())


# ssrf
def csrf(request):
    username = check_user_auth(request)
    csrf_token = CsrfImpl(32).gen_token()
    request.session['csrf_token'] = csrf_token
    if username == "":
        return render(request, "WebVul/login.html")
    else:
        return render(request, "WebVul/csrf.html", locals())


def brutef(request):
    username = check_user_auth(request)
    if username == "":
        return render(request, "WebVul/login.html")
    else:
        login_form = UserForm()
        rainbow_form = RainbowForm()
        normal_form = NormalLoginUserForm()
        return render(request, "WebVul/brutef.html", locals())


def query_with_captcha(request):
    username = check_user_auth(request)
    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = ""
        if login_form.is_valid():
            user_name = login_form.cleaned_data['username']
            pass_word = login_form.cleaned_data['password']
            try:
                user = LoginUsers.objects.filter(user_name=user_name, user_pwd=pass_word)
                if user:
                    message = "能登陆！！"
                else:
                    message = "不能登录，验证失败！"
            except LoginUsers.DoesNotExist:
                message = "不能登录，验证失败2！"
        else:
            message = "验证码错误！"
        return render(request, "WebVul/brutef.html", locals())


def query_by_rainbow(request):
    username = check_user_auth(request)
    if request.method == "POST":
        rainbow_form = RainbowForm(request.POST)
        message2 = ""
        if rainbow_form.is_valid():
            plaintext = rainbow_form.cleaned_data['plaintext']
            hash_code = "de30f4ed64a614089b1ecb0a6f039ac3"
            hashed_plaintext = hashlib.md5(plaintext.encode('utf8')).hexdigest()

            if hashed_plaintext == hash_code:
                message2 = "恭喜！你猜对了！"
            else:
                message2 = "你猜错了！"
        else:
            message = "出错了！！"
        return render(request, "WebVul/brutef.html", locals())


def query_normal(request):
    username = check_user_auth(request)
    if request.method == "POST":
        normal_form = NormalLoginUserForm(request.POST)
        message3 = ""
        if normal_form.is_valid():
            user_name = normal_form.cleaned_data['username']
            pass_word = normal_form.cleaned_data['password']
            try:
                user = LoginUsers.objects.filter(user_name=user_name, user_pwd=pass_word)
                if user:
                    message3 = "能登陆！！"
                else:
                    message3 = "不能登录，验证失败！"
            except LoginUsers.DoesNotExist:
                message3 = "不能登录，验证失败！"
        else:
            message3 = "发生错误了！！"
        return render(request, "WebVul/brutef.html", locals())


def filed(request):
    username = check_user_auth(request)
    if username == "":
        return render(request, "WebVul/login.html")
    else:
        BASE_DIR = str(Path(__file__).resolve().parent.parent) + "/Media"
        files_name = os.listdir(BASE_DIR)

        return render(request, "WebVul/filed.html", locals())


def filed_detail(request):
    username = check_user_auth(request)
    if username == "":
        return render(request, "WebVul/login.html")
    else:
        if request.method == "GET":
            file_name = request.GET.get('name')
            file_path = str(Path(__file__).resolve().parent.parent) + "/Media/" + file_name
            '''扩展名判断
            ext = os.path.basename(file_path).split('.')[-1].lower()
            if ext not in ['py', 'db', 'sqlite3']:
                response = FileResponse(open(file_path, 'rb'))
                response['content_type'] = "application/octet-stream"
            else:
                raise Http404
            '''
            response = FileResponse(open(file_path, 'rb'))
            response['content_type'] = "application/octet-stream"
            response['Content-Disposition'] = 'attachment;filename=%s' % file_name
            return response


def fileu(request):
    username = check_user_auth(request)
    if username == "":
        return render(request, "WebVul/login.html")
    else:
        upload_form = UploadFileForm()
        return render(request, "WebVul/fileu.html", locals())


# #最简单的一种文件上传
def fileu_detail_simple(request):
    username = check_user_auth(request)
    response_to_page = ""
    if username == "":
        return render(request, "WebVul/login.html")
    else:
        if request.method == "POST":
            # 获取上传的文件,如果没有文件,则默认为None;
            File = request.FILES.get("upload_file_simple", None)
            if File is None:
                response_to_page = "没有选择上传的文件！"
            else:
                # 打开特定的文件进行二进制的写操作;
                file_store_path = str(BASE_PATH) + "/Media/" + str(File.name)
                with open(file_store_path, 'wb+') as f:
                    # 分块写入文件;
                    for chunk in File.chunks():
                        f.write(chunk)
                response_to_page = "上传成功!"
        else:
            return render(request, 'WebVul/fileu.html')
    return render(request, 'WebVul/fileu.html', locals())


# Form表单文件上传
def fileu_detail_form(request):
    username = check_user_auth(request)
    response_to_page_form = ""
    if username == "":
        return render(request, "WebVul/login.html")
    else:
        if request.method == "POST":
            upload_form = UploadFileForm(request.POST, request.FILES)
            File_form = request.FILES['file']
            if upload_form.is_valid():
                # 打开特定的文件进行二进制的写操作;
                file_store_path = str(BASE_PATH) + "/Media/" + str(File_form.name)
                with open(file_store_path, 'wb+') as f:
                    # 分块写入文件;
                    for chunk in File_form.chunks():
                        f.write(chunk)
                response_to_page_form = "上传成功!"
            else:
                response_to_page_form = "没有选择上传的文件！"
        else:
            upload_form = UploadFileForm()
            return render(request, 'WebVul/fileu.html', {'upload_form': upload_form, 'response_to_page_form': response_to_page_form})
        return render(request, 'WebVul/fileu.html', {'upload_form': upload_form, 'response_to_page_form': response_to_page_form})


"""
越权访问和无权限访问
    path('unauth/', views.unauth_main),
    path('unauth_noaccess/', views.unauth_noaccess),
    path('unauth_horizontal/', views.unauth_horizontal),
    path('unauth_vertical/', views.unauth_vertical),
"""


def unauth_main(request):
    username = check_user_auth(request)
    if username == "":
        return render(request, "WebVul/login.html")
    else:
        # 用username查询数据库
        try:
            # 查询用户level
            user_level = LoginUsers.objects.get(user_name=username).user_level
            if user_level != 0:
                disabled = "disabled"
            else:
                disabled = ""
        except LoginUsers.DoesNotExist:
            return render(request, "WebVul/login.html")
        return render(request, "WebVul/unauth.html", locals())


def unauth_horizontal(request):
    username = check_user_auth(request)
    if username == "":
        return render(request, "WebVul/login.html")
    else:
        try:
            # 查询用户Level
            user_level_login_user = LoginUsers.objects.get(user_name=username).user_level
            # 获取前端传入的用户名，查询对应的level
            user_name = request.GET.get('id')
            user_level_front_end = LoginUsers.objects.get(user_name=user_name).user_level
            if user_level_login_user == user_level_front_end:
                info_content = Auth_Infos.objects.get(info_owner=user_name).info_content
                if info_content != "":
                    server_response_unauth = info_content
                else:
                    server_response_unauth = "No records!"
            else:
                server_response_unauth = "Unauthorized query!"
        except Auth_Infos.DoesNotExist:
            server_response_unauth = "No records!"
        except LoginUsers.DoesNotExist:
            server_response_unauth = "No records!"
        unauth_type = "横向越权"
        return render(request, "WebVul/unauth_detail.html", locals())


def unauth_noaccess(request):
    pass


def unauth_vertical(request):
    username = check_user_auth(request)
    if username == "":
        return render(request, "WebVul/login.html")
    else:
        try:
            # 获取前端传入的用户名
            user_name = request.GET.get('id')
            info_content = Auth_Infos.objects.get(info_owner=user_name).info_content
            if info_content != "":
                server_response_unauth = info_content
            else:
                server_response_unauth = "No records!"
        except Auth_Infos.DoesNotExist:
            server_response_unauth = "No records!"
    unauth_type = "纵向越权"
    return render(request, "WebVul/unauth_detail.html", locals())


def data_leak(request):
    username = check_user_auth(request)
    if username == "":
        return render(request, "WebVul/login.html")
    else:
        server_response = "This is a page"
        return render(request, "WebVul/data_leak.html", locals())


def register(request):
    return render(request, "WebVul/register.html", locals())


def register_admin(request):
    username = check_user_auth(request)
    if username == "":
        return render(request, "WebVul/login.html")
    else:
        return render(request, "WebVul/register_admin.html", locals())


def register_normal_detail(request):
    user_name = request.POST.get("user_name")
    password_1 = request.POST.get("password_1")
    password_2 = request.POST.get("password_2")
    email = request.POST.get("email")

    if len(user_name) > 20:
        return JsonResponse({"res": 1, "errmsg": "用户名长度超出范围！"})
    elif len(password_1) > 20 or len(password_2) > 20:
        return JsonResponse({"res": 1, "errmsg": "密码长度超出范围！"})
    elif len(email) > 50:
        return JsonResponse({"res": 1, "errmsg": "邮箱长度超出范围！"})

    if user_name == "" or password_1 == "" or password_2 == "" or email == "":
        return JsonResponse({"res": 1, "errmsg": "不能为空！"})
    if password_1 != password_2:
        return JsonResponse({"res": 1, "errmsg": "密码不一致"})

    is_correct_email = re.match("^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$",email)
    if is_correct_email is None:
        return JsonResponse({"res": 1, "errmsg": "邮箱格式不正确"})

    user = LoginUsers.objects.filter(user_name=user_name)
    if user:
        return JsonResponse({"res": 1, "errmsg": "用户名已存在"})
    else:
        user_count = LoginUsers.objects.all().count()
        user_add = LoginUsers(user_id=user_count + 1, user_name=user_name, user_pwd=password_1, user_level="2", user_email=email)
        user_add.save()
        return JsonResponse({"res": 0, "errmsg": "注册成功"})


def register_admin_detail(request):
    username = check_user_auth(request)
    user_name = request.POST.get("user_name")
    password_1 = request.POST.get("password_1")
    password_2 = request.POST.get("password_2")
    email = request.POST.get("email")
    level = request.POST.get("level")
    if username == "":
        return render(request, "WebVul/login.html")
    else:
        if len(user_name) > 20:
            return JsonResponse({"res": 1, "errmsg": "用户名长度超出范围！"})
        elif len(password_1) > 20 or len(password_2) > 20:
            return JsonResponse({"res": 1, "errmsg": "密码长度超出范围！"})
        elif len(email) > 50:
            return JsonResponse({"res": 1, "errmsg": "邮箱长度超出范围！"})

        if level == 'admin':
            user_level = 0
        elif level == 'normal':
            user_level = 1
        else:
            return JsonResponse({"res": 1, "errmsg": "权限不对！"})

        if user_name == "" or password_1 == "" or password_2 == "" or email == "":
            return JsonResponse({"res": 1, "errmsg": "不能为空！"})
        if password_1 != password_2:
            return JsonResponse({"res": 1, "errmsg": "密码不一致"})

        is_correct_email = re.match("^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$", email)
        if is_correct_email is None:
            return JsonResponse({"res": 1, "errmsg": "邮箱格式不正确"})

        user = LoginUsers.objects.filter(user_name=user_name)
        if user:
            return JsonResponse({"res": 1, "errmsg": "用户名已存在"})
        else:
            user_count = LoginUsers.objects.all().count()
            user_add = LoginUsers(user_id=user_count + 1, user_name=user_name, user_pwd=password_1, user_level=user_level,
                                  user_email=email)
            user_add.save()
            return JsonResponse({"res": 0, "errmsg": "注册成功"})


def sessionm(request):
    username = check_user_auth(request)
    if username == "":
        return render(request, "WebVul/login.html")
    else:
        return render(request, "WebVul/sessionm.html", locals())


# 404页面
def page_not_found(request, exception):
    return render(request, "WebVul/404.html", status=404)


# 普通登录
def login_b(request):
    return render(request, "WebVul/login_b.html")


def login_b_submit(request):
    # 使用request.POST.get来获取相关的参数
    username = request.POST.get("username")
    password = request.POST.get("password")
    # 模拟判断账号密码是否正确
    if "zrl" == username and "zrl" == password:
        # 如果账号密码正确，重定向至首页
        return redirect("/index")
    else:
        # 如果错误重定向到登录页面
        return redirect("/login_b")


def cookie_set(request):
    response = HttpResponse("<h1>Set Cookie</h1>")
    response.set_cookie('Name', '123')
    return response


def cookie_get(request):
    response = HttpResponse("读取cookie信息：</br>")
    if 'Name' in request.COOKIES:
        response.write('<h1>' + request.COOKIES['Name'] + '</h1>')
    return response


def session_set(request):
    request.session['key'] = "hello"
    return HttpResponse('写入session')


def session_get(request):
    h1 = request.session.get('key')
    return HttpResponse(h1)


def vul_pages(request):
    username = check_user_auth(request)
    if username == "":
        return render(request, "WebVul/login.html")
    else:
        return render(request, "WebVul/vul_pages.html", locals())


def query_pages(request):
    pages_list = Vul_Pages.objects.all()
    username = check_user_auth(request)
    if username == "":
        return render(request, "WebVul/login.html")
    else:
        return render(request, "WebVul/vul_pages.html", locals())


def insert_page(request):
    vul_title = request.POST.get("vul_title")
    vul_name = request.POST.get("vul_name")
    vul_page = request.POST.get("vul_page")
    page_count = Vul_Pages.objects.all().count()
    print(page_count)
    # 模拟判断账号密码是否正确
    if vul_name == "" or vul_page == "":
        return JsonResponse({"res": 2})
    else:
        try:
            page_info = Vul_Pages(vul_id=page_count + 1, vul_name=vul_name, vul_title=vul_title, vul_page=vul_page)
            page_info.save()
            return JsonResponse({"res": 1})
        except LoginUsers.DoesNotExist:
            return JsonResponse({"res": 0})


def retrieve_vul_info(vul_type):
    BASE_DIR = Path(__file__).resolve().parent.parent
    vul_desc_path = os.path.join(BASE_DIR, 'templates/WebVul/VulDesc/')
    vul_desc_file = vul_desc_path + vul_type + ".json"
    with open(vul_desc_file, 'r') as vul_d:
        vul_details = json.load(vul_d)
    return vul_details


