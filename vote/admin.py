from django.contrib import admin

# Register your models here.
from .models import Template,Vote,Form,Gift,Userinfo,Record,Ordering,Pay,Ad,Setting

from django.forms import TextInput, Textarea
from django.db import models

from django.core.urlresolvers import reverse
from tinymce.widgets import TinyMCE
from django.contrib.auth.admin import UserAdmin


from django.contrib.admin import AdminSite
from django.utils.translation import ugettext_lazy

class TemplateAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ('title','folder','p_picurl')
    search_fields = ['title']

class VoteAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ('title','mid_name','view','start_date','end_date','cknums','sort_field','sort','status_name','pub_date')
    search_fields = ['title']
    exclude = ('mid',) #隐藏字段
    def save_model(self, request, obj, form, change):
        if not change : #添加
            obj.mid = request.user.id  #获取登陆用户
        super().save_model(request, obj, form, change)

     #设置只显示当前登录用户填报条目（对于管理员显示全部模型条目）
    def get_queryset(self, request):
        qs = super(VoteAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(mid=request.user.id)



class FormAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ('username','mid_name','wx_name','num','ticket','tel','p_image','vid','status_name','pub_date')
    search_fields = ['username']
    exclude = ('mid',) #隐藏字段
    def save_model(self, request, obj, form, change):
        if not change : #添加
            obj.mid = request.user.id  #获取登陆用户
        super().save_model(request, obj, form, change)
     #设置只显示当前登录用户填报条目（对于管理员显示全部模型条目）
    def get_queryset(self, request):
        qs = super(FormAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(mid=request.user.id)



class GiftAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ('title','mid_name','ticket','price','vid','attr','sort')
    search_fields = ['title']
    exclude = ('mid',) #隐藏字段
    def save_model(self, request, obj, form, change):
        if not change : #添加
            obj.mid = request.user.id  #获取登陆用户
        super().save_model(request, obj, form, change)
     #设置只显示当前登录用户填报条目（对于管理员显示全部模型条目）
    def get_queryset(self, request):
        qs = super(GiftAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(mid=request.user.id)




class UserinfoAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ('nickName','mid_name','avatar_picurl','gender','city','province','country','language','pub_date')
    search_fields = ['title']
    fieldsets = [
        (None,               {'fields': ['nickName']}),
        (None,               {'fields': ['avatarUrl']}),
        (None,               {'fields': ['gender']}),
        (None,               {'fields': ['city']}),
        (None,               {'fields': ['province']}),
        (None,               {'fields': ['country']}),
        (None,               {'fields': ['language']}),
    ]
    exclude = ('mid',) #隐藏字段
    def save_model(self, request, obj, form, change):
        if not change : #添加
            obj.mid = request.user.id  #获取登陆用户
        super().save_model(request, obj, form, change)
     #设置只显示当前登录用户填报条目（对于管理员显示全部模型条目）
    def get_queryset(self, request):
        qs = super(UserinfoAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(mid=request.user.id)




class RecordAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ('fid_name','mid_name','vid_name','wx_name','pay_name','IP','summary','pub_date')
    search_fields = ['IP']
    exclude = ('mid',) #隐藏字段
    def save_model(self, request, obj, form, change):
        if not change : #添加
            obj.mid = request.user.id  #获取登陆用户
        super().save_model(request, obj, form, change)
     #设置只显示当前登录用户填报条目（对于管理员显示全部模型条目）
    def get_queryset(self, request):
        qs = super(RecordAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(mid=request.user.id)





class OrderingAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ('id','mid_name','vid_name','fid_name','wx_name','gift_name','num','total_price','status_name','pub_date')
    list_filter = ['pub_date']
    search_fields = ['id']
    exclude = ('mid',) #隐藏字段
    readonly_fields = ('id','num','total_fee','status','gift_id','openid','fid','vid',)
    def save_model(self, request, obj, form, change):
        if not change : #添加
            obj.mid = request.user.id  #获取登陆用户
        super().save_model(request, obj, form, change)
     #设置只显示当前登录用户填报条目（对于管理员显示全部模型条目）
    def get_queryset(self, request):
        qs = super(OrderingAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(mid=request.user.id)

    actions = None
    list_display_links = None
    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
    def get_actions(self, request):
        actions = super(OrderingAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
            return actions



class PayAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ('orderid','mid_name','payment','transaction_id','pay_time','openid','status','total_fee','summary','pub_date')
    search_fields = ['orderid__id']  #由于orderid_id是外键
    exclude = ('mid',) #隐藏字段
    readonly_fields = ('id','payment','transaction_id','pay_time','openid','status','total_fee','orderid','mid',)
    def save_model(self, request, obj, form, change):
        if not change : #添加
            obj.mid = request.user.id  #获取登陆用户
        super().save_model(request, obj, form, change)
     #设置只显示当前登录用户填报条目（对于管理员显示全部模型条目）
    def get_queryset(self, request):
        qs = super(PayAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(mid=request.user.id)
    actions = None
    #list_display_links = None
    #禁用删除
    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
    def get_actions(self, request):
        actions = super(PayAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
            return actions






class AdAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ('title','mid_name','vid','pub_date')
    search_fields = ['title']
    fieldsets = [
        (None,               {'fields': ['title']}),
        (None,               {'fields': ['vid']}),
        (None,               {'fields': ['image']}),
    ]
    def save_model(self, request, obj, form, change):
        if not change : #添加
            obj.mid = request.user.id  #获取登陆用户
        super().save_model(request, obj, form, change)
     #设置只显示当前登录用户填报条目（对于管理员显示全部模型条目）
    def get_queryset(self, request):
        qs = super(AdAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(mid=request.user.id)


class SettingAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ('mid_name','appId','appSecret','mch_id','merchant_key','notify_url')
    exclude = ('mid',) #隐藏字段
    def save_model(self, request, obj, form, change):
        if not change : #添加
            obj.mid = request.user.id  #获取登陆用户
        super().save_model(request, obj, form, change)

     #设置只显示当前登录用户填报条目（对于管理员显示全部模型条目）
    def get_queryset(self, request):
        qs = super(SettingAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(mid=request.user.id)

    def has_add_permission(self, request):
        	return False if self.model.objects.count() > 0 else super().has_add_permission(request)


class MyAdminSite(AdminSite):
    # Text to put at the end of each page's <title>.
    site_title = ugettext_lazy('My site admin')
    # Text to put in each page's <h1> (and above login form).
    site_header = ugettext_lazy('My administration')
    # Text to put at the top of the admin index page.
    index_title = ugettext_lazy('Site administration')

admin_site = MyAdminSite()



admin.site.register(Setting, SettingAdmin)
admin.site.register(Ad, AdAdmin)
admin.site.register(Template, TemplateAdmin)
admin.site.register(Vote, VoteAdmin)
admin.site.register(Form, FormAdmin)
admin.site.register(Gift, GiftAdmin)
admin.site.register(Userinfo, UserinfoAdmin)
admin.site.register(Record, RecordAdmin)
admin.site.register(Ordering, OrderingAdmin)
admin.site.register(Pay, PayAdmin)

UserAdmin.list_display += ('date_joined',)
UserAdmin.list_display += ('last_login',)

admin.site.site_header = "懒人CMS管理系统"
