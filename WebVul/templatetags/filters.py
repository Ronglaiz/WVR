from django.template import Library

# 创建一个Library对象
register = Library()


# 使用装饰器进行注册
@register.filter
# 定义判断奇偶函数mod，将value 对 2 求余
def mod(value):
    return value % 2 == 0
