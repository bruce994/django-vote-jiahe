#coding:utf-8

import logging
import hashlib
import urllib
from urllib.request import urlopen
import uuid
import xml.etree.ElementTree as ET



def request(url, data, timeout=30):
    '''
    请求
    :param url:
    :param data:
    :return:
    '''
    req = urllib.request.Request(url, data.encode("utf-8"), headers={'Content-Type': 'application/xml'})
    try:
        result = urlopen(req, timeout=timeout).read()
        return result
    except Exception as e:
        logging.error(e)
        return False



def get_nonce_str():
    '''
    获取随机字符串
    :return:
    '''
    return str(uuid.uuid4()).replace('-', '')


def dict_to_xml(dict_data):
    '''
    dict to xml
    :param dict_data:
    :return:
    '''
    xml = ["<xml>"]
    for k, v in dict_data.items():
        xml.append("<{0}>{1}</{0}>".format(k, v))
    xml.append("</xml>")
    return "".join(xml)


def xml_to_dict(xml_data):
    '''
    xml to dict
    :param xml_data:
    :return:
    '''
    xml_dict = {}
    root = ET.fromstring(xml_data)
    for child in root:
        xml_dict[child.tag] = child.text
    return xml_dict



class WxPay(object):

    def __init__(self, merchant_key, *args, **kwargs):
        self.url = 'https://api.mch.weixin.qq.com/pay/unifiedorder'
        self.merchant_key = merchant_key
        self.pay_data = kwargs
        super(WxPay, self).__init__()


    def create_sign(self, pay_data):
        '''
        生成签名
        :return:
        '''
        stringA = '&'.join(["{0}={1}".format(k, pay_data.get(k))for k in sorted(pay_data)])
        stringSignTemp = '{0}&key={1}'.format(stringA, self.merchant_key)
        sign = hashlib.md5(stringSignTemp.encode('utf-8')).hexdigest()
        return sign.upper()

    def get_pay_info(self):
        '''
        获取支付信息
        :param xml_data:
        :return:
        '''
        sign = self.create_sign(self.pay_data)
        self.pay_data['sign'] = sign
        xml_data = dict_to_xml(self.pay_data)
        response = request(url=self.url, data=xml_data)

        #logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s', datefmt='%a, %d %b %Y %H:%M:%S', filename='myapp.log', filemode='w')
        #logging.info(xml_to_dict(response)) #定义一个日志文件，便于调试

        if response:
            prepay_id = xml_to_dict(response).get('prepay_id')
            paySign_data = {
                'appId': self.pay_data.get('appid'),
                'timeStamp': self.pay_data.get('out_trade_no'),
                'nonceStr': self.pay_data.get('nonce_str'),
                'package': 'prepay_id={0}'.format(prepay_id),
                'signType': 'MD5'
            }
            paySign = self.create_sign(paySign_data)
            paySign_data.pop('appId')
            paySign_data['paySign'] = paySign
            return paySign_data

        return False





