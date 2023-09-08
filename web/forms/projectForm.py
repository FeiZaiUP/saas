import requests
from django import forms
from web import models
from django.conf import settings
from django.core.exceptions import ValidationError

from web.forms.bootstarp import BootStarpForm
import random


class ProjectModelForm(BootStarpForm, forms.ModelForm):
    # desc = forms.CharField(widget=forms.Textarea())

    class Meta:
        model = models.Project
        fields = ['name', 'color', 'desc']
        widgets = {
            'desc': forms.Textarea
        }

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def clean_name(self):
        """项目创建校验"""
        # 1、判断当前用户 的项目是否已存在
        print(self.request.tracer.user)
        # user = self.request.tracer.user
        name = self.cleaned_data['name']
        exists = models.Project.objects.filter(name=name, creator=self.request.tracer.user).exists()
        if exists:
            raise ValidationError('项目名已存在')
        # 2、用户是否有项目额度
        # 总的用户额度
        # max = self.request.tracer.price_policy.project_num
        # 用户已使用额度
        count = models.Project.objects.filter(creator=self.request.tracer.user).count()
        if count >= self.request.tracer.price_policy.project_num:
            raise ValidationError('项目额度已用完，请重新购额度或升级更高额度版本')
        return name
