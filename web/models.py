from django.db import models


# Create your models here.
# db_index 创建索引

class UserInfo(models.Model):
    username = models.CharField(verbose_name='用户', max_length=32, db_index=True)
    email = models.EmailField(verbose_name='邮箱', max_length=32)
    mobile = models.CharField(verbose_name='手机', max_length=32)
    password = models.CharField(verbose_name='密码', max_length=32)
    
    # price_policy = models.ForeignKey(verbose_name='价格策略', to=PricePolicy, null=True, blank=True)

    def __str__(self):
        return self.username


class PricePolicy(models.Model):
    """价格策略"""
    category_choices = (
        (1, '个人免费版'),
        (2, 'VIP优享版'),
        (3, 'VIP尊享版')
    )
    category = models.SmallIntegerField(verbose_name='收费类型', default=1)
    title = models.CharField(verbose_name='标题', max_length=32)
    price = models.PositiveIntegerField(verbose_name='价格')  # 正整数

    project_num = models.PositiveIntegerField(verbose_name='项目数')
    project_member = models.PositiveIntegerField(verbose_name='项目成员数')
    project_space = models.PositiveIntegerField(verbose_name='单项目空间')
    project_size = models.PositiveIntegerField(verbose_name='单文件大小')

    create_datetime = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)


class Transaction(models.Model):
    """订单表"""
    status_choices = (
        (1, '未支付'),
        (2, '已支付'),
    )

    status = models.SmallIntegerField(verbose_name='状态', choices=status_choices)

    order = models.CharField(verbose_name='订单号', max_length=64, unique=True)  # 唯一索引

    user = models.ForeignKey(verbose_name='用户', to='UserInfo', on_delete=models.SET_NULL, blank=True, null=True)
    price_policy = models.ForeignKey(verbose_name='价格策略', to='PricePolicy', on_delete=models.SET_NULL,blank=True,
                                     null=True)

    count = models.IntegerField(verbose_name='数量（年）', help_text='0表示无限期')

    price = models.IntegerField(verbose_name='实际支付价格')

    start_datetime = models.DateTimeField(verbose_name='开始时间', null=True, blank=True)
    end_datetime = models.DateTimeField(verbose_name='结束时间', null=True, blank=True)

    create_datetime = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)


class Project(models.Model):
    """项目表"""
    color_choices = (
        (1, '#56b8eb'),
        (2, '#f28033'),
        (3, '#ebc656'),
        (4, '#a2d148'),
        (5, '#20BFA4'),
        (6, '#7461c2'),
        (7, '#20bfa3'),
    )
    name = models.CharField(verbose_name='项目名', max_length=32)
    color = models.SmallIntegerField(verbose_name='颜色', choices=color_choices, default=1)
    desc = models.CharField(verbose_name='项目描述', max_length=255, null=True, blank=True)
    use_space = models.IntegerField(verbose_name='项目已使用空间', default=0)
    star = models.BooleanField(verbose_name='星标', default=False)
    
    join_count = models.SmallIntegerField(verbose_name='参与人数', default=1)
    creator = models.ForeignKey(verbose_name='创建作者',to=UserInfo,on_delete=models.SET_NULL,blank=True, null=True)
    create_datetime = models.DateTimeField(verbose_name='新创建时间', auto_now_add=True)


class ProjiectUser(models.Model):
    """参与人员表"""
    user = models.ForeignKey(verbose_name='用户', to=UserInfo, related_name='projects', on_delete=models.CASCADE)
    project = models.ForeignKey(verbose_name='项目', to=Project,on_delete=models.SET_NULL,blank=True, null=True)

    # invitee = models.ForeignKey(verbose_name='邀请者', to=UserInfo, related_name='invitees', null=True, blank=True)

    star = models.BooleanField(verbose_name='星标', default=False)

    create_datetime = models.DateTimeField(verbose_name='加入时间', auto_now_add=True)