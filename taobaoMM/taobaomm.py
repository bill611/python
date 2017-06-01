#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import urllib2
import Tool
import re
import os

class Spider:
    def __init__(self):
        self.siteUrl = 'http://mm.taobao.com/json/request_top_list.htm'
        self.tool = Tool.Tool()

    def getPage(self,pageIndex):
        try:
            url = self.siteUrl +  '?page=' + str(pageIndex)
            user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
            request = urllib2.Request(url)
            request.add_header('User-Agent',user_agent)
            response = urllib2.urlopen(request)
            #  print response.read()
            return response.read().decode('gbk')
        except urllib2.URLError,e:
            if hasattr(e,"reason"):
                print u"淘宝MM链接失败，错误原因",e.reason
                return None

    def getContents(self,pageIndex):
        """获取索引界面所有MM的信息，list格式"""
        page = self.getPage(pageIndex)
        pattern = re.compile('<div class="list-item".*?pic-word.*?<a href="(.*?)".*?<img src="(.*?)".*?<a class="lady-name.*?>(.*?)</a>.*?<strong>(.*?)</strong>.*?<span>(.*?)</span>',re.S)
        items = re.findall(pattern,page)
        contents = []
        for item in items:
            contents.append([item[0],item[1],item[2],item[3],item[4]])
        return contents

    def getDetailPage(self,infoURL):
        """获取MM个人详情页面"""
        response = urllib.urlopen(infoURL)
        return response.read().decode('gbk')

    def getBrief(self,page):
        """获取个人文字简介"""
        pattern = re.compile('<div class="mm-aixiu-content".*?>(.*?)<!--',re.S)
        result = re.search(pattern,page)
        if result:
            return self.tool.replace(result.group(1))
        else:
            return None

    def getAllImg(self,page):
        """获取页面所有图片"""
        pattern = re.compile('<div class="mm-aixiu-content".*?>(.*?)<!--',re.S)
        content = re.search(pattern,page)
        patternImg = re.compile('<img.*?src="(.*?)"',re.S)
        if (content):
            images = re.findall(patternImg,content.group(1))
            return images
        else:
            return None

    def saveImgs(self,images,name):
        """保存多张写真图片"""
        number = 1
        print u"发现",name,u"共有",len(images),u"张照片"
        for imageURL in images:
            splitPath = imageURL.split('.')
            fTail = splitPath.pop()
            if len(fTail) > 3:
                fTail = "jpg"
            fileName = name + "/" + str(number) + "." + fTail
            self.saveImg(imageURL,fileName)
            number += 1

    def saveIcon(self,iconURL,name):
        """保存头像"""
        splitPath = iconURL.split('.')
        fTail = splitPath.pop()
        fileName = name + "/icon." + fTail
        self.saveImg(iconURL,fileName)

    def saveBrief(self,content,name):
        """保存个人简介"""
        fileName = name + "/" + name + ".txt"
        f = open(fileName,"w+")
        print u"正在偷偷保存她的个人信息为",fileName
        if content:
            f.write(content.encode('utf-8'))

    def saveImg(self,imageURL,fileName):
        """传入图片地址，文件名，保存单张图片"""
        u = urllib.urlopen(imageURL)
        data = u.read()
        f = open(fileName,'wb')
        f.write(data)
        print u"正在瞧瞧保存她的一张图片为",fileName
        f.close()

    def mkdir(self,path):
        """创建新目录"""
        path = path.strip()
        isExists = os.path.exists(path)
        if not isExists:
            print u"偷偷新建了名字叫做",path,u"的文件夹"
            os.mkdir(path)
            return True
        else:
            print u"名为",path,u"的文件夹已经创建成功"
            return False

    def savePageInfo(self,pageIndex):
        """获取第一页淘宝MM列表"""
        contents = self.getContents(pageIndex)
        for item in contents:
            # item[0]个人详情URL,item[1]头像URL,item[2]姓名,item[3]年龄,item[4]居住地
            print u"发现一位模特，名字叫",item[2],u"芳龄",item[3],u"她在",item[4]
            print u"正在偷偷地保存",item[2],u"的信息"
            print u"又意外地发现她的个人地址是","https:"+item[0]
            detaiURL = "https:" + item[0]
            detailPage = self.getDetailPage(detaiURL)
            brief = self.getBrief(detailPage)
            images = self.getAllImg(detailPage)
            self.mkdir(item[2])
            self.saveBrief(brief,item[2])
            self.saveIcon(item[1],item[2])
            self.saveImgs(images,item[2])

    def savePagesInfo(self,start,end):
        """输入起止页码，获取MM图片"""
        for i in range(start,end+1):
            print u"正在偷偷寻找第",i,u"个地方，看看MM们在不在"
            self.savePageInfo(i)

spider = Spider()
spider.savePagesInfo(1,10)

