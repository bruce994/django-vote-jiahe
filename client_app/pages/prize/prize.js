var config = require('../../utils/config');
var utils = require('../../utils/util.js');
var WxParse = require('../../wxParse/wxParse.js');

const app = getApp();
var vid = 0;
var mid = 0;

Page({
  data: {
    vote:{},
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
  },

  fetchData: function () {
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
                  vote:res.data.vote,
                });
                utils.hideLoading();

                var vote = res.data.vote;
                //富文本
                WxParse.wxParse('html_content', 'html', vote.prize, that, 0);
                //END

            });


    },

})
