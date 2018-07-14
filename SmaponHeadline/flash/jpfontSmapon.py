from m5stack import lcd
from time import sleep

class jpfontSmapon:
    
    def makeSmaponDataList(self,dataList):
        return [
        dataList[16],dataList[17],dataList[0],dataList[1],dataList[6],dataList[7],dataList[22],dataList[23],
        dataList[24],dataList[25],dataList[8],dataList[9],dataList[14],dataList[15],dataList[30],dataList[31],
        dataList[18],dataList[19],dataList[2],dataList[3],dataList[4],dataList[5],dataList[20],dataList[21],
        dataList[26],dataList[27],dataList[10],dataList[11],dataList[12],dataList[13],dataList[28],dataList[29],
        dataList[34],dataList[35],dataList[50],dataList[51],dataList[52],dataList[53],dataList[36],dataList[37],
        dataList[42],dataList[43],dataList[58],dataList[59],dataList[60],dataList[61],dataList[44],dataList[45],
        dataList[32],dataList[33],dataList[48],dataList[49],dataList[54],dataList[55],dataList[38],dataList[39],
        dataList[40],dataList[41],dataList[56],dataList[57],dataList[62],dataList[63],dataList[46],dataList[47]
        ]  
    

    def __init__(self):
        initDataList = [
        1,1,1,1,1,1,1,1,
        1,0,0,0,0,0,0,1,
        1,0,0,0,0,0,0,1,
        1,0,0,0,0,0,0,1,
        1,0,0,0,0,0,0,1,
        1,0,0,0,0,0,0,1,
        1,0,0,0,0,0,0,1,
        1,1,1,1,1,1,1,1
        ]    
        self.fontFile = open("/sd/misakiFontData8x8.bin", "rb")
        self.fontCodeFile = open("/sd/misakiFontCode8x8.bin", "rb")#Unicodeコード→フォント並び順変換
        self.zenkaku="ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ！＃＄％＆’（）＊＋，－．／：；＜＝＞？＠［￥］＾＿‘｛｜｝～　０１２３４５６７８９"
        self.hankaku="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!#$%&'()*+,-./:;<=>?@[\]^_`{|}~ 0123456789"
        self.prevDataList = initDataList[:]
        smaponDataList = self.makeSmaponDataList(initDataList)
        for y in range(8):
            for x in range(8):
                if smaponDataList[x + y * 8] == 1:
                    lcd.rect(68 + x * 23,28 + y * 23,15,15,lcd.WHITE,lcd.WHITE)
                else:
                    lcd.rect(68 + x * 23,28 + y * 23,15,15,lcd.BLACK,lcd.BLACK)
        sleep(10)
 
    def __del__(self):
        self.fontfile.close()
        self.fontCodeFile.close()

    def printChar(self, char):
        if self.hankaku.find(char) != -1:
            char=self.zenkaku[self.hankaku.find(char)]

        fontData = None
        if ord(char) < 65536:
            #フォントの位置取得
            self.fontCodeFile.seek((ord(char)-1) * 2)
            fontIndex = int.from_bytes(self.fontCodeFile.read(2), "big")
            #フォントデータ取得
            self.fontFile.seek(fontIndex * 8)
            fontData = self.fontFile.read(8)

        if fontData is not None:
            fontDataList = []
            y = 0
            index = 0
            for fontDataByte in fontData:
                for x in range(8):
                    if fontDataByte >> (7 - x) & 1 == 1: #ビット上側から、1か0かチェック
                        fontDataList.append(1)
                    else:
                        fontDataList.append(0)
        
            
    
            for offset in range(8):
                smaponDataList = self.makeSmaponDataList(self.prevDataList);
                for y in range(8):
                    for x in range(8):
                        if smaponDataList[x + y * 8] == 1:
                            lcd.rect(68 + x * 23,28 + y * 23,15,15,lcd.WHITE,lcd.WHITE)
                        else:
                            lcd.rect(68 + x * 23,28 + y * 23,15,15,lcd.BLACK,lcd.BLACK)
                            
                #prevListを左にずらし、右から新しい内容をセット
                for y in range(8):
                    for x in range(8):
                        if x != 7:
                            self.prevDataList[x + y * 8] = self.prevDataList[x +1 + y * 8]
                        else:
                            self.prevDataList[x + y * 8] = fontDataList[offset + y * 8]
                sleep(0.05)

    def printString(self, string):
        for c in string:
            self.printChar(c) #1文字ずつ描画呼び出し

