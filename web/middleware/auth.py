import datetime

from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
from django.conf import settings
from web import models


class Tracer(object):
    """封装对象
     request.tracer.user          获取当前登录用户对象
    request.tracer.price_policy    获取当前登录用户价格策略对象
    """
    def __init__(self):
        self.user = None
        self.price_policy = None


class AuthMiddleware(MiddlewareMixin):
    """
    request.tracer.user          获取当前登录用户对象
    request.tracer.price_policy    获取当前登录用户价格策略对象
    """

    @staticmethod
    def process_request(request):
        request.tracer = Tracer()

        user_id = request.session.get('user_id', 0)
        user_obj = models.UserInfo.objects.filter(id=user_id).first()
        request.tracer.user = user_obj

        # 白名单: 用户未登录可以访问的URL
        """
            1.获取当前用户访问的url
            2.检查url是否在url白名单
        """
        if request.path_info in settings.WHITE_REGEX_URL_LIST:
            return
        # settings.WHITE_REGEX_URL_LIST
        #
        # """
        # 当前页不是白名单时，则判断用户是否登录，未登录则跳转到登录页
        # """
        if not request.tracer.user:
            return redirect('/web/login_pwd/')

        # 检查用户是否已登录，访问后台管理时，获取用户所拥有的额度
        # 方式1、免费额度在交易中存储

        # 获取当前用户id值最大（最近交易记录）
        _object = models.Transaction.objects.filter(user=user_obj, status=2).order_by('-id').first()
        # 判断是否已过期
        current_datetime = datetime.datetime.now()
        # 过期时间存在 且 小于当前时间，则表示订单已过期，额度则为免费额度（免费版 无结束时间）
        if _object.end_datetime and _object.end_datetime < current_datetime:
            _object = models.Transaction.objects.filter(user=user_obj, status=2, price_policy__category=1) \
                .order_by('-id')
        # request.price_policy = _object.price_policy
        request.tracer.price_policy = _object.price_policy

        # 方式2、免费额度存储配置文件
        # 获取当前用户id值最大（最近交易记录）
        """
        _object = models.Transaction.objects.filter(user=user_obj, status=2).order_by('-id').first()
        if not _object:
            # 免费版
            request.price_policy = models.PricePolicy.objects.filter(category=1,title='个人免费版').first()
        else:
            # 付费版
            current_datetime = datetime.datetime.now()
            if _object.end_datetime and _object.end_datetime < current_datetime:
                # 已过期
                request.price_policy = models.PricePolicy.objects.filter(category=1, title='个人免费版').first()
            else:
                # 未过期则采用当前购买规格策略
                request.price_policy = _object.price_policy
        """
