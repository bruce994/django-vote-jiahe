from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^index/?$', views.index, name='index'),
    url(r'^detail/?$', views.detail, name='detail'),
    url(r'^gift/?$', views.gift, name='gift'),
    url(r'^api_weixin/$', views.api_weixin, name='api_weixin'),
    url(r'^vote_post/$', views.vote_post, name='vote_post'),
    url(r'^rank/$', views.rank, name='rank'),
    url(r'^sign/$', views.sign, name='sign'),
    url(r'^userinfo/$', views.userinfo, name='userinfo'),
    url(r'^vote_list/$', views.vote_list, name='vote_list'),
    url(r'^userinfo_post/$', views.userinfo_post, name='userinfo_post'),
    url(r'^image_post/$', views.image_post, name='image_post'),
    url(r'^sign_post/$', views.sign_post, name='sign_post'),
    url(r'^search/$', views.search, name='search'),
    url(r'^search_index/$', views.search_index, name='search_index'),
    url(r'^ordering_post/$', views.ordering_post, name='ordering_post'),
    url(r'^ordering_update/(?P<id>[0-9]+)/$', views.ordering_update, name='ordering_update'),
    url(r'^wxpay/$', views.wxpay, name='wxpay'),
    url(r'^wxpay_notify/$', views.wxpay_notify, name='wxpay_notify'),
]



