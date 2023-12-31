import hashlib

from django.conf import settings


def md5(string):
    """MD5加密"""
    hash_obj = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))
    hash_obj.update(string.encode('utf-8'))
    return hash_obj.hexdigest()
