# -*- coding: UTF-8 -*-

#扑克牌类
class Poker():
    #aDecor:C(Club)=♣,D(Diamond)=♦,S(Spade)=♠,H(Heart)=♥,J(Joker)=Joker
    #aNumber:当aDecor=Joker，aNumber=1时为大王，aNumber=0时为小王，其余时候aNumber可以为A2345678910JQK
    def __init__(self,aDecor,aNumber):
        assert aDecor in ('C','D','S','H','J'),pokerValueInputError  #断言限制卡面输入
        assert aNumber in ("A","2","3","4","5","6","7","8","9","10","J","Q","K","0","1"),pokerValueInputError #断言限制卡面输入
        tValueDict={"A":1,"2":2,"3":3,"4":4,"5":5,"6":6,"7":7,"8":8,"9":9,"10":10,"J":10,"Q":15,"K":20}
        tDecorDict={"C":"♣","D":"♦","S":"♠","H":"♥"}
        #CardValue卡分值，用于游戏中的分值计算
        if aDecor == 'J':
            self.CardValue=0
        else:
            self.CardValue=tValueDict[aNumber]
        self.DecorType=aDecor   #卡花色，用于游戏中的花色判断
        self.CardNumber=aNumber #卡面值，用于游戏中的面值判断
        #CardName卡名，根据卡名对应的资源获取图像
        if aDecor == 'J':
            if aNumber == '0':
                self.CardName='LittleJOKER'
            else:
                self.CardName='BigJOKER'
        else:
            self.CardName=tDecorDict[aDecor]+aNumber
        self.CardStatus=0  #卡牌状态，当卡牌状态为0时显示卡背，卡牌状态为1时显示卡面
        self.Position=''    #卡牌位置
        self.Name=self.DecorType+self.CardNumber    #卡牌基础名
        self.Selected=False     #是否被选择
    
    def getName(self):
        #获取卡牌基础名
        return self.Name
        
    def getCardName(self):
        #获取卡牌花名
        return self.CardName
    
    def getCardDecor(self):
        #获取卡牌花色
        return self.DecorType
    
    def getCardNumber(self):
        #获取卡牌点数
        return self.CardNumber
    
    def getCardValue(self):
        #获取卡牌分值
        return self.CardValue    
    
    def setPosition(self,value):
        #设置卡牌位置
        self.Position=value
        
    def getPosition(self):
        #获取卡牌位置
        return self.Position
        
    def setStatus(self,aStatus):
        #设置卡牌状态 0：背面 1：正面
        self.CardStatus=aStatus
        
    def getStatus(self):
        #获取卡牌状态 0：背面 1：正面
        return self.CardStatus
    
    def turnOver(self):
        #翻转卡牌
        if self.getStatus()==1:
            self.setStatus(0)
            return 0
        elif self.getStatus()==0:
            self.setStatus(1)
            return 1

class pokerValueInputError(Exception):
    #卡面输入错误异常
    pass

class posValueError(Exception):
    #位置值错误
    #不在eb(enemybox) , cp(cardpub) , ct(cemetery) , hc(handcard) , jp(jokerpos) , ep(enemypos) , mo(moveout) , tp(tablepos)中
    pass

class handPosValueError(Exception):
    #手牌位置值错误
    #选择手牌数大于当前手牌总数
    pass

class totalHandValueError(Exception):
    #当前总手牌数值错误
    pass