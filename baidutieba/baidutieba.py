#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import urllib
import urllib2
import Tool

class BDTB:
    def __init__(self,baseUrl,seeLZ,floorTag):
        self.baseUrl = baseUrl
        self.seeLZ = '?see_lz=' + str(seeLZ)
        self.tool = Tool.Tool()
        self.file = None
        self.floor = 1
        self.defautlTitle = u"百度贴吧"
        self.floorTag = floorTag

    def getPage(self,pageNum):
        try:
            url = self.baseUrl + self.seeLZ + '&pn=' + str(pageNum)
            response = urllib2.urlopen(urllib2.Request(url))
            #  print response.read()
            return response.read().decode('utf-8')
        except urllib2.URLError,e:
            if hasattr(e,"reason"):
                print u"连接百度贴吧失败，错误原因",e.reason
                return None

    def getTitle(self,page):
        pattern = re.compile('<h3 class="core_title_txt.*?>(.*?)</h3>',re.S)
        result = re.search(pattern,page)
        if result:
            print result.group(1)
            return result.group(1).strip()
        else:
            return None

    def getPageNum(self,page):
        pattern = re.compile('<li class="l_reply_num.*?<span.*?<span.*?>(.*?)</span>',re.S)
        result = re.search(pattern,page)
        if result:
            return result.group(1).strip()
        else:
            return None

    def getContent(self,page):
        pattern = re.compile('<div id="post_content_.*?>(.*?)</div>',re.S)
        items = re.findall(pattern,page)
        contents = []
        for item in items:
            content = "\n" + self.tool.replace(item) + "\n"
            contents.append(content.encode('utf-8'))
        return contents

    def setFileTitle(self,title):
        if title is not None:
            self.file = open(title + ".txt","w")
        else:
            self.file = open(self.defautlTitle + ".txt","w")

    def writeData(self,contents):
        """docstring for writeData"""
        for item in contents:
            if self.floorTag == '1':
                floorLine = "\n" + str(self.floor) + u"-------------------------------------------\n"
                self.file.write(floorLine)
            self.file.write(item)
            self.floor += 1
        
    def start(self):
        """docstring for start"""
        indexPage = self.getPage(1)
        pageNum = self.getPageNum(indexPage)
        title = self.getTitle(indexPage)
        self.setFileTitle(title)
        if pageNum == None:
            print "URL已经失效，请重试"
            return
        try:
            print "该帖子共有" + str(pageNum) + "页"
            for i in range(1,int(pageNum)+1):
                print "正在写入第" + str(i) + "页数据"
                page = self.getPage(i)
                contents = self.getContent(page)
                self.writeData(contents)
        except IOError,e:
            print "write err,reason:" + e.message
        else:
            print "write finished!"
        finally:
            self.file.close()

print "请输入帖子代号"
baseUrl = 'http://tieba.baidu.com/p/' + str(raw_input(u'http://tieba.baidu.com/p/'))
seeLZ = raw_input("是否只取楼主发言，是输入1，否输入0\n")
floorTag = raw_input("是否写入楼层信息，是输入1，否输入0\n")
bdtb = BDTB(baseUrl,seeLZ,floorTag)
bdtb.start()
