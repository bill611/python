#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import urllib
import urllib2
import cookielib

class QSBK:
    def __init__(self):
        self.pageIndex = 1
        self.user_agent = 'Mozilla/4.0 (compatibel; MSIE 5.5; Windows NT)'
        self.headers = {'User-Agent':self.user_agent}
        self.stories = []
        self.match_rule = '<div.*?author.*?<img.*?=".*?".*?"(.*?)".*?="content">.*?span>(.*?)</span>'+\
             '.*?"number">(.*?)<.*?"likenum">'+\
             '.*?/div>'
        self.enable = False

    def getPage(self,pageIndex):
        try:
            url = 'http://www.qiushibaike.com/8hr/page/' + str(pageIndex)+ '/?s=4984541'
            request = urllib2.Request(url,headers = self.headers)
            respons = urllib2.urlopen(request)
            pageCode = respons.read().decode('utf-8')
            return pageCode
        except urllib2.URLError,e:
            if hasattr(e,"reason"):
                print u"连接糗事百科失败，错误原因",e.reason
                return None

    def getPageItems(self,pageIndex):
        pageCode = self.getPage(pageIndex)
        if not pageCode:
            print u"页面加载失败..."
            return None
        else:
            print u"加载成功,正在解析"
        pattern = re.compile(self.match_rule,re.S)
        items = re.findall(pattern,pageCode)
        print u"解析成功"
        pageStories = []
        for item in items:
            pageStories.append([item[0] + '\n' + item[1] + '\n' + item[2] + '\n'])
            print item[0] + '\n' + item[1] + '\n' + item[2] + '\n'
        return pageStories

    def loadPage(self):
        if self.enable == False:
            return
        if len(self.stories) < 2:
            pageStories = self.getPageItems(self.pageIndex)
            if pageStories:
                self.stories.append(pageStories)
                self.pageIndex += 1

    def getOneStory(self,pageStories,page):
        for story in pageStories:
            input = raw_input()
            if input == "Q":
                self.enable = False
                return
            self.loadPage()
            print story[0]

    def start(self):
        print "正在读取糗事百科，回车查看新段子，Q退出"
        self.enable = True
        self.loadPage()
        nowPage = 0
        while self.enable:
            if len(self.stories) > 0:
                pageStories = self.stories[0]
                nowPage += 1
                del self.stories[0]
                self.getOneStory(pageStories,nowPage)

spider = QSBK()
spider.start()
