
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup as bs
import  requests
from selenium import webdriver
import time
song_list_info=[]#存放全部歌曲列表
song_download_url=[]#经过筛选处理后得到的真正的歌曲下载链接
headers={
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36'
}#公用请求头


def SongInformation(page):
    urls='https://www.kugou.com/yy/rank/home/'+page+'-8888.html'
    re=requests.get(url=urls,headers=headers)
    #
    # print(re.encoding)
    # try:
    #     print(re.text.encode(""))

    #save=re.content.decode('utf-8')
    # except:
    #     print("decod is faild!")
    save=re.text
    print(save)
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
            for i in song_list_info:
                print(i)
    else:
        print('!!!!!')


SongInformation(str(10))
