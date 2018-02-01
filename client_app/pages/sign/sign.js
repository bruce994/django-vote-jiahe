var config = require('../../utils/config');
var utils = require('../../utils/util.js');
const app = getApp();
var vid = 0;
var mid = 0;
var openid = '';

Page({
  data: {
    ad:[],
    vote:{},
    value:{"username":""},
    image:[],
    indicatorDots: false,
    autoplay: true,
    interval: 3000,
    duration: 1000,
    media:config.api.url+"/media/",
  },

  onLoad: function (options) {
    //vid = options.fid;
    let g_vid = app.g_vid;
    vid = g_vid;

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
                url: config.api.sign,
                data: {vid:vid}
            };
              //发送数据请求
              utils.request(option,
                  function (res) {
                      that.setData({
                        ad:res.data.ad,
                        vote:res.data.vote,
                      });
                      utils.hideLoading();
                  });
          },



  inputUsername:function(e){
     var that = this;
     var v = e.detail.value;
     var value = that.data.value;
     value.username = v;
     this.setData({
       value:value,
     });
  },


  goSign:function(){
    var that = this;
    var value = that.data.value;
    var image = that.data.image;
    if(value.username == ""){
      utils.alert_msg('姓名不能为空!','error');
      return;
    }
    if(image.length == 0){
      utils.alert_msg('必须上传一张图片!','error');
      return;
    }

    if(image.length > 5){
      utils.alert_msg('最多长传5张图!','error');
      return;
    }

    if(openid == ''){
      wx.showModal({
        title: '提示',
        showCancel:false,
        content: '未授权小程序无法提交',
      });
      return;
    }

    var vote = that.data.vote;

    utils.showLoading();

    var option = {
        header: { "Content-Type": "application/x-www-form-urlencoded" },   //post提交需要加这一行
        url: config.api.sign_post,
        method:'POST',
        data: {
          username:value.username,
          vid:vid,
          mid:mid,
          openid:openid,
          images:image,
        }
    };
    //发送数据请求
    utils.request(option,
        function (res) {
          utils.hideLoading();
          if(res.data.result == 'success'){
              var message = '';
              if(res.data.status == 1){
                message = '报名成功';
              }else{
                message = '报名成功审核中...';
              }

              wx.showModal({
                title: '提示',
                showCancel:false,
                content: message,
                success: function(res) {
                  if (res.confirm) {
                    wx.reLaunch({
                        url: '../default/default?vid='+vid+'&mid='+mid,
                    });
                  }
                },
              });


          }else{
            if(res.data.message == 'repeat'){
                  wx.showModal({
                    title: '提示',
                    showCancel:false,
                    content: '您已经报名过,不能重复提交',
                  });
            }else{
              utils.alert_msg('报名失败成功!','success');
            }

          }
    });



  },


  addPic:function(){
    var that = this;
    var image = that.data.image;

     wx.chooseImage({
       count: 1, // 默认9
       sizeType: ['compressed'],
       success: function(res) {
         var tempFilePaths = res.tempFilePaths
         wx.uploadFile({
           url: config.api.image_post, // 你的接口地址
           filePath: tempFilePaths[0],
           name: "img",
           success: function(res){
             var data = res.data;
             image.push("uploads/"+data);
             that.setData({image: image})
           }
         })
       }
   })
  },


  delPic:function(e){
    var that = this;
    var image = that.data.image;
    var idx = e.currentTarget.dataset.idx;
    image.splice(idx, 1);
    that.setData({image: image})
  },





  bindPickerChange: function (e) {
    console.log('picker发送选择改变，携带值为', e.detail.value)
    this.setData({
      index: e.detail.value
    })
  },


})
