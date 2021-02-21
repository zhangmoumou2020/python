#coding = utf-8
import bs4 #网页解析
from bs4 import BeautifulSoup
import re   #正则匹配
import urllib.request #获取网页数据
import xlwt #进行excel操作
# import sqlite3 #进行sql数据库操作
import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
def main():
    baseurl = "https://movie.douban.com/top250?start="
    #1.爬取网页
    datalist = getData(baseurl)
    savepath = "豆瓣电影TOP250.xls"
    #2 解析数据
    # 3.保存数据
    saveData(datalist,savepath)
    # askURL("https://movie.douban.com/top250?start=")

findLink = re.compile(r'<a href="(.*?)">')   #创建正则表达式对象，表示规则（字符串的模式） 
findimgSrc = re.compile(r'<img .*src="(.*?)"',re.S) #re.S让换行符出现在字符中   
findTitle = re.compile(r'<span class="title">(.*)</span>')
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
findJudge = re.compile(r'<span>(\d*)人评价</span>')
findInq = re.compile(r'<span class="inq">(.*)</span>')
findBd = re.compile(r'<p class="">(.*?)</p>',re.S)
def getData(baseurl):
    datalist = []
    for i in range(0,10):  #调用获取页面信息的函数10次
        url = baseurl + str(i*25)
        html=askURL(url)  #保存获取到的网页源码
        #2.逐一解析数据
        soup = BeautifulSoup(html,"html.parser")
        for item in soup.findAll('div',class_='item'): #查找符合要求的字符串，形成列表
            # print(item)
            data = [] #保存一部电影的所有信息
            item = str(item)
            link = re.findall(findLink,item)[0] #re库通过正则表达式查找指定的字符串
            data.append(link)
            imgSrc = re.findall(findimgSrc,item)[0]
            data.append(imgSrc)
            titles = re.findall(findTitle,item)
            if(len(titles)==2):
                ctitle = titles[0]
                data.append(ctitle)
                otitle = titles[1].replace("/","") #去掉无关符号
                data.append(otitle)
            else:
                data.append(titles[0]) 
                data.append('') #留空
            rating = re.findall(findRating,item)[0]
            data.append(rating)
            judgeNum = re.findall(findJudge,item)[0]
            data.append(judgeNum)
            inq = re.findall(findInq,item)
            if len(inq) != 0:
                inq = inq[0].replace("。","")
                data.append(inq)
            else:
                data.append("")
            bd = re.findall(findBd,item)[0]
            bd = re.sub('<br(\s+)?/>(\s+)?'," ",bd)
            bd = re.sub('/'," ",bd)
            data.append(bd.strip())   #去掉前后的空格
            
            datalist.append(data)
    # print(datalist)
    return datalist
# 得到指定一个URL的网页内容
def askURL(url):
    # 模拟浏览器头部信息，向豆瓣服务器发送消息
    head = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0"
    }
    # 用户代理告诉豆瓣服务器是什么类型浏览器
    request = urllib.request.Request(url,headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        # print(html)
    except  urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)
    return html
# 保存数据
def saveData(datalist,savepath):
    print("...save...")
    book = xlwt.Workbook(encoding="utf-8",style_compression=0)
    sheet = book.add_sheet("豆瓣电影250",cell_overwrite_ok=True)
    col = ("电影详情链接","图片链接","影片中文名","影片外国名","评分","评价数","概况","相关信息")
    for i in range(0,8):
        sheet.write(0,i,col[i]) #列名
    for i in range(0,250):
        print("第%d条"%(i+1))
        data = datalist[i]
        for j in range(0,8):
            sheet.write(i+1,j,data[j])    
        
    book.save(savepath)

if __name__=="__main__": #当程序执行时
#调用函数,整个程序的入口，如果下面有函数，其他地方不会有函数
    main()
    print("爬取完毕")