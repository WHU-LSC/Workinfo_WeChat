//index.js
//获取应用实例
const app = getApp()
// 发送引用请求
import { request } from "../../request/index.js"
import { formatDate } from "../../utils/util.js"

Page({
  data: {
    ShixiList_country:[],
    date:'',
    tabs:[
      {
        id:0,
        value:"今日更新",
        isActive:true
      },
      {
        id:1,
        value:"往日更新",
        isActive:false
      }
    ]
  },
  //事件处理函数
  bindViewTap: function() {
    wx.navigateTo({
      url: '../logs/logs'
    })
  },
  onLoad: function () {
    this.getShixiList();
    var DATE = formatDate(new Date());
    this.setData({
      date: DATE
    });
    console.log(this.data.date);

  } ,
  getShixiList(){
    request({url:"https://lsc.ngrok2.xiaomiqiu.cn/api/test"})
    //https://lsc.ngrok2.xiaomiqiu.cn/api/test
    //http://127.0.0.1:8080/api/test
    .then(result=>{
        this.setData({
          ShixiList_country:result.data.country
        }) 
    })
    wx:wx.stopPullDownRefresh();
  },
  onPullDownRefresh: function () {
    this.setData({
      ShixiList:[]
    })
    this.getShixiList();
  },
  handleTabsItemChange(e){
    const {index}=e.detail;
    let {tabs}=this.data;
    tabs.forEach((v,i) => i===index?v.isActive=true:v.isActive=false);
    this.setData({
      tabs
    })
  }
})
