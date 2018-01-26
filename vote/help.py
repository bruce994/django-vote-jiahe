from django.db import models
import datetime
import os, time, uuid
from django.utils.deconstruct import deconstructible

@deconstructible
class PathAndRename(object):
    def __init__(self, sub_path):
        self.path = sub_path
    def __call__(self, instance, filename):
        # eg: filename = 'my uploaded file.jpg'
        ext = filename.split('.')[-1]  #eg: 'jpg'
        uid = uuid.uuid4().hex[:10]    #eg: '567ae32f97'

        # eg: 'my-uploaded-file'
        new_name = '-'.join(filename.replace('.%s' % ext, '').split())

        # eg: 'my-uploaded-file_64c942aa64.jpg'
        renamed_filename = '%(new_name)s_%(uid)s.%(ext)s' % {'new_name': new_name, 'uid': uid, 'ext': ext}

        # eg: 'images/2017/01/29/my-uploaded-file_64c942aa64.jpg'
        return os.path.join(self.path, renamed_filename)

def date_compare(date,current_date,dd='%m-%d %H:%M'):
    seconds = (current_date -  date).total_seconds()
    if(seconds < 60):
        return '1分钟前'
    if(seconds < 600):
        return '10分钟前'
    if(seconds < 3600):
        return '1小时前'
    if(seconds < 3600 *24):
        return '1天前'
    if(seconds < 3600*24*30):
        return '一个月前'
    return date.strftime(dd)


def millions_formatter(num, m=10000):
    if num < m :
        return num
    # If the number evenly divides 1000000, you can convert its division of 1000000 to an integer
    if num % m == 0:
        num = int(num/m)
    else:
        # Otherwise use a floating representation
        num = float(num/m)
    return '{}万'.format(num)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip



def test1():
    return '3333'


