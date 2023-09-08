import os
import sys
import django


# 首先，一定要把当前项目的路径加到python模块搜索的路径里
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

# 设置django配置文件的路径在哪
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'saas.settings')
django.setup()  # 伪造让django启动

# 将项目目录添加到模块搜索路径才能导入下面的，否则可能报错


# 执行一些操作
from web import models
from utils.encrypt import md5
models.UserInfo.objects.create(username='Mo',email="colinma@gmail.com",mobile="1888888889",
                               password=md5("12345678")
                               )
