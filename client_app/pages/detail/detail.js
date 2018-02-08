var config = require('../../utils/config');
var utils = require('../../utils/util.js');
const app = getApp();
var fid = 0;
var mid = 0;
var openid = '';

Page({
  data: {
    ad:[],
    detail:{},
    vote:{},
    misc:{},
    indicatorDots: false,
    autoplay: true,
    interval: 3000,
    duration: 1000,
    photo:[],
    img_height:400,
    media:config.api.url+"/media/",
  },

  onLoad: function (options) {
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
                      url: config.api.api_weixin2+"?mid="+mid,
                      data: {url:'https://api.weixin.qq.com/sns/jscode2session?js_code=' + code + '&grant_type=authorization_code'},
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
              url: config.api.detail,
              data: {fid:fid}
          };

            //发送数据请求
            utils.request(option,
                function (res) {
                    var detail = res.data.detail;
                    var photo = [];
                    if(detail.fields.image0 != null && detail.fields.image0 !=''){
                      photo.push(detail.fields.image0);
                    }
                    if(detail.fields.image1 != null && detail.fields.image1 !=''){
                      photo.push(detail.fields.image1);
                    }

                    if(detail.fields.image2 != null &&  detail.fields.image2 !=''){
                      photo.push(detail.fields.image2);
                    }

                    if(detail.fields.image3 != null && detail.fields.image3 !=''){
                      photo.push(detail.fields.image3);
                    }

                    if(detail.fields.image4 != null && detail.fields.image4 !=''){
                      photo.push(detail.fields.image4);
                    }

                    that.setData({
                      detail:detail,
                      vote:res.data.vote,
                      ad:res.data.ad,
                      misc:res.data.misc,
                      photo:photo,
                    });
                    utils.hideLoading();

                    wx.setNavigationBarTitle({
                      title: detail.fields.username,
                    });

                })
        },

  goVote:function(){
        var that = this;
        utils.showLoading();

          var option = {
              header: { "Content-Type": "application/x-www-form-urlencoded" },   //post提交需要加这一行
              url: config.api.vote_post,
              method:'POST',
              data: {
                mid:that.data.detail.fields.mid,
                fid:fid,
                vid:that.data.detail.fields.vid,
                openid:openid,
              }
          };

          //发送数据请求
          utils.request(option,
              function (res) {
                utils.hideLoading();
                if(res.data.result == 'success'){
                    utils.alert_msg('投票成功!','success');
                    var detail = that.data.detail;
                    detail['fields']['ticket'] = res.data.ticket;
                    that.setData({
                      detail:detail,
                    });

                }else{
                      //utils.alert_msg(res.data.message,'error');
                      wx.showModal({
                        title: '提示',
                        showCancel:false,
                        content: res.data.message,
                      });
                }
          });
  },



  imageLoad: function(e) {
       var that = this;
       var width=e.detail.width, height=e.detail.height;   //获取图片真实宽度
       that.setData({
         img_height:height,
       });
    },


    goDefault:function(){
      var that = this;
      wx.reLaunch({
          url: '../default/default?vid='+that.data.detail.fields.vid+'&mid='+mid,
      });
    },


  goSend:function(){
    var that = this;
    wx.navigateTo({
      url: '/pages/pay/pay?vid='+that.data.detail.fields.vid + "&fid=" + fid,
    })
  },
  goSign:function(){
    wx.switchTab({
      url: '/pages/sign/sign'
    })
  },


  onShareAppMessage: function (res) {
    var that = this;
    if (res.from === 'button') {
      // 来自页面内转发按钮
    }
    return {
      title: that.data.vote.fields.title + "-" + that.data.detail.fields.username,
      imageUrl:that.data.media + that.data.detail.fields.image0,
      path: '/pages/detail/detail?fid=' + fid,
      success: function (res) {
        // 转发成功
      },
      fail: function (res) {
        // 转发失败
      }
    }
  },


})
