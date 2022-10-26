from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template import loader
from django.shortcuts import redirect
from WebVul.models import LoginUsers
from WebVul.models import VulInfo


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
        #获取字典的内容并传入页面文件
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


# 插入数据到vulinfo表
def query_vul(request):
    vul_list = VulInfo.objects.all()
    username = check_user_auth(request)
    if username == "":
        return render(request, "WebVul/login.html")
    else:
        return render(request, "WebVul/xss.html", locals())

# 查询vulinfo表
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
    return render(request, "WebVul/sqli.html")


# 跳转到xss
def xssi(request):
    username = check_user_auth(request)
    if username == "":
        return render(request, "WebVul/login.html")
    else:
        return render(request, "WebVul/xss.html", locals())


# 跳转到cmdi
def cmdi(request):
    return render(request, "WebVul/cmdi.html")


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
