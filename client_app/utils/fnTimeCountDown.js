
var fnTimeCountDown = function(initObj){
	initObj = initObj || {};
	this.endTime = initObj.endTime || "1514649600";	//结束时间
	this.name = initObj.name;							//当前计时器在计时器数组对象中的名字
	this.intervarID;									//计时ID
}

fnTimeCountDown.prototype = {
		start: function(self){
			var that = this;
			var wxTimerList = self.data.wxTimerList;
			function begin(){
							//更新计时器数组
							wxTimerList[that.name] = {
								hm:that.dv().hm,
								sec:that.dv().sec,
								mini:that.dv().mini,
								hour:that.dv().hour,
								day:that.dv().day,
								month:that.dv().month,
								year:that.dv().year,
							};
							self.setData({
									wxTimerList:wxTimerList,
							});
			}
			begin();
			this.intervarID = setInterval(begin,1000);
		},

		dv:function(){
		  var that = this;
			//d = d || Date.UTC(2050, 0, 1); //如果未定义时间，则我们设定倒计时日期是2050年1月1日
			var now = new Date();
			//现在将来秒差值
			//alert(future.getTimezoneOffset());
			var dur = (that.endTime - now.getTime()) / 1000 ,mss = that.endTime - now.getTime();
			var pms = {
				hm:"000",
				sec: "00",
				mini: "00",
				hour: "00",
				day: "00",
				month: "00",
				year: "0"
			};
			if(mss > 0){
				pms.hm = that.haomiao(mss % 1000);
				pms.sec = that.zero(dur % 60);
				pms.mini = Math.floor((dur / 60)) > 0? that.zero(Math.floor((dur / 60)) % 60) : "00";
				pms.hour = Math.floor((dur / 3600)) > 0? that.zero(Math.floor((dur / 3600)) % 24) : "00";
				pms.day = Math.floor((dur / 86400)) > 0? that.zero(Math.floor((dur / 86400))) : "00";// % 30
				//月份，以实际平均每月秒数计算
				pms.month = Math.floor((dur / 2629744)) > 0? that.zero(Math.floor((dur / 2629744)) % 12) : "00";
				//年份，按按回归年365天5时48分46秒算
				pms.year = Math.floor((dur / 31556926)) > 0? Math.floor((dur / 31556926)) : "0";
			}else{
				pms.year=pms.month=pms.day=pms.hour=pms.mini=pms.sec="00";
				pms.hm = "000";
				clearInterval(this.intervarID);
			}
			return pms;
	},

	haomiao: function(n){
		if(n < 10)return "00" + n.toString();
		if(n < 100)return "0" + n.toString();
		return n.toString();
	},

	zero: function(n){
		var n = parseInt(n, 10);//解析字符串,返回整数
		if(n > 0){
			if(n <= 9){
				n = "0" + n;
			}
			return String(n);
		}else{
			return "00";
		}
	},
}

module.exports = fnTimeCountDown;
