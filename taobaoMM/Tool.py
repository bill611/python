#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

class Tool:
    # 去除img标签，1-7位空格,&nbsp;
    removeImg = re.compile('<img.*?>| {7}|&nbsp')
    # 删除超链接标签
    removeAddd = re.compile('<a.*?>|</a>')
    # 把换行的标签换为\n
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    # 把表格制表<td>替换为\t
    replaceTD = re.compile('<td>')
    # 把换行符或者双换行符替换为\n
    replaceBR = re.compile('<br><br>|<br>')
    # 将其余标签剔除
    replaceExtraTag = re.compile('<.*?>')
    # 将多行空行删除
    replaceNoneLine = re.compile('\n+')

    def replace(self,x):
        x = re.sub(self.removeImg,"",x)
        x = re.sub(self.removeAddd,"",x)
        x = re.sub(self.replaceLine,"\n",x)
        x = re.sub(self.replaceTD,"\t",x)
        x = re.sub(self.replaceBR,"\n",x)
        x = re.sub(self.replaceExtraTag,"",x)
        x = re.sub(self.replaceNoneLine,"\n",x)
        # 将前后多余内容删除
        return x.strip()
