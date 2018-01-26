# **仁裕元科技出品- 微信小程序拳击比赛** #

## 运行环境 ##
* Django 1.11.7
* mysql5.0以上
* apache、nginx

# 技术说明： #
##  一、基于Django 1.11.7框架  ##
* Django [https://www.djangoproject.com/](Link URL)



## docker 镜像如下： ##
```python

FROM django

MAINTAINER wang<1330407081@qq.com>

#COPY requirements.txt /usr/src/app/

RUN apt-get update &&  pip install Django==1.11.7 gunicorn==19.3.0  Pillow  django-tinymce  \
    && apt-get install -y \
    && apt-get clean; rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /usr/share/doc/* \
    && echo 'django.1.11.7 installed.'

```


