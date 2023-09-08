import requests
from django import forms
from web import models
from django.conf import settings

from django_redis import get_redis_connection

from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from utils.tencent.sms import send_sms_single
from utils.encrypt import md5
from web.forms.bootstarp import BootStarpForm
import random

""" 用户注册form """


class RegisterModelForm(BootStarpForm, forms.ModelForm):
    # 自定义表单手机号校验
    mobile = forms.CharField(label='手机', validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$', '手机号错误')])
    password = forms.CharField(
        label='密码',
        min_length=8,
        max_length=16,
        error_messages={
            'min_length': "密码长度不能小于8个字符",
            'max_length': "密码长度不能大于16个字符",
        },
        widget=forms.PasswordInput()
    )
    confirm_password = forms.CharField(
        label='重复密码',
        min_length=8,
        max_length=16,
        error_messages={
            'min_length': "重复密码长度不能小于8个字符",
            'max_length': "重复密码长度不能大于16个字符",
        },
        widget=forms.PasswordInput()
    )
    code = forms.CharField(label='验证码')

    class Meta:
        model = models.UserInfo
        fields = ['username', 'email', 'password', 'confirm_password', 'mobile', 'code']

    def clean_username(self):
        username = self.cleaned_data['username']
        # 判断用户名是否cunz
        exists = models.UserInfo.objects.filter(username=username).exists()
        if exists:
            raise ValidationError("用户名已存在")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        # 判断用户名是否cunz
        exists = models.UserInfo.objects.filter(email=email).exists()
        if exists:
            raise ValidationError("邮箱已存在")
        return email

    def clean_password(self):
        pwd = self.cleaned_data['password']
        # 密码加密并返回
        return md5(pwd)

    def clean_confirm_password(self):
        pwd = self.cleaned_data['password']
        confirm_pwd = md5(self.cleaned_data['confirm_password'])
        if pwd != confirm_pwd:
            raise ValidationError("输入密码不一致")
        return confirm_pwd

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        exists = models.UserInfo.objects.filter(mobile=mobile).exists()
        if exists:
            raise ValidationError("手机号已存在")
        return mobile

    def clean_code(self):
        code = self.cleaned_data['code']
        mobile = self.cleaned_data['mobile']
        # redis 验证
        conn = get_redis_connection()
        redis_code = conn.get(mobile)
        if not redis_code:
            raise ValidationError("验证码失效或未发送，请重新发送")
        redis_str_code = redis_code.decode('utf-8')
        if code.strip() != redis_str_code:
            raise ValidationError("验证码错误，请重新输入")
        return code


"""用于发送短信"""


class SendSmsForm(forms.Form):
    mobile = forms.CharField(label='手机', validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$', '手机号错误')])

    # 重写init方法，传入request对象
    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def clean_mobile(self):
        """手机号验证的勾子"""
        mobile = self.cleaned_data['mobile']

        # 判断短信模板是否有问题
        tpl = self.request.GET.get('tpl')
        template_id = settings.TENCENT_SMS_TEMPLATE_ID[tpl]
        if not template_id:
            raise ValidationError('短信模板错误')

        # 查看数据库中是否存在已注册号码
        exists = models.UserInfo.objects.filter(mobile=mobile).exists()
        if tpl == 'login':
            if not exists:
                raise ValidationError('手机号未注册，请输入正确手机号')
            else:
                pass
        # 发送短信 & 写入redis
        # 生成随机验证码
        code = random.randrange(1000, 9999)
        # 发送短信
        sms = send_sms_single(mobile, template_id, [code, ])
        if sms['result'] != 0:
            raise ValidationError("短信发送失败,{}".format(sms['errmsg']))
        # 验证码写入redis（django-redis）
        conn = get_redis_connection()
        conn.set(mobile, code, ex=60)
        return mobile


"""  短信登陆form """


class LoginSmsForm(BootStarpForm, forms.Form):
    mobile = forms.CharField(label='手机', validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$', '手机号错误')])
    code = forms.CharField(
        label='验证码',
        widget=forms.TextInput()
    )

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        # user_obj = models.UserInfo.objects.filter(mobile=mobile).first()
        exists = models.UserInfo.objects.filter(mobile=mobile).exists()
        if not exists:
            raise ValidationError("手机号未注册，请先注册")
        return mobile

    def clean_code(self):
        code = self.cleaned_data['code']
        mobile = self.cleaned_data.get('mobile')
        # 手机号不存在，则不需要校验验证码
        if not mobile:
            return code
        # redis 验证

        conn = get_redis_connection()
        redis_code = conn.get(mobile)
        # 校验验证码的同时未校验对应手机号，存在BUG
        if not redis_code:
            raise ValidationError("验证码失效或未发送，请重新发送")
        redis_str_code = redis_code.decode('utf-8')
        if code.strip() != redis_str_code:
            raise ValidationError("验证码错误，请重新输入")
        return code


""" 用户账户密码登陆 """


class LoginPwdForm(BootStarpForm, forms.Form):
    username = forms.CharField(label='邮箱或手机号')
    password = forms.CharField(label='密码', widget=forms.PasswordInput(render_value=True))
    code = forms.CharField(label='图片验证码')

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def clean_password(self):
        pwd = self.cleaned_data['password']
        # 密码加密并返回
        return md5(pwd)

    def clean_code(self):
        code = self.cleaned_data['code']
        # 获取session中存入的 image_code
        session_code = self.request.session.get('image_code')
        if not session_code:
            raise ValidationError('验证码已过期')
        if code.strip().upper() != session_code.strip().upper():
            raise ValidationError('验证码输入错误')
        return code
