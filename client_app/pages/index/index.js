//index.js
//获取应用实例
var currentPage = 1;//当前页,默认 第一页
var config = require('../../utils/config');
var utils = require('../../utils/util.js');

const app = getApp()

Page({
  data:{
      keyword:'',
      list:[],
      media:config.api.url+"/media/",
    },

    onLoad: function (options) {

    },

    onShow: function() {
      var that = this;
      this.setData({
          list: [],
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
            url: config.api.vote_list,
            data: {page:currentPage}
        };

        //发送数据请求
        utils.request(option,
            function (res) {
                var tmp = res.data;
                var list = tmp.list;
                for (var i = 0; i < list.length; i++) {
                  var aa = list[i].fields.pub_date;
                  list[i].fields.pub_date = aa.substr(0,10);
                }
                that.setData({
                  list:that.data.list.concat(tmp.list)
                });

                currentPage++;
                utils.hideLoading();
            })

    },


    bindViewTap: function (e) {
      var data = e.currentTarget.dataset;
      wx.reLaunch({
          url: '../default/default?vid='+data.id+'&mid='+data.mid,
      });
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
            url: config.api.search_index,
            method:'POST',
            data: {
              keyword:keyword
            }
        };
        utils.request(option,
            function (res) {
              utils.hideLoading();
              if(res.data.result == 'success'){
                wx.reLaunch({
                    url: '../default/default?vid='+keyword+'&mid='+res.data.mid
                });
              }else{
                  utils.alert_msg('无记录!','success');
              }
        });


      },






    onShareAppMessage: function (res) {
      var that = this;
      if (res.from === 'button') {
        // 来自页面内转发按钮
      }
      return {
        title: '懒人投票',
        path: '/pages/index/index',
        success: function (res) {
          // 转发成功
        },
        fail: function (res) {
          // 转发失败
        }
      }
    },


})
