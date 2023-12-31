"""
Django settings for saas project.

Generated by 'django-admin startproject' using Django 4.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-p$dtny@$#(!szrig_ha)jl4m%932p)n%@8dhinct2%l=8=5h4^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'login.apps.LoginConfig',
    'web'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'web.middleware.auth.AuthMiddleware'
]

ROOT_URLCONF = 'saas.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'saas.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # 默认
        'NAME': 'saas',  # 连接的数据库  #一定要存在的数据库名
        'HOST': '127.0.0.1',  # mysql的ip地址
        'PORT': 3306,  # mysql的端口
        'USER': 'admin',  # mysql的用户名
        'PASSWORD': '123'  # mysql的密码
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 配置腾讯云短信
# 以下配置信息已全部隐藏个人信息内容
TENCENT_SMS_SECRET_ID = "AKIDfzDLNGyUq3DD5Sl"  # API秘钥管理SecretId
TENCENT_SMS_SECRET_KEY = "IPOH1crfP4as45zmTinfN1"  # API秘钥管理SecretKey

TENCENT_SMS_APP_ID = '836346'  # 应用列表SDK AppID
TENCENT_SMS_APP_KEY = 'd8b208a066'
TENCENT_SMS_SIGN = '香蛋公众号'  # 签名管理的内容

# # 正文模板管理ID
TENCENT_SMS_TEMPLATE_ID = {
    'login': 1855800,  # 登录模板ID
    'register': 1855832,  # 注册模板ID
    're_password': 1855833,  # 改密模板ID
}

# 网站登陆白名单
WHITE_REGEX_URL_LIST = {
    '/',
    '/web/register/',
    '/web/login_sms/',
    '/web/login_pwd/',
    '/web/image_code/',
    '/web/send_sms/',
}
# 配置个人本地私有配置文件:local_settings

try:
    from .local_settings import *
except ImportError:
    pass
