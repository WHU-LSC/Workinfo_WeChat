// 处理请求

//同时发送异步代码次数时
let ajaxTimes=0;
export const request=(params)=>{
    ajaxTimes++;
    wx.showLoading({
        title:"加载中" ,
        mask: true
    });
    //定义公共url
    // const baseUrl="https://api-hmugo-web.itheima.net/api/public/v1";
    return new Promise((resolve,reject)=>{
        wx.request({
            ...params,
            // url:baseUrl+params.url,
            url:params.url,
            success:(result)=>{
                resolve(result);
            },
            fail:(err)=>{
                reject(err);
            },
            complete:()=>{
                ajaxTimes--;
                if(ajaxTimes===0){
                    wx.hideLoading();
                }
                
            }
        });
    })
    
}