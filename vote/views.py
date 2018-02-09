from django.shortcuts import render
from django.shortcuts import  get_object_or_404,render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.http import JsonResponse
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.db.models import F
import json,time,logging
from django.utils import timezone
import datetime
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.db import connection
from django.contrib.sessions.backends.db import SessionStore
from django.db.models import Sum
from django.db.models import Max
import urllib.request
import django.core.files
from django.conf import settings
# Create your views here.
from .models import Template,Vote,Ad,Form,Gift,Ordering,Pay,Record,Userinfo,Setting

from random import randint
from vote import help
from vote import wxpayClass

#logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s', datefmt='%a, %d %b %Y %H:%M:%S', filename='debug.log', filemode='w')



def vote_list(request):
    mid = request.GET.get('mid',0)
    latest_list = Vote.objects.filter( Q(status=1)).order_by('-pub_date')
    paginator = Paginator(latest_list, 10)
    page = request.GET.get('page')
    try:
        latest_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        latest_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        latest_list = '';
    latest_list_json  = serializers.serialize('json',latest_list)

    data = '{"list":'+latest_list_json+'}'
    return HttpResponse(data, content_type='json')




def index(request):
    vid = request.GET.get('vid',0)
    vote = Vote.objects.get(pk=vid)
    Vote.objects.filter(pk = vid ).update(view =  F('view') +1)
    vote_json  = serializers.serialize('json',[vote,])
    latest_list = Form.objects.filter(Q(vid = vid) & Q(status=1)).order_by('-pub_date')
    paginator = Paginator(latest_list, 10)
    page = request.GET.get('page')
    try:
        latest_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        latest_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        latest_list = '';
    latest_list_json  = serializers.serialize('json',latest_list)

    data1 = {}
    data1["form_num"] = Form.objects.filter(Q(vid = vid) & Q(status = 1)).count()
    tmp = Form.objects.filter(Q(vid = vid) & Q(status = 1)).aggregate(Sum('ticket'))
    data1["form_ticket"] = tmp['ticket__sum']

    ad = Ad.objects.filter(vid = vid).order_by('-pub_date')
    ad_json  = serializers.serialize('json',ad)

    data = '{"auditd_check":1,"misc":'+json.dumps(data1)+',"ad":'+ad_json+',"vote":'+vote_json[1:-1]+',"list":'+latest_list_json+'}'
    return HttpResponse(data, content_type='json')


def gift(request):
    fid = request.GET.get('fid',0)
    form = Form.objects.get(pk=fid)
    form_json  = serializers.serialize('json',[form,])
    vid = request.GET.get('vid',0)
    gift = Gift.objects.filter(vid = vid ).order_by("sort")
    gift_json  = serializers.serialize('json',gift)
    data = '{"form":'+form_json+',"list":'+gift_json+'}'
    return HttpResponse(data, content_type='json')



def detail(request):
    fid = request.GET.get('fid',0)
    form = Form.objects.get(pk=fid)
    form_json  = serializers.serialize('json',[form,])
    vid = form.vid_id
    vote = Vote.objects.get(pk=vid)
    Vote.objects.filter(pk = vid ).update(view =  F('view') +1)
    vote_json  = serializers.serialize('json',[vote,])

    data1 = {}
    cursor = connection.cursor()
    cursor.execute("select * from (SELECT id,ticket,@curRank := @curRank + 1 AS rank FROM vote_form p, (SELECT @curRank := 0) r  where vid_id="+str(vid)+" and status=1 ORDER BY  ticket desc) as b where b.id="+str(fid))
    rank = [item[2] for item in cursor.fetchall()]
    data1["rank"] = rank

    ad = Ad.objects.filter(vid = vid).order_by('-pub_date')
    ad_json  = serializers.serialize('json',ad)

    data = '{"misc":'+json.dumps(data1)+',"ad":'+ad_json+',"vote":'+vote_json[1:-1]+',"detail":'+form_json[1:-1]+'}'
    return HttpResponse(data, content_type='json')

def rank(request):
    vid = request.GET.get('vid',0)
    vote = Vote.objects.values("message").get(pk=vid)
    Vote.objects.filter(pk = vid ).update(view =  F('view') +1)
    vote_json  = json.dumps(vote)

    ad = Ad.objects.filter(vid = vid).order_by('-pub_date')
    ad_json  = serializers.serialize('json',ad)

    latest_list = Form.objects.filter(Q(vid = vid) & Q(status = 1)).order_by('-ticket')
    paginator = Paginator(latest_list, 10)
    page = request.GET.get('page')
    try:
        latest_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        latest_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        latest_list = '';
    latest_list_json  = serializers.serialize('json',latest_list)

    data = '{"ad":'+ad_json+',"vote":'+vote_json+',"list":'+latest_list_json+'}'
    return HttpResponse(data, content_type='json')


def sign(request):
    vid = request.GET.get('vid',0)
    vote = Vote.objects.values("id","mid","prize").get(pk=vid)
    ad = Ad.objects.filter(vid = vid).order_by('-pub_date')
    ad_json  = serializers.serialize('json',ad)
    data = '{"ad":'+ad_json+',"vote":'+json.dumps(vote)+'}'
    return HttpResponse(data, content_type='json')





@csrf_exempt
def search_index(request):
    mid = request.POST.get('mid',0)
    keyword = request.POST.get('keyword','')
    cc = Vote.objects.filter(Q(status=1) & Q(id=keyword)  ).values_list("mid",flat=True)[:1]
    if not cc :
        return HttpResponse('{"result":"error"}', content_type='json')
    cc = list(cc)
    return HttpResponse('{"result":"success","mid":'+str(cc[0])+'}', content_type='json')



@csrf_exempt
def search(request):
    vid = request.POST.get('vid',0)
    keyword = request.POST.get('keyword','')
    if keyword.isdigit():
        num = keyword
    else :
        num = 0
    form = Form.objects.filter(Q(vid=vid) & Q(status=1) & (Q(username__contains=keyword) | Q(num=num)) ).order_by('-pub_date').values_list("id",flat=True)[:1]
    if not form :
        return HttpResponse('{"result":"error"}', content_type='json')
    form = list(form)
    return HttpResponse('{"result":"success","fid":'+str(form[0])+'}', content_type='json')


@csrf_exempt
def sign_post(request):
    objects = Form()
    vid = request.POST.get('vid',0)
    openid = request.POST.get('openid','')
    vote = Vote.objects.values("sign_status","sign_repeat").get(pk=vid)
    objects.username = request.POST.get('username','')
    tmp = Form.objects.filter(Q(vid_id = vid) & Q(openid = openid) ).count()
    if tmp >= vote['sign_repeat'] :
        return HttpResponse('{"result":"error","message":"repeat"}', content_type='json')
    objects.mid = request.POST.get('mid',0)
    objects.vid_id = vid
    images = request.POST.get('images','')
    images = images.split(',')
    for idx,img in enumerate(images):
        if idx == 0 :
            objects.image0 = img
        elif idx == 1:
            objects.image1 = img
        elif idx == 2:
            objects.image2 = img
        elif idx == 3:
            objects.image3 = img
        elif idx == 4:
            objects.image4 = img
    tmp = Form.objects.filter(Q(vid = vid)).aggregate(Max('num'))
    if tmp['num__max'] is None:
        objects.num = 1
    else:
        objects.num = tmp['num__max'] + 1
    if vote['sign_status'] == 0:
        status = 1
    else :
        status = 0
    objects.status = status
    objects.openid = openid
    objects.save()
    id = objects.id

    return HttpResponse('{"result":"success","status":'+str(status)+',"id":'+str(id)+'}', content_type='json')


@csrf_exempt
def image_post(request):
    f = request.FILES['img']
    destination = open(settings.MEDIA_ROOT+'/uploads/'+f.name, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
    return HttpResponse(f.name)




@csrf_exempt
def vote_post(request):
    mid = request.POST.get('mid',0);
    fid = request.POST.get('fid',0);
    vid = request.POST.get('vid',0);
    openid = request.POST.get('openid','');
    IP = help.get_client_ip(request)
    #try :
    #    tmp = Form.objects.get(openid = openid )
    #    objects = tmp
    #    objects.login_count +=1
    #except ObjectDoesNotExist:
    #    objects = Userinfo()

    now = timezone.now()
    tmp = Vote.objects.filter(Q(id = vid) & Q(start_date__lte = now) & Q(end_date__gte = now)).count()
    if not tmp :
        return HttpResponse('{"result":"error","message":"活动过期或没有开始"}', content_type='json')

    tmp = Vote.objects.filter(Q(id = vid) & Q(v_start_date__lte = now) & Q(v_end_date__gte = now)).count()
    if not tmp :
        return HttpResponse('{"result":"error","message":"投票时间未开放"}', content_type='json')

    #tmp = Userinfo.objects.filter(Q(mid = mid) & Q(openid = openid) ).count()
    tmp = Userinfo.objects.filter( Q(openid = openid) ).count()
    if not tmp :
        return HttpResponse('{"result":"error","message":"小程序未授权,无法投票"}', content_type='json')


    #时间判断
    vote = Vote.objects.values('cknums').get(pk = vid)
    now = datetime.datetime.now()
    today_0 = datetime.datetime(now.year, now.month, now.day, 0, 0, 0)
    today_24 = datetime.datetime(now.year, now.month, now.day, 23, 59, 59)
    tmp = Record.objects.filter(Q(is_pay = 0) & Q(vid = vid) & Q(openid = openid) & Q(pub_date__gte = today_0)& Q(pub_date__lte = today_24)).count()
    if tmp >= vote['cknums']  :
        return HttpResponse('{"result":"error","message":"今天投票次数已用完"}', content_type='json')
    #END

    objects = Record()
    objects.mid = mid
    objects.fid = fid
    objects.vid = vid
    objects.openid = openid
    objects.IP = IP
    objects.save()
    id = objects.id

    Form.objects.filter(pk = fid ).update(ticket =  F('ticket') +1)
    form = Form.objects.values('ticket').get(pk = fid )

    return HttpResponse('{"result":"success","ticket":'+str(form['ticket'])+'}', content_type='json')


@csrf_exempt
def userinfo(request):
    try :
        objects = Userinfo.objects.filter(openid = request.POST.get('openid','') )
        if objects :
            latest_json  = serializers.serialize('json',objects)
            return HttpResponse('{"result":"success","detail":'+latest_json+'}', content_type='json')
        else:
            return HttpResponse('{"result":"error"}', content_type='json')
    except ObjectDoesNotExist:
        return HttpResponse('{"result":"error"}', content_type='json')


@csrf_exempt
def userinfo_post(request):
    try :
        tmp = Userinfo.objects.get(openid = request.POST.get('openid','') )
        objects = tmp
        objects.login_count +=1
    except ObjectDoesNotExist:
        objects = Userinfo()
    objects.openid = request.POST.get('openid','')
    objects.nickName = request.POST.get('nickName','')
    objects.avatarUrl = request.POST.get('avatarUrl','')
    objects.city = request.POST.get('city','')
    objects.gender = request.POST.get('gender',0)
    objects.language = request.POST.get('language','')
    objects.province = request.POST.get('province','')
    objects.country = request.POST.get('country','')
    objects.mid = request.POST.get('mid',0)
    objects.save()
    uid = objects.id
    return HttpResponse('{"result":"success","uid":'+str(uid)+'}', content_type='json')


@csrf_exempt
def ordering_post(request):
    mid = request.POST.get('mid',0)
    openid = request.POST.get('openid','');
    #tmp = Userinfo.objects.filter(Q(mid = mid) & Q(openid = openid) ).count()
    tmp = Userinfo.objects.filter(Q(openid = openid) ).count()
    if not tmp :
        return HttpResponse('{"result":"error","message":"小程序未授权,无法送礼物投票"}', content_type='json')

    try :
        tmp = Ordering.objects.get(pk = request.POST.get('id','') )
        objects = tmp
    except ObjectDoesNotExist:
        objects = Ordering()
        objects.mid = request.POST.get('mid',0)
        objects.vid = request.POST.get('vid',0)
        objects.fid = request.POST.get('fid',0)
        objects.gift_id = request.POST.get('gift_id',0)
        objects.num = request.POST.get('num',0)
        objects.openid = request.POST.get('openid','')
        objects.total_fee = request.POST.get('total_fee',0.00)
        objects.save()
        id = objects.id
        return HttpResponse('{"result":"success","id":'+str(id)+'}', content_type='json')


def ordering_update(request,id):
    n = 16
    new_id = ''.join(["%s" % randint(0, 9) for num in range(0, n)])   #随机数
    cursor = connection.cursor()
    cursor.execute("update vote_ordering set id='"+new_id+"' where id='"+id+"'")
    return HttpResponse('{"result":"success","id":'+str(new_id)+'}', content_type='json')




@csrf_exempt
def wxpay(request):
    #data = {
    #    'appid': 'wx76df4a73c8ecfc06',
    #    'mch_id': '1486279882',
    #    'nonce_str': wxpayClass.get_nonce_str(),
    #    'body': '测试',                              # 商品描述
    #    'out_trade_no': str(int(time.time())),       # 商户订单号
    #    'total_fee': '1',
    #    'spbill_create_ip': '123.12.12.123',
    #    'notify_url': 'https://django2.yy.lanrenmb.com/vote/wxpay_notify/',
    #    'attach': '{"msg": "自定义数据"}',
    #    'trade_type': 'JSAPI',
    #    'openid': 'oBxj00HJ_LpE7Mgw1A6OaB_cSWE0'
    #}
    #merchant_key = 'd32831100d1bf387d8faec783fde3888'

    data = {
        'appid': request.POST.get('appid',''),
        'mch_id': request.POST.get('mch_id',''),
        'nonce_str': wxpayClass.get_nonce_str(),
        'body': request.POST.get('body',''),                              # 商品描述
        'out_trade_no': request.POST.get('out_trade_no',''),       # 商户订单号
        'total_fee': request.POST.get('total_fee',1),
        'spbill_create_ip': help.get_client_ip(request),
        'notify_url': request.POST.get('notify_url',''),
        'attach': request.POST.get('attach',''),
        'trade_type': request.POST.get('trade_type',''),
        'openid': request.POST.get('openid','')
    }
    merchant_key = request.POST.get('merchant_key','')

    wxpay = wxpayClass.WxPay(merchant_key, **data)
    pay_info = wxpay.get_pay_info()
    if pay_info:
        return JsonResponse(pay_info)
    return JsonResponse({'errcode': 40001, 'errmsg': '请求支付失败'})





@csrf_exempt
def wxpay2(request):
    #data = {
    #    'appid': 'wx76df4a73c8ecfc06',
    #    'mch_id': '1486279882',
    #    'nonce_str': wxpayClass.get_nonce_str(),
    #    'body': '测试',                              # 商品描述
    #    'out_trade_no': str(int(time.time())),       # 商户订单号
    #    'total_fee': '1',
    #    'spbill_create_ip': '123.12.12.123',
    #    'notify_url': 'https://django2.yy.lanrenmb.com/vote/wxpay_notify/',
    #    'attach': '{"msg": "自定义数据"}',
    #    'trade_type': 'JSAPI',
    #    'openid': 'oBxj00HJ_LpE7Mgw1A6OaB_cSWE0'
    #}
    #merchant_key = 'd32831100d1bf387d8faec783fde3888'
    mid = request.POST.get('mid',0)
    setting = Setting.objects.get(mid=mid)
    data = {
        'appid': setting.appId,
        'mch_id': setting.mch_id,
        'nonce_str': wxpayClass.get_nonce_str(),
        'body': request.POST.get('body',''),                              # 商品描述
        'out_trade_no': request.POST.get('out_trade_no',''),       # 商户订单号
        'total_fee': request.POST.get('total_fee',1),
        'spbill_create_ip': help.get_client_ip(request),
        'notify_url': setting.notify_url,
        'attach': request.POST.get('attach',''),
        'trade_type': request.POST.get('trade_type',''),
        'openid': request.POST.get('openid','')
    }
    merchant_key = setting.merchant_key

    wxpay = wxpayClass.WxPay(merchant_key, **data)
    pay_info = wxpay.get_pay_info()
    if pay_info:
        return JsonResponse(pay_info)
    return JsonResponse({'errcode': 40001, 'errmsg': '请求支付失败'})




@csrf_exempt
def wxpay_notify(request):
        data = wxpayClass.xml_to_dict(request.body)
        if data['result_code'] == 'SUCCESS' :

            order = Ordering.objects.values("vid","mid","openid","fid","num","gift_id").get(pk = data['out_trade_no'] )

            objects = Pay.objects.filter(transaction_id=data['transaction_id'])
            if objects :
                if objects.status == 0 :
                    objects.status = 1
                    objects.pub_date = timezone.now()
                    objects.save()
            else :
                objects = Pay()
                objects.orderid_id = data['out_trade_no']
                objects.transaction_id = data['transaction_id']
                objects.pay_time = data['time_end']
                objects.openid = data['openid']
                objects.summary = data['attach']
                objects.status = 1
                objects.mid = order['mid']
                objects.total_fee = int(data['total_fee']) / 100.00
                objects.pub_date = timezone.now()
                objects.save()

            Ordering.objects.filter(pk = data['out_trade_no'] ).update(status=1)

            #增加票
            gift = Gift.objects.values("ticket").get(pk = order['gift_id'])
            ticket  = gift['ticket'] * order['num']
            Form.objects.filter(pk = order['fid'] ).update(ticket = F('ticket') + ticket )
            #END


            #插入投票记录
            IP = help.get_client_ip(request)
            querysetlist=[]
            for i in range(ticket):
                querysetlist.append(Record(mid=order['mid'],fid=order['fid'],vid=order['vid'],openid=order['openid'],IP=IP,is_pay=1))
            Record.objects.bulk_create(querysetlist)
            #END

            result_data = {
                'return_code': 'SUCCESS',
                'return_msg': 'OK'
            }
        else :
            result_data = {
                'return_code': 'FAIL',
                'return_msg': 'error'
            }
        data = wxpayClass.dict_to_xml(result_data)
        return HttpResponse(data, content_type='text/xml')


def setting(request):
    mid = request.GET.get('mid',0)
    setting = Setting.objects.filter(mid=mid)[:1]
    setting_json  = serializers.serialize('json',setting)
    data = setting_json[1:-1]
    return HttpResponse(data, content_type='json')


@csrf_exempt
def api_weixin(request):
    url = request.POST.get("url","")
    with urllib.request.urlopen(url) as response:
        result = response.read()
        return HttpResponse(result, content_type='json')

@csrf_exempt
def api_weixin2(request):
    url = request.POST.get("url","")
    mid = request.GET.get('mid',0)
    setting = Setting.objects.get(mid=mid)
    url = url +  '&appid=' + setting.appId + '&secret=' + setting.appSecret
    with urllib.request.urlopen(url) as response:
        result = response.read()
        return HttpResponse(result, content_type='json')
