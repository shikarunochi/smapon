from m5stack import *
import random
import urequests
import ujson
import json
from jpfontSmapon import jpfontSmapon
import uos
import gc
import time
import YahooHeadline

class smaponHeadline:
    
    def __init__(self):
        lcd.clear()

        uos.mountsd()
        self.jpfontSmaponObj = jpfontSmapon()
        random.seed(int(time.time()))

        #Yahooヘッドライン取得（XML）
        self.maxCategoty = YahooHeadline.getCategoryCount()
        self.nowCategory = 4
        self.titleTextList = YahooHeadline.getYahooHeadline(self.nowCategory)
        self.nowTitleIndex = 0
        
        lcd.setCursor(0, 0)
        lcd.setColor(lcd.BLACK)
        self.nextNews()

        self.autoNewsCount = 0
        self.autoNews()
    
    def printNews(self, newsTitle): 
        self.jpfontSmaponObj.printString(newsTitle)
        gc.collect()    

    def nextNews(self):
        self.autoNewsCount = 0
        lastNewsFlag = False
        if len(self.titleTextList) ==0 :
            return
        self.printNews(self.titleTextList[self.nowTitleIndex])
        self.nowTitleIndex = self.nowTitleIndex + 1
        if self.nowTitleIndex >= len(self.titleTextList):
            self.nowTitleIndex = 0
            lastNewsFlag = True
        return lastNewsFlag
        
    def prevCategory(self):
        lcd.image(0, 0, random.choice(self.sakuraList))
        self.autoNewsCount = 0
        self.nowCategory = self.nowCategory - 1
        if self.nowCategory < 0:
            self.nowCategory = self.maxCategoty - 1           
        self.titleTextList = YahooHeadline.getYahooHeadline(self.nowCategory)
        self.nowTitleIndex = 0
        self.nextNews()
    
    def nextCategory(self):
        self.autoNewsCount = 0
        self.nowCategory = self.nowCategory + 1
        if self.nowCategory >= self.maxCategoty:
            self.nowCategory = 0
        self.titleTextList = YahooHeadline.getYahooHeadline(self.nowCategory)
        self.nowTitleIndex = 0
        self.nextNews()

    def autoNews(self):
        lastNewsFlag = False
        while True:
            self.autoNewsCount = self.autoNewsCount + 1
            if self.autoNewsCount > 5:
                if lastNewsFlag == True:
                    self.nextCategory()
                    lastNewsFlag = False
                else:
                    lastNewsFlag = self.nextNews()
