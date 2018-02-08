var config = require('../../utils/config');
var utils = require('../../utils/util.js');
var WxParse = require('../../wxParse/wxParse.js');
var fnTimeCountDown = require('../../utils/fnTimeCountDown.js');

var currentPage = 1;//当前页,默认 第一页
var mid = 0;
var openid = '';
var vid = 0;
const app = getApp();

Page({
  data: {
    auditd_check:0,
    keyword:'',
    wxTimerList:{},
    list:[],
    ad:[],
    vote:{},
    misc:{},
    isMore:true,
    indicatorDots: false,
    autoplay: true,
    interval: 3000,
    duration: 1000,
    array: ['请选择参赛组别','美国', '中国', '巴西', '日本'],
    index:0,
    media:config.api.url+"/media/",
  },
  onLoad: function (options) {
    var that = this;
    vid = options.vid;
    mid = options.mid;
    let g_vid = vid;  //定义全局变量
    let g_mid = mid;  //定义全局变量
    app.g_vid = g_vid;
    app.g_mid = g_mid;

  },

  onReady:function(){

  },

      onShow: function() {
        var that = this;

        that.setData({
          list:[],
        });
        currentPage = 1;
        that.fetchData();

              wx.checkSession({
                success: function(e){
                     var user_info = wx.getStorageSync('user_info');
                     //console.log(user_info);
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
                                      var openid = detail[0].fields.openid;
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
                                     mid:mid
                                   }
                               };
                               utils.request(option,
                                   function (res) {
                                     if(res.data.result == 'success'){
                                          var result = {"userInfo":userInfo,"openid":openid,"uid":res.data.uid};
                                          wx.setStorageSync('user_info', result);
                                          openid = openid;
                                          //console.log(result);
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

    onPullDownRefresh: function () { //下拉刷新
        currentPage = 1;
        this.setData({
            list: [],
        });
        this.fetchData();
        setTimeout(function () {
            wx.stopPullDownRefresh();
        }, 1000);
    },
    onReachBottom: function () { // 上拉加载更多
        // Do something when page reach bottom.
        this.fetchData();
    },


    fetchData: function () {//获取列表信息
        var that = this;
        utils.showLoading();
        var option = {
            url: config.api.index,
            data: {page:currentPage,vid:vid}
        };

          //发送数据请求
          utils.request(option,
              function (res) {
                  var tmp = res.data.list;
                  var vote = res.data.vote;
                  var isMore = true;
                  if(tmp.length == 0){
                    isMore = false;
                  }
                  that.setData({
                    auditd_check:res.data.auditd_check,
                    list:that.data.list.concat(tmp),
                    vote:vote,
                    ad:res.data.ad,
                    isMore:isMore,
                    misc:res.data.misc,
                  });
                  currentPage++;
                  utils.hideLoading();

                  wx.setNavigationBarTitle({
                    title: vote.fields.title,
                  });


                  var end_date = vote.fields.end_date;
                  end_date = new Date(end_date);
                  end_date = end_date.getTime()
                  var wxTimer = new fnTimeCountDown({
                      endTime:end_date,
                      name:'dtime',
                  })
                  wxTimer.start(that);

                  //富文本
                  WxParse.wxParse('html_content', 'html', vote.fields.content, that, 0);
                  //END
              });
      },


  goMore: function (e) {
    var that = this;
    that.fetchData();
  },


  inputKeyword:function(e){
     var that = this;
     var v = e.detail.value;
     this.setData({
       keyword:v,
     });
  },



  goSearch:function(){
    var that = this;
    var keyword = that.data.keyword;
    if(keyword == ""){
      utils.alert_msg('请输入关键字!','error');
      return;
    }

    utils.showLoading();
    var option = {
        header: { "Content-Type": "application/x-www-form-urlencoded" },   //post提交需要加这一行
        url: config.api.search,
        method:'POST',
        data: {
          keyword:keyword,
          vid:vid,
        }
    };
    utils.request(option,
        function (res) {
          utils.hideLoading();
          if(res.data.result == 'success'){
            wx.navigateTo({
              url: '/pages/detail/detail?fid='+res.data.fid,
            });
          }else{
              utils.alert_msg('无记录!','success');
          }
    });


  },


  bindPickerChange: function (e) {
    console.log('picker发送选择改变，携带值为', e.detail.value)
    this.setData({
      index: e.detail.value
    })
  },
  goSign: function () {
    wx.switchTab({
      url: '/pages/sign/sign'
    })
  },
  goDetail: function (e) {
    var data = e.currentTarget.dataset;
    wx.navigateTo({
      url: '/pages/detail/detail?fid='+data.id
    })
  },


    onShareAppMessage: function (res) {
      var that = this;
      if (res.from === 'button') {
        // 来自页面内转发按钮
      }
      return {
        title: that.data.vote.fields.title,
        path: '/pages/default/default?vid='+vid,
        success: function (res) {
          // 转发成功
        },
        fail: function (res) {
          // 转发失败
        }
      }
    },


})
