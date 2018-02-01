  var config = require('../../utils/config');
  var utils = require('../../utils/util.js');
  const app = getApp();
  var currentPage = 1;//当前页,默认 第一页
  var vid = 0;
  Page({
    data: {
      ad:[],
      list:[],
      vote:{},
      indicatorDots: false,
      autoplay: true,
      interval: 3000,
      duration: 1000,
      photo:[],
      media:config.api.url+"/media/",
    },

  onLoad: function (options) {
    //vid = options.fid;
    let g_vid = app.g_vid;
    vid = g_vid;
  },

  onShow: function() {
    var that = this;
    that.setData({
      list:[],
    });
    currentPage = 1;
    that.fetchData();
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
              url: config.api.rank,
              data: {page:currentPage,vid:vid}
          };

            //发送数据请求
            utils.request(option,
                function (res) {
                    var tmp = res.data.list;
                    var vote = res.data.vote;
                    that.setData({
                      list:that.data.list.concat(tmp),
                      vote:vote,
                      ad:res.data.ad,
                    });
                    currentPage++;
                    utils.hideLoading();
                })
        },




        goDetail: function (e) {
          var data = e.currentTarget.dataset;
          wx.navigateTo({
            url: '/pages/detail/detail?fid='+data.id
          })
        },


})
