import pymysql
import pandas as pd
import datetime
from selenium import webdriver
import re
import sys
import os
import time
from  openpyxl import Workbook
from openpyxl.styles import Font,Alignment
import requests
from bs4 import BeautifulSoup
import urllib
from fontTools.ttLib import TTFont
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By 


#这里调用数据爬虫获得数据
def flatten(input_list):
    output_list = []
    while True:
        if input_list == []:
            break
        for index, i in enumerate(input_list):

            if type(i) == list:
                input_list = i + input_list[index + 1:]
                break
            else:
                output_list.append(i)
                input_list.pop(index)
                break
    return output_list
#整合数据用的函数
def zhenghe(a,b):#用于数据整合，避免使用numpy
    re=[]
    for x in a:
        re.append(x)
    for x in b:
        re.append(x)
    return re  
def get_info_yingjiesheng():
    print('开始抓取实习信息......\n')
    #加载启动项
    try:
        option = webdriver.ChromeOptions()
        option.add_argument('headless')
        #import win32com
        #应届生求职网的信息
        url = 'http://www.yingjiesheng.com/commend-parttime-1.html'
        wb_data = requests.get(url)
        soup = BeautifulSoup(wb_data.content, 'html.parser', from_encoding='utf-8')
        a = []
        time=[]
        result = []
        for link in soup.select('#mainNav > div.jobList > table > tr > td > a'):
                                #mainNav > div.jobList > table > tbody > tr:nth-child(22) > td.date
            a.append(str(link))
        for link in soup.select('#mainNav > div.jobList > table > tr > td.date'):
                                #mainNav > div.jobList > table > tbody > tr:nth-child(22) > td.date
            time.append(str(link))

        for i in range(len(a)):
            result.append([re.findall(r'<a href="(.*?)" target=',a[i]),
                           re.findall(r'#008000;">(.*?)</span>',a[i]),
                           re.findall(r'</span>(.*?)</a>',a[i]),
                           re.findall(r'<td class="date">(.*?)</td>',time[i])[0]])
        for i in range(len(result)):
            if result[i][-1][-5:]!=datetime.datetime.now().strftime('%m-%d'):
                result[i]=[]
        result=[x[1]+x[2]+x[0] for x in result if x!=[]]
        for i in range(len(result)):
            if len(result[i])!=3:
                result[i]=[]
        result=[x for x in result if x!=[]]
        for x in result:
            x[1]=x[1].split("招聘")
            if len(x[1])==1:
                x[1].append('实习生')
            elif len(x[1])!=2:
                del x[1][1]
                if x[1][1]=='':
                    x[1][1]='实习生'
            elif x[1][1]=='':
                x[1][1]='实习生'
            elif len(x[1])==1:
                x[1].append('实习生')
        result = [flatten(x) for x in result if x!=[]]
        for x in result:
            x[1]=x[1].replace('实习生','')
            x[1]=x[1].replace('2020','')
            x[1]=x[1].replace('春季','')
            x[1]=x[1].replace('秋季','')
            x[1]=x[1].replace('暑假','')
            x[1]=x[1].replace('寒假','')
            x[1]=x[1].replace('暑期','')
            x[1]=x[1].replace('冬季','')
            if '<' in x[1] and '>' in x[1]:
                x[1]=x[1].split('</span>')[1]
        for i in range(len(result)):
                if 'http' not in result[i][-1]:
                    result[i][-1]='http://www.yingjiesheng.com/'+result[i][-1]
        for x in result:
            x.append('应届生求职网',datetime.datetime.now().strftime('%Y-%m-%d'))
        return result    
    except IndexError:
        return []
# 应届生求职网的备用函数
def getinfo_new4(url):
    a=[]
    wb_data = requests.get(url)
    url=[]
    soup = BeautifulSoup(wb_data.content, 'html.parser', from_encoding='utf-8')
    try:
        for link in soup.select('#wrap > div.clear > div.rec.recr > ul'):
                                ##wrap > div.clear > div.rec.recr > ul > li:nth-child(1)
            a.append(link)
            url.append(str(link))
        #print(len(a),len(str(a[0]).split('实习生'))>=4)
        #print(a)
        if len(str(a[0]).split('实习生'))<=4 :
            a=[]
            url=[]
            for link in soup.select('#mainNav > div.recommend.s_clear > div.box.floatr > ul:nth-child(8)'):
                a.append(link)
                url.append(str(link))
        if len(str(a[0]).split('实习生'))<=4:
            a=[]
            url=[]
            for link in soup.select('#mainNav > div.recommend.s_clear > div.box.floatr > ul:nth-child(6)'):
                a.append(link)
                url.append(str(link))
        a = str(a[0]).split('</li>\n<li>\n')
        a = flatten([x.split('li>\n<li') for x in a])
        a=[x for x in a if '.'+datetime.datetime.now().strftime('%d') in x]
           #datetime.datetime.now().strftime('%d')
        #url=[re.findall(r'href="(.*?)" target=',str(x))[0] for x in a if x!='']
        a=[[re.findall(r'#008000;">(.*?)</span>',str(x)),re.findall(r'</span>(.*?)</a>',str(x)),re.findall(r'href="(.*?)" target=',str(x))] for x in a] 
        info = [flatten(a[i]) for i in range(len(a))]
        for i in range(len(info)):
            if len(info[i])<3:
                info[i]=[]
        info = [x for x in info if x!=[]]
        for i in range(len(info)):
                if 'http' not in info[i][-1]:
                    info[i][-1]='http://www.yingjiesheng.com/'+info[i][-1]

        for x in info:
            x[1]=x[1].split("招聘")
            if len(x[1])==1:
                x[1].append('实习生')
            elif len(x[1])!=2:
                del x[1][1]
                if x[1][1]=='':
                    x[1][1]='实习生'
            elif x[1][1]=='':
                x[1][1]='实习生'
            elif len(x[1])==1:
                x[1].append('实习生')
        info = [flatten(x) for x in info if x!=[]]
        info = [x[:3]+[x[-1],'应届生',datetime.datetime.now().strftime('%Y-%m-%d')] for x in info if x!=[]]
        for x in info:
            x[1]=x[1].replace('实习生','')
            x[1]=x[1].replace('2020','')
            x[1]=x[1].replace('2021','')
            x[1]=x[1].replace('春季','')
            x[1]=x[1].replace('秋季','')
            x[1]=x[1].replace('暑假','')
            x[1]=x[1].replace('寒假','')
            x[1]=x[1].replace('暑期','')
            x[1]=x[1].replace('冬季','')
        return info
    except:
        return []
#获取实习僧信息的爬虫函数
def shuju_shixisen(page,browser,url):
    if url !='no_url':
        browser.get(url.format(page))
    if page==1:
        ttf = []
        ttf_test=[]
        pwd = browser.find_elements_by_xpath('/html/head/style[1]')
        for x in pwd:
            ttf_test=[x.get_attribute('outerHTML')]
            ttf.append(ttf_test[0].split('url(')[1].split(');}<')[0])
        url='https://www.shixiseng.com'
        urllib.request.urlretrieve(url+ttf[0], "shixi.ttf")
    elif os.path.exists('shixi.ttf'):
        pass
    #获得ttf文件并解码
    else:
        ttf = []
        ttf_test=[]
        pwd = browser.find_elements_by_xpath('/html/head/style[1]')
        for x in pwd:
            ttf_test=[x.get_attribute('outerHTML')]
            ttf.append(ttf_test[0].split('url(')[1].split(');}<')[0])
        url='https://www.shixiseng.com'
        urllib.request.urlretrieve(url+ttf[0], "shixi.ttf")
    font = TTFont('shixi.ttf')
    # 由于实习增的这个文件页面刷新前后是不变的，所以不用前后进行字体文件的比对了
    font_base_order = font.getGlyphOrder()[2:]# 下载下来的文件头两个是空的
    # 新下载的问件与原文件进行比对
    # 前10个是0到9，从本地将对应的文字写出来
    map_list =[
        *[str(i) for i in range(10)], u'一', u'师', 'X', u'会', u'四', u'计', u'财', u'场', 'D', 'H',
        'L', 'P', 'T', u'聘', u'招', u'工', 'd', u'周', 'I', u'端', 'p', u'年', 'h', 'x', u'设', u'程',
        u'二', u'五', u'天', 't', 'C', 'G', u'前', 'K', 'O', u'网', 'S', 'W', 'c', 'g', 'k', 'o', 's',
        'w', u'广', u'市', u'月', u'个', 'B', 'F', u'告', 'N', 'R', 'V', 'Z', u'作', 'b', 'f', 'j', 'n',
        'r', 'v', 'z', u'三', u'互', u'生', u'人', u'政', 'A', 'J', 'E', 'I', u'件', 'M', '行', 'Q', 'U',
        'Y', 'a', 'e', 'i', 'm', u'软', 'q', 'u', u'银', 'y', u'联', 
    ]
    # 你会发现网页中编码对应的是font.getBestCmap()的key的16进制的值
    map_dict = {value: '&#' + hex(key)[1:]
                for key, value in font.getBestCmap().items()}
    # 将固定的字体顺序和uni编码进行一一对应，并从map_dict中寻找16进制的值对应的字体
    temp_dict = {map_dict[key]: value for key, value in zip(font_base_order, map_list)}

    #地区
    dq=[]
    dq_test=[]
    pwd = browser.find_elements_by_xpath('//*[@id="__layout"]/div/div[2]/div[2]/div[1]/div[1]/div[1]/div/div[1]/div[1]/p[2]/span[1]')
    for x in pwd:
        dq_test=[x.text,x.get_attribute('href')]
        dq.append(dq_test[0])
    #公司名称
    gs=[]
    gs_test=[]
    pwd = browser.find_elements_by_xpath('//*[@id="__layout"]/div/div[2]/div[2]/div[1]/div[1]/div[1]/div/div[1]/div[2]/p[1]/a')
    for x in pwd:
        gs_test=[x.text,x.get_attribute('href')]
        gs.append(gs_test[0])
    #职位
    zw=[]
    zw_test=[]
    pwd = browser.find_elements_by_xpath('//*[@id="__layout"]/div/div[2]/div[2]/div[1]/div[1]/div[1]/div/div[1]/div[1]/p[1]/a')
    for x in pwd:
        zw_test=[x.get_attribute('outerHTML')]
        m=str(zw_test[0]).split('title="')[1].split('" target=')[0]
        m=''.join(m.split('amp;'))
        for k,value in temp_dict.items():
            m = m.replace(k,value)
        zw.append(m)
    #链接
    xq = []
    xq_test=[]
    pwd = browser.find_elements_by_xpath('//*[@id="__layout"]/div/div[2]/div[2]/div[1]/div[1]/div[1]/div/div[1]/div[1]/p[1]/a')
    for x in pwd:
        xq_test=[x.get_attribute("outerHTML")]
        xq.append(re.findall(r'href="(.*?)" title="',str(xq_test[0]))[0])
    if len(dq) != len(zw) or len(dq) != len(gs) or  len(gs) != len(zw) or len(xq) != len(zw):
        return []
    else:
        return [[dq[i],gs[i],zw[i],xq[i],'实习僧',datetime.datetime.now().strftime('%Y-%m-%d')] for i in range(len(xq))]  


if __name__ == "__main__":
#实习信息的主函数  
    path = os.path.abspath(os.curdir)
    sys.path.append(str(path))
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    browser = webdriver.Chrome(r'D:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe', options=option)
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    result_yingjiesheng=get_info_yingjiesheng()
    if result_yingjiesheng==[]:
        result_yingjiesheng=getinfo_new4(r'http://www.yingjiesheng.com')
    if result_yingjiesheng==[]:
        print('扎心了!应届生求职网的信息还没有更新......\n')
    url_quanguo = "https://www.shixiseng.com/interns?page={}&keyword=&type=intern&area=&months=&days=&degree=&official=&enterprise=IT300&salary=-0&publishTime=day&sortType=zj&city=全国&internExtend="
    url_wuhan = "https://www.shixiseng.com/interns?page=1&keyword=&type=intern&area=&months=&days=&degree=&official=&enterprise=&salary=-0&publishTime=day&sortType=zj&city=武汉&internExtend="
    result_shixisen =shuju_shixisen(1,browser,url_quanguo)
    for i in range(6):
        result_shixisen =zhenghe(result_shixisen,shuju_shixisen(i+2,browser,url_quanguo))
    #这里是武汉实习信息版块
    browser.get(url_wuhan)
    result_shixisen_wuhan =shuju_shixisen(1,browser,'no_url')
    for i in range(10):
        try:
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            button=browser.find_element_by_xpath('//*[@id="__layout"]/div/div[2]/div[2]/div[1]/div[1]/div[2]/div/ul/li[{}]'.format(i+2))
            button.click()
            time.sleep(1)
            result_shixisen_wuhan =zhenghe(result_shixisen_wuhan,shuju_shixisen(i+2,browser,'no_url'))
        except:
            break
    #信息筛选
    result_wuhan = [x for x in result_shixisen_wuhan if '武汉' in x[0]]
    result_country = result_yingjiesheng + result_shixisen
    data_country = pd.DataFrame(result_country,columns = ['base','company','job','url','source','upgrade_time'])
    data_wuhan = pd.DataFrame(result_wuhan,columns = ['base','company','job','url','source','upgrade_time'])
    print('信息抓取完毕，准备写入数据库')

#将获取到的数据插入数据库
    # 连接database
    conn = pymysql.connect(host="localhost", user="root",password="123456",database="shixi",charset="utf8")
    # 得到一个可以执行SQL语句的光标对象
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    #如果没有数据表要进行生成
    sql_create1 =" CREATE TABLE IF NOT EXISTS `shixi_country`\
        (\
       `base` VARCHAR(100) NOT NULL,\
       `company` VARCHAR(40) NOT NULL,\
       `job` VARCHAR(100) NOT NULL,\
       `url` VARCHAR(300) NOT NULL,\
       `source` VARCHAR(100) NOT NULL,\
       `upgrade_date` DATE\
        )\
        ENGINE=InnoDB DEFAULT CHARSET=utf8;"
    sql_create2 =" CREATE TABLE IF NOT EXISTS `shixi_wuhan`\
        (\
       `base` VARCHAR(100) NOT NULL,\
       `company` VARCHAR(40) NOT NULL,\
       `job` VARCHAR(100) NOT NULL,\
       `url` VARCHAR(300) NOT NULL,\
       `source` VARCHAR(100) NOT NULL,\
       `upgrade_date` DATE\
        )\
        ENGINE=InnoDB DEFAULT CHARSET=utf8;"
    cursor.execute(sql_create1)
    cursor.execute(sql_create2)
    #批量插入数据
    #首先是全国信息
    sql_country = "INSERT INTO shixi_country  VALUES (%s, %s, %s, %s, %s,%s)"
    for i in range(len(data_country)):
        a = data_country['base'][i]
        b = data_country['company'][i]
        c = data_country['job'][i]
        d = data_country['url'][i]
        e = data_country['source'][i]
        f = data_country['upgrade_time'][i]
        values = (a, b, c, d,e,f)#在从也可以进行插入数据格式修改
        cursor.execute(sql_country,values)
    #之后是武汉信息
    sql_wuhan = "INSERT INTO shixi_wuhan  VALUES (%s, %s, %s, %s, %s,%s)"
    for i in range(len(data_wuhan)):
        a = data_wuhan['base'][i]
        b = data_wuhan['company'][i]
        c = data_wuhan['job'][i]
        d = data_wuhan['url'][i]
        e = data_wuhan['source'][i]
        f = data_wuhan['upgrade_time'][i]
        values = (a, b, c, d,e,f)#在从也可以进行插入数据格式修改
        cursor.execute(sql_wuhan,values)
    #在插入完数据之后，将最近跟新的数据覆盖掉之前有的数据，也就是查找重复，如果时间越早则删除记录
    conn.commit()
    sql_delete_country=" delete from shixi_country where (url,upgrade_date) in (select url,n from(select url,min(upgrade_date)as n,count(*) as c from shixi_country group by `url` having c>1)as t)"
    sql_delete_wuhan=" delete from shixi_wuhan where (url,upgrade_date) in (select url,n from(select url,min(upgrade_date)as n,count(*) as c from shixi_wuhan group by `url` having c>1)as t)"
    cursor.execute(sql_delete_country)
    cursor.execute(sql_delete_wuhan)
    # 执行SQL语句
    conn.commit()
    # 关闭光标对象
    cursor.close()
    # 关闭数据库连接
    conn.close()
    print('信息写入完毕，开始删除重复信息')
    print('信息写入成功，更新数据接口')
    #接下来学习利用python写接口
    
    