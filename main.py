# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup as bs
import  requests
from selenium import webdriver
import time
# #此项目为爬取酷狗排行榜并批量下载的python项目
def down(url):
    option = webdriver.ChromeOptions()
    option.add_argument("headless")
    browser = webdriver.Chrome('E:\python\Scripts\chromedriver.exe', chrome_options=option)
    browser.get(url)#仍以阿衣莫为例
    response=browser.page_source
    audiutl=browser.find_element_by_id('myAudio')
    time.sleep(2)
    print('*****************'+audiutl.get_property('src'))
    return audiutl.get_property('src')

    #browser.close()#关闭浏览器其他应用
#*****************************************************************************************************************************************
#此方法为爬取歌曲信息：
song_list_info=[]#存放全部歌曲列表
song_download_url=[]#经过筛选处理后得到的真正的歌曲下载链接
headers={
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36'
}#公用请求头
def SongInformation(page):
    urls='https://www.kugou.com/yy/rank/home/'+page+'-8888.html'

    re=requests.get(url=urls,headers=headers)
    #save=re.content.decode('utf-8')
    save=re.text
    if save!=None:
        soup=bs(save,'html.parser')
        rank=soup.select('span.pc_temp_num')#歌曲排名
        musichref=soup.select('div.pc_temp_songlist>ul>li>a')
        mhref=[]#歌曲链接
        list=[]# 歌曲信息综合
        singer = []#歌手名字
        songname = []#歌曲名字
        for i in musichref:
            mhref.append(i['href'])#添加歌曲链接
            list.append(i['title'].split(' - ',2))#添加歌曲作者以及歌曲名字
        for i in list:
            songname.append(i[1])
            singer.append(i[0])
        for i,j,k in zip(mhref,songname,singer):
            song_infor = {
                'url':i,
                'name':j,
                'singer':k
            }
            song_list_info.append(song_infor)
    else:
        pass
#*****************************************************************************************************************************************
def KuGouDownload(startpage,endpage):
    for i in range(startpage,endpage):
        try:
            print('正在存储第'+str(i+1)+'页歌曲信息')
            SongInformation(str(i+1))
            print('第'+str(i+1)+'页歌曲信息存储成功')
            time.sleep(1)
        except:
            print('第'+str(i+1)+'页歌曲信息存储失败，已跳过当前页')
    for i in song_list_info:
        print(i['name'] + '下载地址:')
        z=down(i['url'])
        #print('************'+z)
        #z=song_download_url.append(down(i['url']))
        with open("D:\KugouSpider\下载音乐\{}.mp3".format(i["name"]), 'wb') as f:
            mp3 = requests.get(z, headers=headers).content
            f.write(mp3)
            print('歌曲已下载完毕')
#********************************************************************************************************************************************
def main():
    try:
        a=input('请输入下载开始页数(默认为从第一页开始下载):')
        if a==''or a=='1':
            a=0
        else:
            a=int(a)
        b=input('请输入下载结束页数(最大为23):')
        b=int(b)
        #if b>23
        print("您想要下载第"+str(a)+'至第'+str(b)+'页')
        print('即将开始下载，请勿关机或者停止程序！')
        KuGouDownload(a,b)
        print('音乐已下载完毕，祝君开心。')
    except:
        print('您输入的信息有误，请重新运行此程序。')
if __name__ == '__main__':
    main()