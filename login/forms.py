from django import forms
from login import models

from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


class RegisterModelForm(forms.ModelForm):
    # 自定义表单手机号校验
    mobile = forms.CharField(label='手机', validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$', '手机号错误')])
    password = forms.CharField(label='密码', widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='重复密码')
    code = forms.CharField(label='验证码')

    class Meta:
        model = models.UserInfo
        fields = ['username','email','password','confirm_password','mobile','code']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, filed in self.fields.items():
            filed.widget.attrs['class'] = 'form-control'
            filed.widget.attrs['placeholder'] = '请输入%s' % (filed.label,)
