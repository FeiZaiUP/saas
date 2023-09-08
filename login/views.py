import random

from django.shortcuts import render, HttpResponse
from utils.tencent.sms import send_sms_single
from login.forms import RegisterModelForm


# Create your views here.
# def send_sms_code(request):
#     """发送短信
#     """
#
#     code = random.randrange(1000, 9999)
#     res = send_sms_single(17747466491, 1855800, [code, ])
#     print(res)
#     return HttpResponse('成功')


# # 模拟注册
# def register(request):
#     form = RegisterModelForm()
#     return render(request, 'login/register.html', {'form': form})
