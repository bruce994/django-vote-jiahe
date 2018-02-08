from django.db import models
from django.utils import timezone
from django.utils.deconstruct import deconstructible
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.functional import lazy
from django.db import connection
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
# Create your models here.
from vote import help

from tinymce.models import HTMLField
from filebrowser.fields import FileBrowseField
from random import randint
import datetime
import os, time, uuid

class Template(models.Model):
    title = models.CharField('模板名称',max_length=30,default='')
    folder = models.CharField('模板文件名',max_length=30,default='')
    image_path = time.strftime('images/%Y/%m/%d')
    picurl = models.ImageField(upload_to=help.PathAndRename(image_path),verbose_name="模板缩略图",max_length=500)
    status = models.IntegerField('状态',default=0,choices=[(0,"禁用"),(1,"启用")])

    def p_picurl(self):
        url =  '<img src="%s%s" width="%d" height="%d"/>' % (settings.MEDIA_URL,self.picurl,200,150)
        return '<a href="%s%s">%s</a>' % (settings.MEDIA_URL,self.picurl,url)
    p_picurl.allow_tags = True
    p_picurl.short_description = '模板缩略图'

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "界面风格"
        verbose_name_plural = "1.界面风格"



class Vote(models.Model):
    mid  = models.IntegerField('会员ID',default=0)
    title = models.CharField('活动主题',max_length=30,default='')
    message = models.CharField('公告',max_length=100,default='')
    image = FileBrowseField("图片", max_length=200, directory="uploads/", extensions=['.jpg','.jpeg','.gif','.png','.tif','.tiff'],default='', blank=True)
    view  = models.IntegerField('虚拟人气设置',default=1)
    start_date = models.DateTimeField('活动开始时间')
    end_date = models.DateTimeField('活动结束时间')
    v_start_date = models.DateTimeField('投票开始时间')
    v_end_date = models.DateTimeField('投票结束时间')
    cknums  = models.IntegerField('每人限制每天投多少票',default=1)
    sort_field = models.CharField('选手排序字段',max_length=30,default='pub_date',choices=[("pub_date","时间"),("num","投票号"),("ticket","票数")])
    status = models.IntegerField('状态',default=0,choices=[(0,"禁用"),(1,"启用")])
    sign_status = models.IntegerField('选手报名是否审核',default=0,choices=[(0,"不审核"),(1,"审核")])
    sign_repeat = models.IntegerField('一个微信号允许多少次报名',default=1)
    sort = models.IntegerField('排序',default=0,choices=[(0,"升序"),(1," 降序")])
    template_id  = models.ForeignKey(Template,verbose_name='模板界面风格')
    content = HTMLField('活动规则',default='',blank=True)
    prize = HTMLField('奖品',default='',blank=True)
    pub_date = models.DateTimeField('发布时间',auto_now_add=True)

    def __str__(self):
        return self.title

    def mid_name(self):
        tmp = User.objects.get(pk=self.mid)
        return  tmp.username
    mid_name.allow_tags = True
    mid_name.short_description = '会员'

    def status_name(self):
        return  self.status
    status_name.admin_order_field = 'status'
    status_name.boolean = True
    status_name.short_description = '状态'


    class Meta:
        verbose_name = "投票活动"
        verbose_name_plural = "2.投票活动"

class Ad(models.Model):
    mid  = models.IntegerField('会员ID',default=0)
    vid  = models.ForeignKey(Vote,verbose_name='活动')
    title = models.CharField('广告标题',max_length=30,default='')
    image = FileBrowseField("图片", max_length=200, directory="uploads/", extensions=['.jpg','.jpeg','.gif','.png','.tif','.tiff'],default='', blank=True)
    pub_date = models.DateTimeField('发布时间',auto_now_add=True)

    def __str__(self):
        return self.title

    def mid_name(self):
        tmp = User.objects.get(pk=self.mid)
        return  tmp.username
    mid_name.allow_tags = True
    mid_name.short_description = '会员'


    class Meta:
        verbose_name = "广告管理"
        verbose_name_plural = "3.广告管理"


class Form(models.Model):
    mid  = models.IntegerField('会员ID',default=0)
    vid  = models.ForeignKey(Vote,verbose_name='活动')
    openid = models.CharField("微信ID",max_length=200,default='',blank=True,db_index=True)
    username = models.CharField('姓名',max_length=30,default='')
    tel = models.CharField('电话',max_length=30,default='',blank=True)
    #image0 = FileBrowseField("照片1", max_length=200, directory="uploads/", extensions=['.jpg','.jpeg','.gif','.png','.tif','.tiff'], blank=True, null=True)
    image_path = time.strftime('images/%Y/%m/%d')
    image0 = models.ImageField(upload_to=help.PathAndRename(image_path),verbose_name="照片0",max_length=500,blank=True, default='')
    image_path = time.strftime('images/%Y/%m/%d')
    image1 = models.ImageField(upload_to=help.PathAndRename(image_path),verbose_name="照片1",max_length=500,blank=True, default='')
    image_path = time.strftime('images/%Y/%m/%d')
    image2 = models.ImageField(upload_to=help.PathAndRename(image_path),verbose_name="照片2",max_length=500,blank=True, default='')
    image_path = time.strftime('images/%Y/%m/%d')
    image3 = models.ImageField(upload_to=help.PathAndRename(image_path),verbose_name="照片3",max_length=500,blank=True, default='')
    image_path = time.strftime('images/%Y/%m/%d')
    image4 = models.ImageField(upload_to=help.PathAndRename(image_path),verbose_name="照片4",max_length=500,blank=True, default='')
    image_path = time.strftime('images/%Y/%m/%d')
    info = models.CharField('个人介绍',max_length=1000,default='',blank=True)
    num  = models.IntegerField('投票号',default=1)
    ticket = models.IntegerField('票数',default=0)
    pub_date = models.DateTimeField('发布时间',auto_now_add=True)
    status = models.IntegerField('状态',default=1,choices=[(0,"禁用"),(1,"启用")])

    def p_image(self):
        url =  '<img src="%s%s" width="%d" height="%d"/>' % (settings.MEDIA_URL,self.image0,50,80)
        return '<a href="%s%s">%s</a>' % (settings.MEDIA_URL,self.image0,url)
    p_image.allow_tags = True
    p_image.short_description = '模板缩略图'

    def wx_name(self):
        tmp = Userinfo.objects.values("nickName").get(openid=self.openid)
        return  tmp['nickName']
    wx_name.allow_tags = True
    wx_name.short_description = '微信用户'

    def mid_name(self):
        tmp = User.objects.get(pk=self.mid)
        return  tmp.username
    mid_name.allow_tags = True
    mid_name.short_description = '会员'

    def status_name(self):
        return  self.status
    status_name.admin_order_field = 'status'
    status_name.boolean = True
    status_name.short_description = '状态'


    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "选手"
        verbose_name_plural = "4.选手"



class Gift(models.Model):
    vid  = models.ForeignKey(Vote,verbose_name='活动')
    mid = models.IntegerField('会员ID',default=0)
    title = models.CharField('名称',max_length=30,default='')
    ticket = models.IntegerField('票数',default=1)
    price = models.FloatField('价格',default='0.00')
    image_path = time.strftime('images/%Y/%m/%d')
    picurl = models.ImageField(upload_to=help.PathAndRename(image_path),verbose_name="图片",max_length=500,blank=True, default='')
    attr = models.IntegerField('属性',default=0,choices=( (0, '不开启自定义'), (1, '开启自定义'),))
    sort = models.IntegerField('排序',default=0)
    def p_picurl(self):
            url =  '<img src="%s%s" width="%d" height="%d"/>' % (settings.MEDIA_URL,self.picurl,80,80)
            return '<a href="%s%s">%s</a>' % (settings.MEDIA_URL,self.picurl,url)
    p_picurl.allow_tags = True
    p_picurl.short_description = '图片'


    def mid_name(self):
        tmp = User.objects.get(pk=self.mid)
        return  tmp.username
    mid_name.allow_tags = True
    mid_name.short_description = '会员'


    def __str__(self):
        return self.title

    class Meta:
        ordering = ['sort']
        verbose_name = "礼物"
        verbose_name_plural = "5.礼物"



class Userinfo(models.Model):
    mid  = models.IntegerField('会员ID',default=0,db_index=True)
    openid = models.CharField(max_length=200,default='',db_index=True)
    image_path = time.strftime('images/%Y/%m/%d')
    avatarUrl = models.ImageField(upload_to=help.PathAndRename(image_path),verbose_name="头像",max_length=500,db_index=True)
    city = models.CharField('城市',max_length=20,default='')
    country = models.CharField('国家',max_length=20,default='')
    gender = models.CharField('姓别',max_length=1, choices=[("0","未知"),("1","男"),("2","女")],default='0')
    language = models.CharField('语言',max_length=20,default='')
    nickName = models.CharField('名称',max_length=20,default='')
    province = models.CharField('省份',max_length=20,default='')
    pub_date = models.DateTimeField('时间',auto_now_add=True)
    login_count  = models.IntegerField('登陆次数',default=1)
    login_date  = models.DateTimeField('最后登陆时间',auto_now=True)

    def avatar_picurl(self):
            return '<img src="%s" width="%d" height="%d"/>' % (self.avatarUrl,80,60)
    avatar_picurl.allow_tags = True
    avatar_picurl.short_description = '头像'

    def __str__(self):
        return self.nickName

    def mid_name(self):
        tmp = User.objects.get(pk=self.mid)
        return  tmp.username
    mid_name.allow_tags = True
    mid_name.short_description = '会员'

    class Meta:
        verbose_name = "微信用户"
        verbose_name_plural = "6.微信用户"

APPROVAL_CHOICES_2 = ( (0, '否'), (1, '否'),)
class Record(models.Model):
    mid  = models.IntegerField('会员ID',default=0)
    fid  = models.IntegerField('选手ID',default=0,db_index=True)
    vid  = models.IntegerField('活动ID',default=0,db_index=True)
    openid = models.CharField('微信ID',max_length=60,default='',db_index=True)
    IP = models.CharField('投票人IP',max_length=15,default='')
    summary = models.CharField('描述',max_length=100,default='')
    is_pay = models.IntegerField('是否支付投票',default=0,choices=APPROVAL_CHOICES_2)
    pub_date = models.DateTimeField('发布时间',auto_now_add=True,db_index=True)

    def __str__(self):
        return str(self.id)

    def wx_name(self):
        tmp = Userinfo.objects.values("nickName").get(openid=self.openid)
        return  tmp['nickName']
    wx_name.allow_tags = True
    wx_name.short_description = '微信用户'

    def vid_name(self):
        tmp = Vote.objects.get(pk=self.vid)
        return  tmp.title
    vid_name.allow_tags = True
    vid_name.short_description = '活动'

    def fid_name(self):
        tmp = Form.objects.get(pk=self.fid)
        return  tmp.username
    fid_name.allow_tags = True
    fid_name.short_description = '选手'

    def mid_name(self):
        tmp = User.objects.get(pk=self.mid)
        return  tmp.username
    mid_name.allow_tags = True
    mid_name.short_description = '会员'

    def pay_name(self):
        if self.is_pay == 0 :
            return  '<img src="/static/admin/img/icon-no.svg" alt="0">' + APPROVAL_CHOICES_2[self.is_pay][1]
        elif self.is_pay ==1 :
            return  '<img src="/static/admin/img/icon-yes.svg" alt="1">' + APPROVAL_CHOICES_2[self.is_pay][1]
    pay_name.admin_order_field = 'is_pay'
    pay_name.allow_tags = True
    pay_name.short_description = '是否付费'


    class Meta:
        verbose_name = "投票记录"
        verbose_name_plural = "7.投票记录"


APPROVAL_CHOICES_1 = ( (0, '未支付'), (1, '已支付'),)
class Ordering(models.Model):
    mid  = models.IntegerField('会员ID',default=0)
    id = models.CharField('订单号',primary_key=True, max_length=16)
    def save(self):
        if not self.id:
            n = 16
            self.id = ''.join(["%s" % randint(0, 9) for num in range(0, n)])   #随机数
            super(Ordering, self).save()

    vid  = models.IntegerField('活动ID',default=0)
    fid  = models.IntegerField('选手ID',default=0)
    openid  = models.CharField('微信openid',max_length=100,default='',db_index=True)
    gift_id  = models.IntegerField('礼物ID',default=0)
    num  = models.IntegerField('数量',default=0)
    status = models.IntegerField('状态',default=0,choices=APPROVAL_CHOICES_1)
    pub_date = models.DateTimeField('添加时间',auto_now_add=True)
    total_fee = models.FloatField('支付金额',default='0.00')

    def __str__(self):
        return self.id

    def wx_name(self):
        tmp = Userinfo.objects.values("nickName").get(openid=self.openid)
        return  tmp['nickName']
    wx_name.allow_tags = True
    wx_name.short_description = '微信用户'

    def vid_name(self):
        tmp = Vote.objects.get(pk=self.vid)
        return  tmp.title
    vid_name.allow_tags = True
    vid_name.short_description = '活动'

    def fid_name(self):
        tmp = Form.objects.get(pk=self.fid)
        return  tmp.username
    fid_name.allow_tags = True
    fid_name.short_description = '选手'

    def mid_name(self):
        tmp = User.objects.get(pk=self.mid)
        return  tmp.username
    mid_name.allow_tags = True
    mid_name.short_description = '会员'


    def gift_name(self):
        tmp = Gift.objects.get(pk=self.gift_id)
        return  tmp.title
    gift_name.allow_tags = True
    gift_name.short_description = '礼物'

    def total_price(self):
        P = Gift.objects.get(pk=self.gift_id)
        tmp = self.num * P.price
        return  tmp
    total_price.allow_tags = True
    total_price.short_description = '支付金额'

    def status_name(self):
        if self.status == 0 :
            return  '<img src="/static/admin/img/icon-no.svg" alt="0">' + APPROVAL_CHOICES_1[self.status][1]
        elif self.status ==1 :
            return  '<img src="/static/admin/img/icon-yes.svg" alt="1">' + APPROVAL_CHOICES_1[self.status][1]
    status_name.admin_order_field = 'status'
    status_name.allow_tags = True
    status_name.short_description = '状态'



    class Meta:
        ordering = ['-pub_date']
        verbose_name = "订单"
        verbose_name_plural = "8.订单"


class Pay(models.Model):
    mid  = models.IntegerField('会员ID',default=0)
    orderid  = models.ForeignKey(Ordering,verbose_name='支付单号')
    APPROVAL_CHOICES = ( ('weixin', '微信支付'), ('alipay', '支付宝'),)
    payment = models.CharField('付款方式',max_length=20,default='weixin',choices=APPROVAL_CHOICES)
    transaction_id = models.CharField('商户订单号',max_length=60,default='')
    pay_time = models.CharField('交易时间',max_length=60,default='')
    openid = models.CharField('微信ID',max_length=60,default='')
    APPROVAL_CHOICES = ( (0, '未支付'), (1, '已支付'),)
    status = models.IntegerField('状态',default=0,choices=APPROVAL_CHOICES)
    total_fee = models.FloatField('交易金额',default='0.00')
    summary = models.CharField('备注',max_length=100,default='')
    pub_date = models.DateTimeField('添加时间',auto_now_add=True)

    def mid_name(self):
        tmp = User.objects.get(pk=self.mid)
        return  tmp.username
    mid_name.allow_tags = True
    mid_name.short_description = '会员'

    def __str__(self):
        return str(self.orderid)

    class Meta:
        verbose_name = "支付记录"
        verbose_name_plural = "9.支付记录"


class Setting(models.Model):
    mid  = models.IntegerField('会员ID',default=0)
    appId = models.CharField('AppID(小程序ID',max_length=30,default='',blank=True)
    appSecret =  models.CharField('AppSecret(小程序密钥)',max_length=80,default='',blank=True)
    mch_id =  models.CharField('商户ID',max_length=20,default='',blank=True)
    merchant_key =  models.CharField('商户支付密钥',max_length=80,default='',blank=True)
    notify_url =  models.CharField('回调支付url地址',max_length=300,default='',blank=True)

    def mid_name(self):
        tmp = User.objects.get(pk=self.mid)
        return  tmp.username
    mid_name.allow_tags = True
    mid_name.short_description = '会员'

    class Meta:
        verbose_name = "系统参数设置"
        verbose_name_plural = "0.系统参数设置"





