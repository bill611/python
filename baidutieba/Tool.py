#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

class Tool:
    removeImg = re.compile('<img.*?>| {7}|')
    removeAddd = re.compile('<a.*?>|</a>')
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    replaceTD = re.compile('<td>')
    replacePara = re.compile('<p.*?>')
    replaceBR = re.compile('<br><br>|<br>')
    replaceExtraTag = re.compile('<.*?>')

    def replace(self,x):
        x = re.sub(self.removeImg,"",x)
        x = re.sub(self.removeAddd,"",x)
        x = re.sub(self.replaceLine,"\n",x)
        x = re.sub(self.replaceTD,"\t",x)
        x = re.sub(self.replacePara,"\n",x)
        x = re.sub(self.replaceBR,"\n",x)
        x = re.sub(self.replaceExtraTag,"",x)
        return x.strip()
