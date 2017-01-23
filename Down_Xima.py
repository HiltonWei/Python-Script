#coding=utf8

'''
喜马拉雅专辑下载

环境：Windows+Python27 
其他：不需其他软件


备注：不再维护 有bug请自行解决
时间：魏学士 2017.1.1
'''
import urllib2
import re
import json
import os
from pprint import pprint

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

htmlfile = u"喜马拉雅.html"
fname_url= 'mp3.txt'

#页码正则
reg_list = [re.compile(r"class=\"pagingBar_wrapper\" url=\"(.*?)\""),
                re.compile(r"<a href='(/\d+/album/\d+\?page=\d+)' data-page='\d+'")]

def analyze(trackid):
    trackurl = 'http://www.ximalaya.com/tracks/%s.json' % trackid
    htmltrack = gethtml(trackurl)
    jsonobj = json.loads(htmltrack)
    title = jsonobj['title']
    mp3url = jsonobj['play_path']
    filename = title.strip() + '.mp3'
    print filename, mp3url
    with open(fname_url, 'ab+') as mp3file:
        mp3file.write('%s|%s\n' % (filename, mp3url))
    
def getMp3url(url):
    Mp3HTML = gethtml(url)
    ids_reg = re.compile(r'sound_ids="(.+?)"')
    ids_res = ids_reg.findall(Mp3HTML)
    idslist = [j for j in ids_res[0].split(',')]
    for trackid in idslist:
        analyze(trackid)
        
def ParseBegin(Url):
    htmlBase = gethtml(Url)
    with open(htmlfile,'w') as fhtml:
        fhtml.write(htmlBase)
    
    #读保存的html文件
    #with open(htmlfile,'r') as f:
    #    htmlBase = f.read()
    pageList = []
    for reg in reg_list:
        pageList.extend(reg.findall(htmlBase))
        
    urlList = ['http://www.ximalaya.com' + x for x in pageList[:-1]]
    urlList.append(Url)
    urlList = list(set(urlList))
    for ul in urlList:
        print ul
        getMp3url(ul)
    return
    
def gethtml(url):
    response = urllib2.urlopen(url)
    html = response.read()
    with open('test.txt','w') as f:
        f.write(html)
    return html
    
#下载模块
def chunk_report(bytes_so_far, chunk_size, total_size):
   percent = float(bytes_so_far) / total_size
   percent = round(percent*100, 2)
   sys.stdout.write("Downloaded %d of %d bytes (%0.2f%%)\r" %
       (bytes_so_far, total_size, percent))
 
   if bytes_so_far >= total_size:
      sys.stdout.write('\n')
 
def chunk_read(response,tofile, chunk_size=8192, report_hook=None):
   total_size = response.info().getheader('Content-Length').strip()
   total_size = int(total_size)
   if checkFileSize(total_size,tofile):
       print tofile + "    succ"
       return 999
   bytes_so_far = 0
   outfile = open(tofile,'wb')
 
   while 1:
      chunk = response.read(chunk_size)
      bytes_so_far += len(chunk)
 
      if not chunk:
         break
      outfile.write(chunk)
 
      if report_hook:
         report_hook(bytes_so_far, chunk_size, total_size)
         
   outfile.close()
   return bytes_so_far

def down_file(url,tofile):
    reponse = urllib2.urlopen(url)
    chunk_read(reponse,tofile,report_hook=chunk_report)

def checkFileSize(size,filepath):
    if os.path.isfile(filepath):
        fsize = os.path.getsize(filepath)
        fsize = int(fsize)
        return size == fsize
    return False

def mkdirs(path):
    try:
        os.makedirs(path)
    except Exception:
        return False
    return True
    
def chdir(path):
    try:
        os.chdir(path)
    except Exception as e:
        print e
        mkdirs(path)
        os.chdir(path)
    return
#下载模块结束

#从mp3.txt中读入 (文件名|url) 
#然后下载到mp3文件夹中
def BeginDown():
    dataStr = []
    with open(fname_url,'r') as f:
        dataStr = f.readlines()
    
    chdir(u'mp3音乐')#下载路径
    setfile = open('setfile.txt','w')
    dataStr = list(set(dataStr))
    for line in range(len(dataStr)):
        fileInfo = dataStr[line].split('|')
        if len(fileInfo) != 2:
            continue
        print line,fileInfo[0].encode('gb18030'),fileInfo[1]
        down_file(fileInfo[1],fileInfo[0].encode('gb18030'))#开始下载
        setfile.write(str(line)+fileInfo[0].encode('gb18030')+fileInfo[1])
    setfile.close()
    chdir("../.")
    
    
if __name__ == '__main__':
    #解析放到mp3.txt文件中
    url = "http://www.ximalaya.com/26358409/album/4480584"
    ParseBegin(url)
    
    #从mp3.txt中读入 (文件名|url) 
    #然后下载到mp3文件夹中
    BeginDown()
    print u"\n-----下载完成------\n"
    
