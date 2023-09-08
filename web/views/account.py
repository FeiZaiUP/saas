import datetime

from django.shortcuts import render, HttpResponse, redirect
from web.forms.accountForm import RegisterModelForm, SendSmsForm, LoginSmsForm, LoginPwdForm
from utils.tencent.sms import send_sms_single
from django.http import JsonResponse
from django.conf import settings
from web import models
from django.db.models import Q
from utils.image_code import check_code
from io import BytesIO
import random
import uuid
import json


def index(request):
    """网站首页"""
    return render(request, 'index.html')


def register(request):
    """注册"""
    if request.method == 'GET':
        form = RegisterModelForm()
        return render(request, 'register.html', {'form': form})
    form = RegisterModelForm(data=request.POST)
    if form.is_valid():
        # 写入数据库
        # instance = form.save() 在数据库新增一条数据，并将新增数据赋值给instance
        instance = form.save()

        # 创建交易记录,默认注册后使用"个人免费版"
        # 方式一 （对应auth中间件中获取用户额度策略方式一）
        policy_object = models.PricePolicy.objects.filter(category=1, title='个人免费版').first()
        print(policy_object)
        models.Transaction.objects.create(
            status=2,
            order=str(uuid.uuid4()),
            user=instance,
            price_policy=policy_object,
            count=0,
            price=0,
            start_datetime=datetime.datetime.now(),
        )

        # 方式一 （对应auth中间件中获取用户额度策略方式一）

        return JsonResponse({'status': True, 'data': '/web/login_sms/'})
    return JsonResponse({'status': False, 'error': form.errors})


def send_sms(request):
    """发送短信"""
    form = SendSmsForm(request, data=request.GET)
    if form.is_valid():
        # 校验成功表示 钩子函数内数据校验通过
        return JsonResponse({'status': True})
    # 校验不通过返回错误信息
    return JsonResponse({'status': False, 'error': form.errors})


def login_sms(request):
    """短信登陆"""
    if request.method == 'GET':
        form = LoginSmsForm()
        return render(request, 'login_sms.html', {'form': form})
    form = LoginSmsForm(data=request.POST)
    if form.is_valid():
        mobile = form.cleaned_data['mobile']
        # 用户信息存入session
        user_obj = models.UserInfo.objects.filter(mobile=mobile).first()
        request.session['user_id'] = user_obj.id
        request.session.set_expiry(60 * 60 * 24 * 7)
        return JsonResponse({'status': True, 'data': "/"})
    return JsonResponse({'status': False, 'error': form.errors})


def login_pwd(request):
    """ 用户账户密码登陆 """
    if request.method == 'GET':
        form = LoginPwdForm(request)
        return render(request, 'login_pwd.html', {'form': form})
    form = LoginPwdForm(request, data=request.POST)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        # user_obj = models.UserInfo.objects.filter(username=username,password=password).first()
        user_obj = models.UserInfo.objects.filter(Q(email=username) | Q(mobile=username)).\
            filter(password=password).first()
        if user_obj:
            request.session['user_id'] = user_obj.id
            request.session.set_expiry(60 * 60 * 24 * 7)
            return redirect('/')
        form.add_error('username', '用户名或密码错误')
    return render(request, 'login_pwd.html', {'form': form})


def image_code(request):
    """图片验证码"""
    image_object, code = check_code()
    request.session['image_code'] = code
    request.session.set_expiry(60)
    # 写入内存
    stream = BytesIO()
    image_object.save(stream, 'png')
    print("验证码:" + code)

    return HttpResponse(stream.getvalue())


def logout(request):
    request.session.flush()
    return redirect('/')
