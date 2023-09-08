from django.db import models


# Create your models here.
class UserInfo(models.Model):
    username = models.CharField(verbose_name='用户', max_length=32)
    email = models.EmailField(verbose_name='邮箱', max_length=32)
    mobile = models.CharField(verbose_name='手机', max_length=32)
    password = models.CharField(verbose_name='密码', max_length=32)

    def __str__(self):
        return self.username