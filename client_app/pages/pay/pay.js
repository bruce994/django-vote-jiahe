var config = require('../../utils/config');
var utils = require('../../utils/util.js');
const app = getApp();
var vid = 0;
var fid = 0;
var mid = 0;
var openid = '';
var check_idx = 0;

Page({
  data: {
    num:0,
    form:{},
    ps:"",
    price:0,
    list:[],
    media:config.api.url+"/media/",
  },

  onLoad: function (options) {
    vid = options.vid;
    fid = options.fid;

    let g_mid = app.g_mid;
    mid = g_mid;
  },

    onShow: function() {
      var that = this;
      that.fetchData();

            wx.checkSession({
              success: function(e){
                  var user_info = wx.getStorageSync('user_info');
                  wx.getUserInfo({
                      success:function(res){
                          var option = {
                              header: { "Content-Type": "application/x-www-form-urlencoded" },   //post提交需要加这一行
                              url: config.api.userinfo,
                              method:'POST',
                              data: {
                                openid:user_info.openid,
                              }
                          };
                          utils.request(option,
                              function (res) {
                                if(res.data.result == 'success'){
                                    var detail = res.data.detail;
                                    openid = detail[0].fields.openid;
                                }else{
                                    that.login(config);
                                }
                          });

                       }
                  });
              },
              fail: function(){
                  that.login(config);
               }
             });

    },


        login: function(config){
          var that = this;
          //登陆
          wx.login({
              success:function(resLogin){
                  var code = resLogin.code; //返回code
                  wx.request({
                        url: config.api.api_weixin,
                        data: {url:'https://api.weixin.qq.com/sns/jscode2session?appid=' + config.appId + '&secret=' + config.secret + '&js_code=' + code + '&grant_type=authorization_code'},
                        header: {
                          "Content-Type": "application/x-www-form-urlencoded"
                         },
                         method:'POST',
                         success: function (res) {
                           var openid = res.data.openid; //返回openid
                           wx.getUserInfo({
                               success:function(res){
                                   var userInfo = res.userInfo;
                                   var option = {
                                       header: { "Content-Type": "application/x-www-form-urlencoded" },   //post提交需要加这一行
                                       url: config.api.userinfo_post,
                                       method:'POST',
                                       data: {
                                         openid:openid,
                                         nickName:userInfo.nickName,
                                         avatarUrl:userInfo.avatarUrl,
                                         gender:userInfo.gender,
                                         city:userInfo.city,
                                         province:userInfo.province,
                                         country:userInfo.country,
                                         language:userInfo.language,
                                         mid:mid,
                                       }
                                   };
                                   utils.request(option,
                                       function (res) {
                                         if(res.data.result == 'success'){
                                              var result = {"userInfo":userInfo,"openid":openid,"uid":res.data.uid};
                                              wx.setStorageSync('user_info', result);
                                              openid = openid;
                                         }

                                   });

                               }
                           });

                         }
                    });
              }
          });
          //END
        },


        fetchData: function () {//获取列表信息
            var that = this;
            utils.showLoading();
            var option = {
                url: config.api.gift,
                data: {vid:vid,fid:fid}
            };

              //发送数据请求
              utils.request(option,
                  function (res) {
                      var list = res.data.list;
                      var form = res.data.form;
                      for (var i = 0; i < list.length; i++) {
                        list[i]['isCheck'] = false;
                      }
                      that.setData({
                        list:list,
                        form:form[0],
                      });
                      utils.hideLoading();


                      if(list.length > 0){
                        list[0]['isCheck'] = true;
                        that.setData({
                          list:list,
                          ps:list[0].fields.price+"元打赏"+list[0].fields.title+"，"+list[0].fields.title+"等于"+list[0].fields.ticket+"票",
                          price:list[0].fields.price,
                        });
                      }


                  })
          },



  check:function(e){
    var that=this;
    var idx = e.currentTarget.dataset.idx;
    check_idx = idx;
    var list = that.data.list;
    for (var i = 0; i < list.length; i++) {
      list[i]['isCheck'] = false;
    }
    list[idx]['isCheck'] = true;

    var ps = list[idx].fields.price+"元打赏"+list[idx].fields.title+"，"+list[idx].fields.title+"等于"+list[idx].fields.ticket+"票";
    if(list[idx].fields.attr == 1){   //自定义
       ps = list[idx].fields.price+"元打赏1钻"+"，1钻等于"+list[idx].fields.ticket+"票";
    }

    that.setData({
      list:list,
      ps:ps,
      price:list[idx].fields.price,
    });
  },


  goVideoDetail:function(){
    wx.navigateTo({
      url: '/pages/videoDetail/videoDetail',
    })
  },
  tabMatch: function () {
    var that = this;
    var isMatch = that.data.isMatch;
    if (isMatch) {
      isMatch = false;
    } else {
      isMatch = true;
    }
    that.setData({
      isMatch: isMatch
    })
  },


  inputNumber:function(e){
     var that = this;
     var list = that.data.list;
     var num = e.detail.value;
     var price = list[check_idx].fields.price * num
     this.setData({
       num:num,
       price:price,
     });

  },

  goPay:function(){
    var that = this;
    var list = that.data.list;
    if(list.length == 0){
      utils.alert_msg('礼物未设置!','error');
      return;
    }

    var num = parseInt(that.data.num);
    if(list[check_idx].fields.attr == 1){  //选中自定义
      if(num == 0){
        utils.alert_msg('请输入钻石数!','error');
        return;
      }
    }else{
      num = 1;
    }

    var price = list[check_idx].fields.price * num;
    var gift_id = list[check_idx].pk;

    //var mid = list[check_idx].fields.mid;  //这里方便给用户测试，应该直接调用 config.mid

    utils.showLoading();

    var option = {
        header: { "Content-Type": "application/x-www-form-urlencoded" },   //post提交需要加这一行
        url: config.api.ordering_post,
        method:'POST',
        data: {
          vid:vid,
          fid:fid,
          gift_id:gift_id,
          mid:mid,
          openid:openid,
          num:num,
          total_fee:price,
        }
    };

    //发送数据请求
    utils.request(option,
        function (res) {
          utils.hideLoading();
          if(res.data.result == 'success'){
              utils.alert_msg('订单提交成功!','success');

              //订单号
              var ordering_id = res.data.id;
              var totalPrice = price * 100;

              wx.request({
                header: { "Content-Type": "application/x-www-form-urlencoded" },   //post提交需要加这一行
                url: config.api.wxpay,
                method:'POST',
                data: {
                  appid:config.appId,
                  mch_id:config.mch_id,
                  body:'投票',
                  out_trade_no:ordering_id,  //商品订单号
                  total_fee:totalPrice,
                  //total_fee:1,
                  notify_url:config.api.wxpay_notify,
                  attach: '投票',
                  trade_type:'JSAPI',
                  openid:openid,
                  merchant_key:config.merchant_key
                },

                 success: function (res) {
                   wx.requestPayment({
                     timeStamp: res.data.timeStamp,
                     nonceStr: res.data.nonceStr,
                     package: res.data.package,
                     signType: res.data.signType,
                     paySign: res.data.paySign,
                     'success': function (res) {

                       wx.showModal({
                         title: '提示',
                         showCancel:false,
                         content: '支付成功',
                         success: function(res) {
                           if (res.confirm) {
                             wx.navigateTo({
                               url: '../detail/detail?fid='+fid,
                             });
                           }
                         },
                       });

                     },
                     'fail': function (res) {
                      //商户订单支付失败需要生成新单号重新发起支付
                      var option = {
                          url: config.api.ordering_update+ordering_id,
                          data: {}
                      };
                      utils.request(option,function (res) {});
                      //END

                        utils.alert_msg('支付失败!','error');


                     }
                   })
                 }
               });
          }else{
              wx.showModal({
                title: '提示',
                showCancel:false,
                content: res.data.message,
              });
          }


        }
    );


  },





})
