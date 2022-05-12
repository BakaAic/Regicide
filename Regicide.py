# -*- coding: UTF-8 -*-

import pygame
from pygame.locals import *
from sys import exit
from time import sleep
import time
import os

from sqlalchemy import null
from RegicideBase import *
import random

base_path=os.getcwd()+'\\'


#FPSClock.tick(FPS)  #根据时钟设置的帧率进行阻塞
#pygame.time.wait() #等待时间

class GameDisplayer():
    def __init__(self,aFPS=120,aResolution=(1920,1080),aMode=pygame.NOFRAME):  #默认分辨率1920x1080，无边框  48帧，1拍6 
        self.FPS=aFPS
        self.FPSClock=pygame.time.Clock() #设置时钟
        pygame.init()
        pygame.display.set_caption("Regicide") #标题
        self.screen=pygame.display.set_mode(aResolution,aMode) #设置窗口
        self.Enemy=None   #敌人设置初始化
    def GameStart(self):
        #启动游戏
        #游戏阶段分为 启动画面、游戏主标题、进入游戏动画、游戏维持动画、出牌阶段刷新显示、游戏失败画面、游戏胜利画面
        # self.StartMovie()       #启动画面
        # self.TitleStage()       #标题界面
        # self.GameEnterMovie()   #进入游戏动画
        self.GameMain()         #游戏主界面
    def StartMovie(self):
        #启动画面阶段  
        #调用字体
        t_font = pygame.font.Font(base_path+'fonts\\JOKERMAN.TTF',80)
        t_font2 =  pygame.font.Font(base_path+'fonts\\msyhbd.ttc',50)
        
        t_text = t_font.render("Aikko",True,(255,255,255)) #文本内容
        t_textRect=t_text.get_rect() #获取文本区域
        t_textRect.center = (960,590) #设置文本显示位置
        
        t_text2 = t_font2.render("开发者",True,(255,255,255)) #文本内容
        t_textRect2=t_text2.get_rect() #获取文本区域
        t_textRect2.center = (960,490) #设置文本显示位置
        
        self.screen.fill((0,0,0)) #填充默认背景
        pygame.display.update()
        pygame.time.wait(800)
        self.screen.blit(t_text,t_textRect) #显示文本
        self.screen.blit(t_text2,t_textRect2) #显示文本
        pygame.display.update()
        pygame.time.wait(3000)
        self.screen.fill((0,0,0)) #填充默认背景，覆盖显示内容
        pygame.display.update()
        pygame.time.wait(800)
        
    def TitleStage(self):
        #游戏标题界面阶段
        
        #背景
        titlebackground=pygame.image.load(base_path+'resource\\title\\titlebackground.jpg')
        titlebackground=pygame.transform.scale(titlebackground,(1920,1080))

        #图标
        gameicon=pygame.image.load(base_path+'resource\\title\\gameicon.png')
        gameicon=pygame.transform.scale(gameicon,(450,420))
        
        #开始按钮
        startButton=pygame.image.load(base_path+'resource\\title\\StartButton.png').convert_alpha()
        startButton=pygame.transform.scale(startButton,(350,100))
        startButton_MOUSEMOTION=pygame.transform.scale(startButton,(420,120))
        
        #退出按钮
        exitButton=pygame.image.load(base_path+'resource\\title\\ExitButton.png').convert_alpha()
        exitButton=pygame.transform.scale(exitButton,(350,100))
        exitButton_MOUSEMOTION=pygame.transform.scale(exitButton,(420,120))
        
        t_font =  pygame.font.Font(base_path+'fonts\\msyhbd.ttc',14)
        t_text = t_font.render("version 1.0.0",True,(98,98,98)) #文本内容
        t_textRect=t_text.get_rect() #获取文本区域
        t_textRect.center = (1850,1060) #设置文本显示位置
        
        mouse_on_start=0 #鼠标在开始按钮上
        mouse_on_exit=0  #鼠标在退出按钮上
        continue_flag=0  #开始游戏状态
        while True:
            self.screen.fill((0,0,0))
            self.screen.blit(titlebackground,(0,0)) #显示背景
            self.screen.blit(gameicon,((1920-450)/2,50))
            self.screen.blit(t_text,t_textRect) #显示文本 版本号
            for event in pygame.event.get():
                if event.type==QUIT:
                    exit()
                if event.type==MOUSEMOTION:
                    #判断鼠标所处区域判定是否在按钮上
                    if event.pos[0]>770 and event.pos[0]<1120 and event.pos[1]>550 and event.pos[1]<650:
                        mouse_on_start=1
                    else:
                        mouse_on_start=0
                    if event.pos[0]>770 and event.pos[0]<1120 and event.pos[1]>710 and event.pos[1]<810:
                        mouse_on_exit=1
                    else:
                        mouse_on_exit=0
                if event.type==MOUSEBUTTONDOWN:
                    #判断鼠标按下事件
                    if mouse_on_start==1:
                        continue_flag=1
                        break
                    if mouse_on_exit==1:
                        exit()
            if mouse_on_start==0:
                self.screen.blit(startButton,(770,550)) #显示开始按钮
            else:
                self.screen.blit(startButton_MOUSEMOTION,(740,540)) #显示开始按钮
            if mouse_on_exit==0:
                self.screen.blit(exitButton,(770,710)) #显示开始按钮
            else:
                self.screen.blit(exitButton_MOUSEMOTION,(740,700)) #显示开始按钮
            pygame.display.update()
            if continue_flag:
                break
            
    def GameEnterMovie(self):
        #进入游戏动画阶段
        print('Done')
    
    def GameMain(self):
        #游戏画面维持阶段
        self.Game=RuleClass(self)  #载入游戏规则
        self.Game.init()       #游戏初始化
        self.Table=self.TableClass(self) #建立卡桌对象
        self.Table.initLoad()           #桌面显示对象预设
        self._card=self.Game.cardObj   #卡牌对象映射
        self.Game.BossGet()     #获取最新Boss资源
        
        #游戏背景
        gamebackground=pygame.image.load(base_path+'resource\\table\\gamebackground.png')
        gamebackground=pygame.transform.scale(gamebackground,(1920,1080))
        
        #BOSS
        self.Enemy=self.EnemyClass(self,self.Game.getCurBossName())         #获取敌人显示
        
        #扩充帧数
        self.ExpansionFrame=1   #一拍四扩充帧
        self.Expansion=self.ExpansionFrame
        
        #日志初始化显示
        self.Table.log('====欢迎进入游戏====')
        self.Table.log('-----请出牌-----')
        
        while True:
            self.FPSClock.tick(self.FPS)  #根据时钟设置的帧率进行阻塞
            self.screen.fill((0,0,0))
            self.screen.blit(gamebackground,(0,0)) #显示游戏背景                    
            
            self.activeWatch()      #增加动作监测
            
            self.Game.Run()         #游戏流程进行
            
            # if self.Expansion==0:
            if self.Enemy.CurState==1:
                self.Enemy.Hurt_next()
            elif self.Enemy.CurState==2:
                self.Enemy.ATK_next()
            elif self.Enemy.CurState==3:
                self.Enemy.Recruit_next()
            elif self.Enemy.CurState==4:
                self.Enemy.Death_next()
            self.Expansion=self.ExpansionFrame
            # else:
            #     self.Expansion-=1
            
            self.Table.ShowTable()   #创建桌面信息
            
            pygame.display.update()
            
    def restartGameFun(self):
        self.Game.init()       #游戏初始化
        self.Table=self.TableClass(self) #建立卡桌对象    
        self.Table.initLoad()           #桌面显示对象预设
        self._card=self.Game.cardObj   #卡牌对象映射
        self.Game.BossGet()     #获取最新Boss资源
        self.Enemy=self.EnemyClass(self,self.Game.getCurBossName())         #获取敌人显示
        #日志初始化显示
        self.Table.log('====重新开始游戏====')
        self.Table.log('-----新的回合-----')
    
    def getTips(self):
        return self.Game.tipwords
    
    def activeWatch(self):  #动作监测
        for event in pygame.event.get():
            if event.type==QUIT:
                exit()
            
            #A键测试
            # if event.type==KEYDOWN:
                # if event.key==97:   #A键切换
                    # self.Table.StageSwitch()    #阶段切换
                    
                    # self.Game.handcard.pop()  #测试删牌
                    # self.Enemy.CurState=2
                    # self.Game.removeBoss()
                    # self.Game.BossGet()
                    

            #小贴士定时关闭
            if event.type==self.Game.tipsDisplay:
                self.Table.tipsShowState=False
            
            #阶段切换延时解锁
            if event.type==self.Game.stageSwitchDelay:
                self.Table.StageSwitchState=False

            #boss死亡动画延迟
            if event.type==self.Game.bossDeathDelay:
                self.Game.WaitKill=False
                self.Game.KillBoss()   #击杀判断
                
            
            if self.Table.settingClick:
                #设置菜单-退出游戏监视
                if event.type==MOUSEMOTION: #监测鼠标是否在区域内，是则显示高亮
                    if event.pos[0]>=1005 and event.pos[0]<=1065 and event.pos[1]>=510 and event.pos[1]<=570:
                        self.Table.MouseOnSetting_exit=1
                    else:
                        self.Table.MouseOnSetting_exit=0
                if event.type==MOUSEBUTTONDOWN:  #监测鼠标按下
                    if self.Table.MouseOnSetting_exit:    #如果处于区域内
                        exit()      #退出游戏

                #设置菜单-重开游戏监视
                if event.type==MOUSEMOTION: #监测鼠标是否在区域内，是则显示高亮
                    if event.pos[0]>=930 and event.pos[0]<=990 and event.pos[1]>=510 and event.pos[1]<=570:
                        self.Table.MouseOnSetting_restart=1
                    else:
                        self.Table.MouseOnSetting_restart=0
                if event.type==MOUSEBUTTONDOWN:  #监测鼠标按下
                    if self.Table.MouseOnSetting_restart:    #如果处于区域内
                        self.restartGameFun()                #重开游戏
                    
                #设置菜单-返回游戏监视
                if event.type==MOUSEMOTION: #监测鼠标是否在区域内，是则显示高亮
                    if event.pos[0]>=855 and event.pos[0]<=915 and event.pos[1]>=510 and event.pos[1]<=570:
                        self.Table.MouseOnSetting_back=1
                    else:
                        self.Table.MouseOnSetting_back=0
                if event.type==MOUSEBUTTONDOWN:  #监测鼠标按下
                    if self.Table.MouseOnSetting_back:    #如果处于区域内
                        self.Table.MouseOnSetting=0         #取消设置选中状态
                        self.Table.settingClick=False       #取消设置菜单状态
            
            if self.Table.helpClick:
                #帮助菜单
                if event.type==MOUSEBUTTONDOWN:
                    if event.pos[0]<360 or event.pos[0]>1560 or event.pos[1]<190 or event.pos[1]>890:    #点击帮助画面外时
                        self.Table.MouseOnHelp=0        #取消帮助按钮选中状态
                        self.Table.helpClick=False      #取消帮助显示
                        
            if not self.Table.settingClick and not self.Table.helpClick:         #确保设置按钮及帮助按钮按下时动作不进行
            #=====================================================================
                #设置部分动作监测
                if event.type==MOUSEMOTION: #监测鼠标是否在区域内，是则显示高亮
                    if event.pos[0]>=1860 and event.pos[0]<=1905 and event.pos[1]>=20 and event.pos[1]<=65:
                        self.Table.MouseOnSetting=1
                    else:
                        self.Table.MouseOnSetting=0
                if event.type==MOUSEBUTTONDOWN:  #监测鼠标按下
                    if self.Table.MouseOnSetting:    #如果处于区域内
                        self.Table.settingClick=True
                
                #帮助部分动作监测
                if event.type==MOUSEMOTION: #监测鼠标是否在区域内，是则显示背景
                    if event.pos[0]>=1795 and event.pos[0]<=1840 and event.pos[1]>=20 and event.pos[1]<=65:
                        self.Table.MouseOnHelp=1
                    else:
                        self.Table.MouseOnHelp=0
                if event.type==MOUSEBUTTONDOWN:  #监测滚轮
                    if self.Table.MouseOnHelp:    #如果处于区域内
                        self.Table.helpClick=True
                    
                #日志部分动作监测
                if event.type==MOUSEMOTION: #监测鼠标是否在区域内，是则显示背景
                    if event.pos[0]>=0 and event.pos[0]<=380 and event.pos[1]>=900 and event.pos[1]<=1080:
                        self.Table.logbackgroundshow=1
                    else:
                        self.Table.logbackgroundshow=0
                if event.type==MOUSEWHEEL:  #监测滚轮
                    if self.Table.logbackgroundshow:    #如果处于区域内
                        if event.y==1:  #滚轮往上
                            if self.Table.log_line_flag>0:
                                self.Table.log_line_flag-=1
                        elif event.y==-1:  #滚轮往上
                            if self.Table.log_line_flag<len(self.Table.logs)-5:
                                self.Table.log_line_flag+=1
                            
                #手牌部分动作监测
                HandArea=self.Table.calcHandCardArea(len(self.Game.handcard))
                if event.type==MOUSEMOTION: #监测鼠标是否在区域内，是则提高手牌位置
                    i=0
                    _flag=True #是否所有区域都不在
                    for xmin,xmax,ymin,ymax in HandArea:
                        if event.pos[0]>=xmin and event.pos[0]<=xmax and event.pos[1]>=ymin and event.pos[1]<=ymax:
                            self.Table.MouseOnHandCard=i
                            _flag=False
                        i+=1
                    if _flag:
                        self.Table.MouseOnHandCard=-1
                if event.type==MOUSEBUTTONDOWN:
                    if self.Table.MouseOnHandCard!=-1:
                        if self.Game.handcard[self.Table.MouseOnHandCard].Selected:
                            self.Game.selectHandCard(self.Game.handcard[self.Table.MouseOnHandCard],False)
                        else:
                            self.Game.selectHandCard(self.Game.handcard[self.Table.MouseOnHandCard],True)         

                #鬼牌部分动作监测
                if event.type==MOUSEMOTION: #监测鼠标是否在区域内，是则扩大鬼牌
                    if event.pos[0]>=90 and event.pos[0]<=213 and event.pos[1]>=660 and event.pos[1]<=833:
                        self.Table.MouseOnJokerPos=1
                    else:
                        self.Table.MouseOnJokerPos=0
                if event.type==MOUSEBUTTONDOWN:
                    if self.Table.JokerLockOn==0 and event.pos[0]>=90 and event.pos[0]<=213 and event.pos[1]>=660 and event.pos[1]<=833:
                        self.Table.JokerLockOn=1
                    elif self.Table.JokerLockOn==1 and event.pos[0]>=90 and event.pos[0]<=213 and event.pos[1]>=660 and event.pos[1]<=833:
                        self.Table.JokerLockOn=0
                        
                #出牌按钮部分动作监测
                if event.type==MOUSEMOTION: #监测鼠标是否在区域内，是则显示高亮
                    if event.pos[0]>=775 and event.pos[0]<=895 and event.pos[1]>=700 and event.pos[1]<=816:
                        self.Table.MouseOnButton_play=1
                    else:
                        self.Table.MouseOnButton_play=0
                if event.type==MOUSEBUTTONDOWN:  #监测鼠标按下
                    if self.Table.MouseOnButton_play:    #如果处于区域内
                        #按下出牌，需要判断按钮是否合法
                        
                        #出牌不合法时
                        if self.Game.ActiveButtonState[0]==2:
                            self.Table.tips(self.getTips())
                        elif self.Game.ActiveButtonState[0]==1:
                            self.Game.PlayOut() #出牌方法
                            
                    
                #弃牌按钮部分动作监测
                if event.type==MOUSEMOTION: #监测鼠标是否在区域内，是则显示高亮
                    if event.pos[0]>=925 and event.pos[0]<=1056 and event.pos[1]>=700 and event.pos[1]<=817:
                        self.Table.MouseOnButton_discard=1
                    else:
                        self.Table.MouseOnButton_discard=0
                if event.type==MOUSEBUTTONDOWN:  #监测鼠标按下
                    if self.Table.MouseOnButton_discard:    #如果处于区域内
                        #按下弃牌，需要判断按钮是否合法
                        
                        #弃牌不合法时
                        if self.Game.ActiveButtonState[1]==2:
                            self.Table.tips(self.getTips())    
                        elif self.Game.ActiveButtonState[1]==1:
                            self.Game.DiscardAction()   #弃牌方法
                    
                #过牌按钮部分动作监测
                if event.type==MOUSEMOTION: #监测鼠标是否在区域内，是则显示高亮
                    if event.pos[0]>=1075 and event.pos[0]<=1196 and event.pos[1]>=700 and event.pos[1]<=824:
                        self.Table.MouseOnButton_pass=1
                    else:
                        self.Table.MouseOnButton_pass=0
                if event.type==MOUSEBUTTONDOWN:  #监测鼠标按下
                    if self.Table.MouseOnButton_pass:    #如果处于区域内
                        #按下过牌
                        self.Game.PassAction()
                        
                    
                        
    class EnemyClass(): #敌人显示动态效果
        def __init__(self,root,BossName):
            self.screen=root.screen
            self.Back_img=pygame.image.load(base_path+'\\resource\\enemy\\'+BossName+'_back.png').convert_alpha()   #载入角标背景图片
            self.Main_img=pygame.image.load(base_path+'\\resource\\enemy\\'+BossName+'.png').convert_alpha()  #载入敌人动画序列图
            self.Hurt_img=pygame.image.load(base_path+'\\resource\\enemy\\Hurt.png').convert_alpha()   #载入伤害动画序列图
            self.BackPos=(814,143)      #背景位置
            self.EnemyPos=(795,125)     #敌人显示位置
            self.HurtEffectPos=(725,85)    #受伤效果位置
            self.frame_width=410        #敌人动画帧宽度
            self.frame_height=574       #敌人动画帧高度
            self.hurt_frame_width=392   #受伤动画帧宽度
            self.hurt_frame_height=502  #受伤动画帧高度
            #======Status======#
            #动作状态
            self.CurState=0     #0：正常状态   1：受伤过程   2：攻击过程   3：招募过程   4：死亡过程    5:结束状态（只有死亡和招募状态会转到这个状态）
            #======SubPos======#
            #子表面坐标 x,y
            self.NormalSub=(1,1)        #正常状态子表面位置
            self.DeathSub=[1,1]         #死亡动画子表面，第一行，最大八列
            self.RecruitSub=[1,2]       #招募动画子表面，第二行，最大五列
            self.ATKSub=[1,3]           #攻击动画子表面，第三行，最大七列
            self.HurtSub=[1,1]          #受伤动画子表面，受伤动画图第一行，最大九列
            #====ShowDelay=====#
            #延迟显示帧数       #攻击和被攻击动画不需要延迟
            self.Death_delay=9          #死亡动画延迟显示帧
            self.Recruit_delay=9          #招募动画延迟显示帧
        
        def ChangeStage(self,state):
            #改变当前状态   0：正常状态   1：受伤过程   2：攻击过程   3：招募过程   4：死亡过程    5:结束状态（只有死亡和招募状态会转到这个状态）
            self.CurState=state

        def Death_next(self):
            #死亡过程下一帧
            if self.CurState==4:    #死亡过程时
                if self.DeathSub[0]<8:  #帧动画     最大帧数取决于序列图长度
                    self.DeathSub[0]+=1
                else:    
                    if self.Death_delay>0:  #延迟
                        self.Death_delay-=1
                    else:
                        self.CurState=5 #转到结束状态
        def Recruit_next(self):
            #招募过程下一帧
            if self.CurState==3:    #招募过程时
                if self.RecruitSub[0]<5:  #帧动画   最大帧数取决于序列图长度
                    self.RecruitSub[0]+=1
                else:    
                    if self.Recruit_delay>0:  #延迟
                        self.Recruit_delay-=1
                    else:
                        self.CurState=5 #转到结束状态
        def ATK_next(self):
            #攻击过程下一帧
            if self.CurState==2:    #攻击过程时
                if self.ATKSub[0]<7:  #帧动画   最大帧数取决于序列图长度
                    self.ATKSub[0]+=1
                else:
                    self.ATKSub[0]=1
                    self.CurState=0 #转回正常
        def Hurt_next(self):
            #受伤过程下一帧
            if self.CurState==1:    #受伤过程时
                if self.HurtSub[0]<9:  #帧动画   最大帧数取决于序列图长度
                    self.HurtSub[0]+=1
                else:
                    self.HurtSub[0]=1
                    self.CurState=0 #转回正常
                    

        def update(self):   #显示输出
            #更新子表面
            if self.CurState==0:    #普通状态                
                back_img=pygame.transform.scale(self.Back_img,(343,475))    
                self.screen.blit(back_img,self.BackPos)    #角标背景

                image=pygame.Surface.subsurface(self.Main_img,pygame.rect.Rect(((self.NormalSub[0]-1)*self.frame_width, (self.NormalSub[1]-1)*self.frame_height),(self.frame_width,self.frame_height)))
                self.screen.blit(image,(self.EnemyPos[0],self.EnemyPos[1]))
            elif self.CurState==1:  #受伤状态
                back_img=pygame.transform.scale(self.Back_img,(343,475))    
                self.screen.blit(back_img,self.BackPos)    #角标背景
                
                image=pygame.Surface.subsurface(self.Main_img,pygame.rect.Rect(((self.NormalSub[0]-1)*self.frame_width, (self.NormalSub[1]-1)*self.frame_height),(self.frame_width,self.frame_height)))
                image2=pygame.Surface.subsurface(self.Hurt_img,pygame.rect.Rect(((self.HurtSub[0]-1)*self.hurt_frame_width, (self.HurtSub[1]-1)*self.hurt_frame_height),(self.hurt_frame_width,self.hurt_frame_width)))
                self.screen.blit(image,(self.EnemyPos[0],self.EnemyPos[1]))        #boss底图
                
                image2=pygame.transform.scale(image2,(410,574))
                self.screen.blit(image2,(self.HurtEffectPos[0],self.HurtEffectPos[1])) #攻击动画
            elif self.CurState==2:  #攻击状态
                back_img=pygame.transform.scale(self.Back_img,(343,475))    
                self.screen.blit(back_img,self.BackPos)    #角标背景
                
                image=pygame.Surface.subsurface(self.Main_img,pygame.rect.Rect(((self.ATKSub[0]-1)*self.frame_width, (self.ATKSub[1]-1)*self.frame_height),(self.frame_width,self.frame_height)))
                image2=pygame.Surface.subsurface(self.Main_img,pygame.rect.Rect(((self.NormalSub[0]-1)*self.frame_width, (self.NormalSub[1]-1)*self.frame_height),(self.frame_width,self.frame_height)))
                
                
                self.screen.blit(image2,(self.EnemyPos[0],self.EnemyPos[1]))       #boss原图
                self.screen.blit(image,(self.EnemyPos[0],self.EnemyPos[1]))        #boss扩大线条
            elif self.CurState==3:   #招募状态
                back_img=pygame.transform.scale(self.Back_img,(343,475))    
                self.screen.blit(back_img,self.BackPos)    #角标背景
                
                image=pygame.Surface.subsurface(self.Main_img,pygame.rect.Rect(((self.RecruitSub[0]-1)*self.frame_width, (self.RecruitSub[1]-1)*self.frame_height),(self.frame_width,self.frame_height)))
                self.screen.blit(image,(self.EnemyPos[0],self.EnemyPos[1]))
            elif self.CurState==4:   #死亡状态
                back_img=pygame.transform.scale(self.Back_img,(343,475))    
                self.screen.blit(back_img,self.BackPos)    #角标背景
                
                image=pygame.Surface.subsurface(self.Main_img,pygame.rect.Rect(((self.DeathSub[0]-1)*self.frame_width, (self.DeathSub[1]-1)*self.frame_height),(self.frame_width,self.frame_height)))
                self.screen.blit(image,(self.EnemyPos[0],self.EnemyPos[1]))
                
                
    class TableClass():
        def __init__(self,root):          
            self.root=root              #映射
            self.screen=root.screen     
            self.Game=root.Game
            self._card=self.Game.cardObj
            self.logInfo()
            
            #鼠标状态
            self.MouseOnJokerPos=0
            self.JokerLockOn=0
            self.MouseOnHandCard=-1 #鼠标是否在手牌上，如果是则显示牌顺序下标（从0开始），否则为-1
            self.MouseOnSetting=0   #鼠标是否在设置按钮上
            self.MouseOnHelp=0      #鼠标是否在帮助按钮上
            self.MouseOnSetting_restart=0   #鼠标是否在设置-重开游戏上
            self.MouseOnSetting_exit=0   #鼠标是否在设置-退出游戏上
            self.MouseOnSetting_back=0   #鼠标是否在设置-返回游戏上
            self.MouseOnButton_play=0       #鼠标是否在出牌按钮上
            self.MouseOnButton_discard=0    #鼠标是否在弃牌按钮上
            self.MouseOnButton_pass=0       #鼠标是否在过牌按钮上
            
            #阶段指针状态
            self.BackgroundPos=[420,360]
            self.PointerPos=[self.BackgroundPos[0]-8,self.BackgroundPos[1]+13]  #指针与背景初始相对位置
            self.PointerState=self.Game.StageNum    #获取当前阶段
            self.StageSwitchState=False #阶段切换状态
            self.PointerMoveState=False #指针移动状态
            self.PointerCurPos=0    #指针当前位置偏移量
            self.StageSwitchTime=1000   #切换动画时间（毫秒）
            self.PointerStageMove=58    #每阶段移动距离
            self.NowPos=self.PointerState * self.PointerStageMove       #本阶段位置
            self.CurMove=self.PointerState * self.PointerStageMove - self.NowPos     #当前所需移动距离
            self.PointerSpeed=self.CurMove / (self.root.FPS * self.StageSwitchTime / 1000)      #指针偏移速度   当前所需移动距离/(帧率x动画时间(毫秒)/1000)
            
            #手牌
            self.MaxCard=self.Game.MaxHandCard  #最大手牌数
            self.HandShowObj=[]                 #手牌显示对象
            self.HandMidPos=990     #手牌中央点横坐标   
            self.HandYPOS=880       #手牌纵坐标
            #手牌0.3倍宽度123，高度171 标准宽度410 标准高度574
            self.CardStandardWeight=410 #标准宽
            self.CardStandardHeight=574 #标准高
            self.NarrowRate=0.3         #缩小倍率
            self.HandCardGap=10     #手牌间隙
            
            #小贴士
            self.tipsShow=[] #可能超长，需要自动分段
            self.tipsShowTime=5000  #5000毫秒
            self.tipsMaxWords=14    #一行最大显示文字数量
            self.tipsShowState=False    #显示状态
            
            #设置
            self.settingClick=False     #设置按钮点击状态
            
            #帮助
            self.helpClick=False        #设置帮助按钮点击状态
            
            #阶段切换延迟
            self.stageSwitchDelayTime=1000  #阶段切换延迟1000毫秒
            
            # self.Game.cemetery.append(self.Game.cardpub.pop())
            # self.Game.cemetery.append(self.Game.cardpub.pop())
            # self.Game.cemetery.append(self.Game.cardpub.pop())
            # self.Game.cemetery.append(self.Game.cardpub.pop())
            # self.Game.cemetery.append(self.Game.cardpub.pop())
            # self.Game.cardpub=[]
            # self.log('中华人民共和国中华人民共和国中华人民共和国')
            # self.tips('中华人民共和国中央人民政府中华人民共和国')

        def initLoad(self):
            #图像初始加载到内存
            
            #选择后背景图像
            self.selectback=pygame.image.load(base_path+'\\resource\\table\\selectback.png').convert_alpha()  
            #敌人显示列表
            self.EnemyList_Show=[]
            for i in range(12):
                tmp=pygame.image.load(base_path+'\\resource\\enemy\\enemylist_unknow_card.png').convert_alpha()
                tmp=self.adjustmentObj(tmp,0.110,0)
                self.EnemyList_Show.append(tmp)
            #敌人显示列表背景
            self.EnemyList_Back=pygame.image.load(base_path+'\\resource\\enemy\\enemylist_kill_front.png').convert_alpha()
            #敌人显示背景
            self.EnemyBack=pygame.image.load(base_path+'\\resource\\table\\enemybackground.png').convert_alpha()  #载入敌人背景
            self.EnemyBack=self.adjustmentObj(self.EnemyBack,1.1,0)
            self.HPBack=pygame.image.load(base_path+'\\resource\\table\\HPpic.png').convert_alpha()  #载入生命值图标
            self.HPBack=pygame.transform.scale(self.HPBack,(104,94))
            self.ATKBack=pygame.image.load(base_path+'\\resource\\table\\ATKpic.png').convert_alpha()  #载入攻击力图标
            self.ATKBack=pygame.transform.scale(self.ATKBack,(121,117))
            #小丑背景显示
            self.Jokerbackground=pygame.image.load(base_path+'\\resource\\table\\jokerbackground.png').convert_alpha()  #载入酒馆显示背景
            self.Jokerbackground=self.adjustmentObj(self.Jokerbackground,0.3,0)
            #酒馆预载
            self.pubbackground=pygame.image.load(base_path+'\\resource\\table\\cardbackground.png').convert_alpha()  #载入酒馆显示背景
            self.pubbackground=self.adjustmentObj(self.pubbackground,0.4,0)
            self.pubcardback=pygame.image.load(base_path+'\\resource\\cards\\CardBack.png')  #载入酒馆剩余卡背
            self.pubcardback=self.adjustmentObj(self.pubcardback,0.395,0)
            #墓地预载
            self.Cemeterybackground=pygame.image.load(base_path+'\\resource\\table\\cardbackground.png').convert_alpha()  #载入墓地显示背景
            self.Cemeterybackground=self.adjustmentObj(self.Cemeterybackground,0.4,0)
            #日志背景预载
            self.logbackground=pygame.image.load(base_path+'\\resource\\table\\logbackground.png').convert_alpha()
            self.logbackground=pygame.transform.scale(self.logbackground,(380,180))
            #小贴士背景预载
            self.Tipsbackground=pygame.image.load(base_path+'\\resource\\table\\tipsbackground.png').convert_alpha()  #载入阶段背景
            self.Tipsbackground=pygame.transform.scale(self.Tipsbackground,(190,140))
            #阶段指示器预载
            self.Stagebackground=pygame.image.load(base_path+'\\resource\\table\\stagebackground.png').convert_alpha()  #载入阶段背景
            self.Stagebackground=pygame.transform.scale(self.Stagebackground,(280,250))
            self.Stagepointer=pygame.image.load(base_path+'\\resource\\table\\stagepointer.png').convert_alpha()  #载入阶段指针
            self.Stagepointer=pygame.transform.scale(self.Stagepointer,(295,55))
            #出牌动作按钮预载
            self.play_able_button=pygame.image.load(base_path+'\\resource\\table\\play_able.png').convert_alpha()  #载入出牌按钮可用状态
            self.play_able_button=pygame.transform.scale(self.play_able_button,(120,116))
            self.play_disable_button=pygame.image.load(base_path+'\\resource\\table\\play_disable.png').convert_alpha()  #载入出牌按钮不可用状态
            self.play_disable_button=pygame.transform.scale(self.play_disable_button,(120,116))
            self.play_selected_button=pygame.image.load(base_path+'\\resource\\table\\play_selected.png').convert_alpha()  #载入出牌按钮被选择状态
            self.play_selected_button=pygame.transform.scale(self.play_selected_button,(120,116))
            self.play_illegal_button=pygame.image.load(base_path+'\\resource\\table\\play_illegal.png').convert_alpha()  #载入出牌按钮被选择状态
            self.play_illegal_button=pygame.transform.scale(self.play_illegal_button,(120,116))
            self.play_illegal_selected_button=pygame.image.load(base_path+'\\resource\\table\\play_illegal_selected.png').convert_alpha()  #载入出牌按钮被选择状态
            self.play_illegal_selected_button=pygame.transform.scale(self.play_illegal_selected_button,(120,116))
            
            self.discard_able_button=pygame.image.load(base_path+'\\resource\\table\\discard_able.png').convert_alpha()  #载入弃牌按钮可用状态
            self.discard_able_button=pygame.transform.scale(self.discard_able_button,(131,117))
            self.discard_disable_button=pygame.image.load(base_path+'\\resource\\table\\discard_disable.png').convert_alpha()  #载入弃牌按钮不可用状态
            self.discard_disable_button=pygame.transform.scale(self.discard_disable_button,(131,117))
            self.discard_selected_button=pygame.image.load(base_path+'\\resource\\table\\discard_selected.png').convert_alpha()  #载入弃牌按钮被选择状态
            self.discard_selected_button=pygame.transform.scale(self.discard_selected_button,(131,117))
            self.discard_illegal_button=pygame.image.load(base_path+'\\resource\\table\\discard_illegal.png').convert_alpha()  #载入弃牌按钮被选择状态
            self.discard_illegal_button=pygame.transform.scale(self.discard_illegal_button,(131,117))
            self.discard_illegal_selected_button=pygame.image.load(base_path+'\\resource\\table\\discard_illegal_selected.png').convert_alpha()  #载入弃牌按钮被选择状态
            self.discard_illegal_selected_button=pygame.transform.scale(self.discard_illegal_selected_button,(131,117))
            
            
            self.pass_able_button=pygame.image.load(base_path+'\\resource\\table\\pass_able.png').convert_alpha()  #载入过牌按钮可用状态
            self.pass_able_button=pygame.transform.scale(self.pass_able_button,(121,124))
            self.pass_disable_button=pygame.image.load(base_path+'\\resource\\table\\pass_disable.png').convert_alpha()  #载入过牌按钮不可用状态
            self.pass_disable_button=pygame.transform.scale(self.pass_disable_button,(121,124))
            self.pass_selected_button=pygame.image.load(base_path+'\\resource\\table\\pass_selected.png').convert_alpha()  #载入过牌按钮被选择状态
            self.pass_selected_button=pygame.transform.scale(self.pass_selected_button,(121,124))
            
            
        def Turn(self,aBoolean):
            #翻转布尔值
            return not aBoolean
        
        def calcHandCardArea(self,Total):
            #计算手牌位置区域
            assert Total>=0 and Total<=self.MaxCard,totalHandValueError
            Area=[]
            for i in range(Total):
                Xmin = self.HandMidPos - (self.CardStandardWeight * self.NarrowRate * Total + (Total-1) * self.HandCardGap) / 2 + (self.CardStandardWeight * self.NarrowRate + self.HandCardGap) * i
                Xmax = Xmin + self.CardStandardWeight * self.NarrowRate
                Ymin = self.HandYPOS
                Ymax = Ymin + self.CardStandardHeight * self.NarrowRate
                Area.append((Xmin,Xmax,Ymin,Ymax))  #算出X和Y的最大最小值
            return Area
                

        def calcHandCardPos(self,Total,Num):
            #计算手牌坐标
            #输入Total当前手牌总数(1开始)，Num当前手牌顺序(0开始)
            #返回坐标及宽高（x,y,w,h）
            #纵坐标固定为初始纵坐标HandYPos
            assert Total>=Num + 1,handPosValueError  #输入验证
            
            #中间坐标-（标准卡牌宽*缩小率*总卡牌数+（总卡牌数-1）*卡牌间隙）/ 2 + (标准卡牌宽*缩小率+卡牌间隙)*第几张卡
            _x = self.HandMidPos - (self.CardStandardWeight * self.NarrowRate * Total + (Total-1) * self.HandCardGap) / 2 + (self.CardStandardWeight * self.NarrowRate + self.HandCardGap) * Num
            _y = self.HandYPOS
            _w = self.CardStandardWeight * self.NarrowRate
            _h = self.CardStandardHeight * self.NarrowRate
            return (_x,_y,_w,_h)
            

        def tips(self,aText):
            if aText != null or aText != '':
                self.tipsShow=[aText[i:i+self.tipsMaxWords] for i in range(0,len(aText),self.tipsMaxWords)]
                self.tipsShowState=True
                pygame.time.set_timer(self.Game.tipsDisplay,self.tipsShowTime,1)  #设置定时器定时关闭
            
            
        def StageSwitch(self,aStage=null):  #阶段切换，若参数为默认，则直接切换，否则切换到指定参数
            if self.StageSwitchState==False:    #移动中不可切换
                if self.Game.StageNum==aStage or aStage not in (0,1,2,3,null):
                    return False
                else:
                    if aStage != null:
                        self.Game.StageNum=aStage
                        self.StageMove()
                        return True
                    else:
                        if self.Game.StageNum==3:
                            self.Game.StageNum=0
                        else:
                            self.Game.StageNum+=1
                        self.StageMove()
                        return True
            else:
                return False
        def StageMove(self):
            self.PointerMoveState=True
            self.StageSwitchState=True
            self.PointerState=self.Game.StageNum    #获取当前阶段
            self.CurMove=self.PointerState * self.PointerStageMove - self.NowPos     #当前所需移动距离
            self.PointerSpeed=self.CurMove / (self.StageSwitchTime / 1000 * self.root.FPS) *15     #指针偏移速度   当前所需移动距离/(帧率x动画时间(毫秒)/1000)  *15（可能跟计算速率有关，速度没有达到理想状态，乘以15加速

        def ShowTable(self):
            #显示桌面信息  包含 酒馆（包含剩余卡数），墓地，手牌（包含被选中状态），鬼牌位，敌人位，敌方生命攻击信息，战斗日志，出、弃牌按钮位，规则提示按钮，重置、退出游戏按钮，boss进度显示区,游戏阶段进度显示区
            self._showHand()        #手牌显示
            self._showPub()         #酒馆显示
            self._showCemetery()    #墓地显示
            self._showJokerpos()    #鬼牌位显示
            self._showLog()         #日志显示
            self._showStageIndicator()  #阶段指示器显示
            self._showTips()        #小贴士显示
            self._showDecorIndicator()  #花色指示器显示
            self._showEnemyBack()         #显示敌方背景
            self._showEnemy()             #显示敌方
            self._showEnemyList()         #显示敌方列表
            self._showActiveButton()      #出牌动作按钮预载
            
            #处于最上层（最后绘图）
            self._showSettingButton()   #设置按钮显示
            self._showHelpButton()      #帮助按钮显示
            
        
        def adjustmentObj(self,aSurface,proportion=1,Slope=0):
            #获取缩放对象
            return pygame.transform.rotozoom(aSurface,Slope,proportion) #控制缩放比率及斜率
        
        def _showActiveButton(self):
            #显示行动按钮，根据rule类中状态决定显示情况
            if self.root.Game.ActiveButtonState[0]==0:
                self.screen.blit(self.play_disable_button,(775,700))
            elif self.root.Game.ActiveButtonState[0]==1:
                if self.MouseOnButton_play==0:
                    self.screen.blit(self.play_able_button,(775,700))
                else:
                    self.screen.blit(self.play_selected_button,(775,700))
            elif self.root.Game.ActiveButtonState[0]==2:
                if self.MouseOnButton_play==0:
                    self.screen.blit(self.play_illegal_button,(775,700))
                else:
                    self.screen.blit(self.play_illegal_selected_button,(775,700))
                
            if self.root.Game.ActiveButtonState[1]==0:
                self.screen.blit(self.discard_disable_button,(925,700))
            elif self.root.Game.ActiveButtonState[1]==1:
                if self.MouseOnButton_discard==0:
                    self.screen.blit(self.discard_able_button,(925,700))
                else:
                    self.screen.blit(self.discard_selected_button,(925,700))    
            elif self.root.Game.ActiveButtonState[1]==2:
                if self.MouseOnButton_discard==0:
                    self.screen.blit(self.discard_illegal_button,(925,700))
                else:
                    self.screen.blit(self.discard_illegal_selected_button,(925,700)) 
                
            if self.root.Game.ActiveButtonState[2]==0:
                self.screen.blit(self.pass_disable_button,(1075,700))
            elif self.root.Game.ActiveButtonState[2]==1:
                if self.MouseOnButton_pass==0:
                    self.screen.blit(self.pass_able_button,(1075,700))
                else:
                    self.screen.blit(self.pass_selected_button,(1075,700))
                
        
        def _showEnemyList(self):
            #显示敌方列表，未知敌人显示为问号，当前敌人正常显示，已击杀敌人灰色，已感化敌人金色
            
            listPosX=85     #列表起始点X
            listPosY=160    #列表起始点Y
            gap=55          #间隔
            
            _tmp=pygame.transform.scale(self.EnemyList_Back,(gap*12+10,574*0.11+20))
            self.screen.blit(_tmp,(listPosX-10.,listPosY-10))
            
            n=0             #计数器
            for i in self.EnemyList_Show:
                if isinstance(i,tuple):
                    self.screen.blit(i[0],(listPosX+n*gap,listPosY))
                    self.screen.blit(i[1],(listPosX+n*gap,listPosY))
                else:
                    self.screen.blit(i,(listPosX+n*gap,listPosY))
                n+=1
        def EnemyListChange(self,num,aType,aCard=None):
            #敌人列表状态变换   Num为顺序，aType为类型，aCard为卡名
            if aType==0:    #未知状态
                _tmp=pygame.image.load(base_path+'\\resource\\enemy\\enemylist_unknow_card.png').convert_alpha()
                _tmp=self.adjustmentObj(_tmp,0.110,0)
            elif aType==1:    #正常显示状态
                _tmp=pygame.image.load(base_path+'\\resource\\cards\\'+aCard+'.jpg').convert_alpha()
                _tmp=self.adjustmentObj(_tmp,0.110,0)
            elif aType==2:    #死亡状态
                _tmp=pygame.image.load(base_path+'\\resource\\cards\\'+aCard+'.jpg').convert_alpha()
                _tmp=self.adjustmentObj(_tmp,0.110,0)
                _tmp2=pygame.image.load(base_path+'\\resource\\enemy\\enemylist_kill_front.png').convert_alpha()
                _tmp2=self.adjustmentObj(_tmp2,0.110,0)
                _tmp=(_tmp,_tmp2)
            elif aType==3:    #招募状态
                _tmp=pygame.image.load(base_path+'\\resource\\cards\\'+aCard+'.jpg').convert_alpha()
                _tmp=self.adjustmentObj(_tmp,0.110,0)
                _tmp2=pygame.image.load(base_path+'\\resource\\enemy\\enemylist_recruit_front.png').convert_alpha()
                _tmp2=self.adjustmentObj(_tmp2,0.110,0)
                _tmp=(_tmp,_tmp2)
            self.EnemyList_Show[num]=_tmp
        
        def _showEnemy(self):
            #显示敌方
            self.root.Enemy.update()
            
        def _showEnemyBack(self):
            #显示敌人背景

            EnemyBackPos=self.EnemyBack.get_rect()       #获取图像宽度
            self.screen.blit(self.EnemyBack,(960-EnemyBackPos[2]/2+25,540-EnemyBackPos[3]/2-160))    #通过计算和手动补偿调整位置
            #显示攻击面板及生命面板
            
            self.screen.blit(self.HPBack,(1200,280))
            self.screen.blit(self.ATKBack,(1180,420))
            #面板数值显示
            t_font =  pygame.font.Font(base_path+'fonts\\msyhbd.ttc',60)    #载入字体
            try:
                _ATK=str(self.Game.BossATK)
                _HP=str(self.Game.BossHP)
            except Exception as f:
                _ATK='Null'
                _HP='Null'
            t_text = t_font.render(_HP+self.Game.assist_HP,True,(200,200,200)) #HP显示
            self.screen.blit(t_text,(1312,310))
            t_text2 = t_font.render(_ATK+self.Game.assist_ATK,True,(200,200,200)) #ATK显示
            self.screen.blit(t_text2,(1312,435))
                             
            
        def _showDecorIndicator(self):
            #显示花色指示器
            #指示器只获取规则类中指示器状态并显示
            
            Indicator_high=630  #指示器高度
            Size=60     #指示器大小
            spacing=6   #间距
            Midpos=960  #中间点

            Club_Indicator=pygame.image.load(base_path+'\\resource\\table\\DecorType\\Club_'+str(self.Game.DecorShow[0])+'.png').convert_alpha()  #载入花色指示器-梅花
            Club_Indicator=pygame.transform.scale(Club_Indicator,(Size,Size))
            Diamond_Indicator=pygame.image.load(base_path+'\\resource\\table\\DecorType\\Diamond_'+str(self.Game.DecorShow[1])+'.png').convert_alpha()  #载入花色指示器-方块
            Diamond_Indicator=pygame.transform.scale(Diamond_Indicator,(Size,Size))
            Spade_Indicator=pygame.image.load(base_path+'\\resource\\table\\DecorType\\Spade_'+str(self.Game.DecorShow[2])+'.png').convert_alpha()  #载入花色指示器-黑桃
            Spade_Indicator=pygame.transform.scale(Spade_Indicator,(Size,Size))
            Heart_Indicator=pygame.image.load(base_path+'\\resource\\table\\DecorType\\Heart_'+str(self.Game.DecorShow[3])+'.png').convert_alpha()  #载入花色指示器-红桃
            Heart_Indicator=pygame.transform.scale(Heart_Indicator,(Size,Size))            
            
            self.screen.blit(Club_Indicator,(Midpos-Size/2-spacing-spacing/2-Size,Indicator_high))   #梅花
            self.screen.blit(Diamond_Indicator,(Midpos-Size/2-spacing/2,Indicator_high)) #方块
            self.screen.blit(Spade_Indicator,(Midpos+Size/2+spacing/2,Indicator_high))   #黑桃
            self.screen.blit(Heart_Indicator,(Midpos+Size/2+spacing+spacing/2+Size,Indicator_high))  #红桃
        
        def _showSettingButton(self):
            #显示设置按钮
            if not self.MouseOnSetting and not self.settingClick:
                SettingButton=pygame.image.load(base_path+'\\resource\\button\\settingbutton.png').convert_alpha()  #载入设置按钮图1
            else:
                SettingButton=pygame.image.load(base_path+'\\resource\\button\\settingbutton2.png').convert_alpha()  #载入设置按钮图2
            SettingButton=pygame.transform.scale(SettingButton,(45,45))
            self.screen.blit(SettingButton,(1920-60,20))
            
            if self.settingClick:
                SettingBack=pygame.image.load(base_path+'\\resource\\table\\logbackground.png').convert_alpha()  #载入设置背景
                SettingBack=pygame.transform.scale(SettingBack,(250,80))
                SettingBack2=pygame.transform.scale(SettingBack,(1920,1080))

                t_font =  pygame.font.Font(base_path+'fonts\\msyh.ttc',14)    #载入字体

                if self.MouseOnSetting_back:
                    setting_backgame=pygame.image.load(base_path+'\\resource\\button\\backgame2.png').convert_alpha()  #载入返回游戏按钮
                    t_text = t_font.render('返回游戏',True,(255,255,255)) #返回游戏文本
                    t_textRect=t_text.get_rect() #获取文本区域      内容为左上角的x，y坐标及宽，高  (x,y,w,h)
                    t_textRect.center = (885,585) #设置文本显示位置中点
                else:
                    setting_backgame=pygame.image.load(base_path+'\\resource\\button\\backgame.png').convert_alpha()  #载入返回游戏按钮
                setting_backgame=pygame.transform.scale(setting_backgame,(60,60))
                if self.MouseOnSetting_restart:
                    setting_restart=pygame.image.load(base_path+'\\resource\\button\\restartgame2.png').convert_alpha()  #载入重开按钮
                    t_text = t_font.render('重开游戏',True,(255,255,255)) #重开游戏文本
                    t_textRect=t_text.get_rect() #获取文本区域      内容为左上角的x，y坐标及宽，高  (x,y,w,h)
                    t_textRect.center = (960,585) #设置文本显示位置中点
                else:
                    setting_restart=pygame.image.load(base_path+'\\resource\\button\\restartgame.png').convert_alpha()  #载入重开按钮                    
                setting_restart=pygame.transform.scale(setting_restart,(60,60))
                if self.MouseOnSetting_exit:
                    setting_exitgame=pygame.image.load(base_path+'\\resource\\button\\exitgame2.png').convert_alpha()  #载入退出游戏按钮
                    t_text = t_font.render('退出游戏',True,(255,255,255)) #退出游戏文本
                    t_textRect=t_text.get_rect() #获取文本区域      内容为左上角的x，y坐标及宽，高  (x,y,w,h)
                    t_textRect.center = (1035,585) #设置文本显示位置中点
                else:
                    setting_exitgame=pygame.image.load(base_path+'\\resource\\button\\exitgame.png').convert_alpha()  #载入退出游戏按钮
                setting_exitgame=pygame.transform.scale(setting_exitgame,(60,60))
                self.screen.blit(SettingBack2,(0,0))
                self.screen.blit(SettingBack,(960-250/2,540-80/2))
                
                self.screen.blit(setting_backgame,(960-60/2-75,540-60/2))
                self.screen.blit(setting_restart,(960-60/2,540-60/2))
                self.screen.blit(setting_exitgame,(960-60/2+75,540-60/2))
                
                if self.MouseOnSetting_back or self.MouseOnSetting_restart or self.MouseOnSetting_exit: #当任意按钮区域被指向时才会显示文本
                    self.screen.blit(t_text,t_textRect) #显示文本
                


        def _showHelpButton(self):
            #显示帮助按钮
            if not self.MouseOnHelp and not self.helpClick:
                HelpButton=pygame.image.load(base_path+'\\resource\\button\\helpbutton.png').convert_alpha()  #载入帮助按钮图1
            else:
                HelpButton=pygame.image.load(base_path+'\\resource\\button\\helpbutton2.png').convert_alpha()  #载入帮助按钮图2
            HelpButton=pygame.transform.scale(HelpButton,(45,45))
            self.screen.blit(HelpButton,(1920-125,20))
            
            if self.helpClick:
                HelpPic=pygame.image.load(base_path+'\\resource\\table\\helppic.png').convert_alpha()  #载入帮助说明图
                HelpPic=pygame.transform.scale(HelpPic,(1200,700))
                self.screen.blit(HelpPic,((1920-1200)/2,(1080-700)/2))
        
        def _showStageIndicator(self):
            #显示阶段指示器            
            self.screen.blit(self.Stagebackground,self.BackgroundPos)

            if self.PointerMoveState==True:
                self.PointerCurPos+=self.PointerSpeed
                if abs(self.PointerState * self.PointerStageMove - self.PointerCurPos) <= 1:
                    self.PointerCurPos = self.PointerState * self.PointerStageMove
                    self.NowPos = self.PointerCurPos
                    self.PointerMoveState=False
                    pygame.time.set_timer(self.Game.stageSwitchDelay,self.stageSwitchDelayTime,1)  #设置定时器定时关闭
                    
            self.screen.blit(self.Stagepointer,(self.PointerPos[0],self.PointerPos[1]+self.PointerCurPos)) #安装阶段状态直接设置 后续做成动画
            
        def _showTips(self):
            #显示小贴士
            if self.tipsShowState==True:
                self.screen.blit(self.Tipsbackground,(1240,650))
                t_font =  pygame.font.Font(base_path+'fonts\\msyhl.ttc',12)
                for i in range(len(self.tipsShow)):
                    self.screen.blit(t_font.render(self.tipsShow[i],True,(0,0,0)),(1250,670+i*14)) #墓地卡牌数量显示
                
        
        def _showCemetery(self):
            #显示墓地
            t_font =  pygame.font.Font(base_path+'fonts\\msyh.ttc',16)
            t_font2 =  pygame.font.Font(base_path+'fonts\\msyhbd.ttc',25)
            t_font3 =  pygame.font.Font(base_path+'fonts\\courbd.ttf',47)
            
            t_text = t_font.render('阵亡卡牌:'+str(len(self.Game.cemetery)),True,(250,250,250)) #墓地卡牌数量显示
            t_text2 = t_font2.render('墓地',True,(220,220,220)) #墓地招牌
            
            t_text3 = t_font3.render(self.Game.assist_cemetery,True,(235,235,235)) #辅助显示  (160,52,46)
            t_rect3=t_text3.get_rect()
            t_rect3.center=(1785,630)
            
            self.screen.blit(self.Cemeterybackground,(1700,510))  #显示背景                 
            self.screen.blit(t_text,(1770,750))        #显示剩余数
            self.screen.blit(t_text2,(1710,740))        #显示招牌
            
            j=0
            for i in self.Game.cemetery:        #显示牌
                _name=i.getName()
                _card=self.adjustmentObj(self._card[_name],0.395,0)
                self.screen.blit(_card,(1700+j//2,511-j//3))
                j+=1
            
            if self.Game.assist_cemetery!='':
                _background=pygame.transform.scale(self.logbackground,(t_rect3[2],t_rect3[3]))
                self.screen.blit(_background,t_rect3)
            
            self.screen.blit(t_text3,t_rect3)        #辅助显示
        
        def _showPub(self):
            #显示酒馆
            t_font =  pygame.font.Font(base_path+'fonts\\msyh.ttc',16)
            t_font2 =  pygame.font.Font(base_path+'fonts\\msyhbd.ttc',25)
            t_font3 =  pygame.font.Font(base_path+'fonts\\msyhbd.ttc',38)
            
            t_text = t_font.render('剩余卡牌:'+str(len(self.Game.cardpub)),True,(250,250,250)) #卡牌剩余数量显示
            t_text2 = t_font2.render('酒馆',True,(220,220,220)) #酒馆招牌
            
            t_text3 = t_font3.render(self.Game.assist_pub,True,(220,220,220)) #显示辅助
            t_rect3=t_text3.get_rect()
            t_rect3.center=(1622,960)
                             
            self.screen.blit(self.pubbackground,(1700,810))  #显示背景
            for i in range(len(self.Game.cardpub)):     #显示牌
                self.screen.blit(self.pubcardback,(1700+i//2,811-i//3))
            self.screen.blit(t_text,(1770,1050))        #显示剩余数
            self.screen.blit(t_text2,(1710,1040))        #显示招牌
            self.screen.blit(t_text3,t_rect3)        #显示辅助
            
        def _showJokerpos(self):
            #显示鬼牌位
            
            t_font =  pygame.font.Font(base_path+'fonts\\msyh.ttc',18)
            t_text = t_font.render('鬼牌可用次数:'+str(len(self.Game.jokerpos))+'/2',True,(250,250,250)) #鬼牌剩余可用次数显示

            self.screen.blit(self.Jokerbackground,(90,660))  #显示背景
            self.screen.blit(t_text,(78,615))        #显示剩余数
            for i in self.Game.jokerpos:        #显示牌
                _name=i.getName()
                if self.JokerLockOn:
                    _select=pygame.transform.scale(self.selectback,(170,238))   #背景贴一个选项框
                    self.screen.blit(_select,(68,645))                    
                    _card=self.adjustmentObj(self._card[_name],0.4,0)
                    self.screen.blit(_card,(71,650))
                elif self.MouseOnJokerPos:
                    _card=self.adjustmentObj(self._card[_name],0.4,0)
                    self.screen.blit(_card,(71,650))
                else:
                    _card=self.adjustmentObj(self._card[_name],0.3,0)
                    self.screen.blit(_card,(90,660))
            
        def _showLog(self):
            #战斗日志显示
            t_font =  pygame.font.Font(base_path+'fonts\\msyh.ttc',22)
            self.logLineUpdate()    #获取最新显示内容
            
            if self.logbackgroundshow==1:       #日志背景，鼠标处于区域内才显示
                self.screen.blit(self.logbackground,(0,900))
            
            t_text1 = t_font.render(self.log_line[0],True,self.logcolor) #文本内容第一行 #不能换行
            t_text2 = t_font.render(self.log_line[1],True,self.logcolor) #文本内容第二行 #不能换行
            t_text3 = t_font.render(self.log_line[2],True,self.logcolor) #文本内容第三行 #不能换行
            t_text4 = t_font.render(self.log_line[3],True,self.logcolor) #文本内容第四行 #不能换行
            t_text5 = t_font.render(self.log_line[4],True,self.logcolor) #文本内容第五行 #不能换行

            # t_textRect=t_text.get_rect() #获取文本区域      内容为左上角的x，y坐标及宽，高  (x,y,w,h)
            # t_textRect.center = (960,540) #设置文本显示位置中点

            self.screen.blit(t_text1,(self.logpos[0],self.logpos[1]+0*self.logpos[3],self.logpos[2],self.logpos[3]))   #显示日志，根据标准坐标重叠
            self.screen.blit(t_text2,(self.logpos[0],self.logpos[1]+1*self.logpos[3],self.logpos[2],self.logpos[3]))
            self.screen.blit(t_text3,(self.logpos[0],self.logpos[1]+2*self.logpos[3],self.logpos[2],self.logpos[3]))
            self.screen.blit(t_text4,(self.logpos[0],self.logpos[1]+3*self.logpos[3],self.logpos[2],self.logpos[3]))
            self.screen.blit(t_text5,(self.logpos[0],self.logpos[1]+4*self.logpos[3],self.logpos[2],self.logpos[3]))
            # print(t_textRect)
    
        def log(self,logstring):
            #记录日志   
            line = len(logstring) // self.wordscount #一行取self.wordscount个汉字
            if len(logstring) % self.wordscount != 0:     #超过部分单独成行
                line+=1
            for i in range(line):
                self.logs.append(logstring[i*self.wordscount:i*self.wordscount+self.wordscount])   #录入日志
            self.log_line_flag=len(self.logs)-5 #重置行标
            if self.log_line_flag<0:
                self.log_line_flag=0
        
        def logInfo(self):
            #战斗日志参数
            self.logcolor=(240,255,240)         #日志颜色
            self.logpos=(15,915,350,30)        #日志标准坐标
            self.wordscount=15                  #一行取字数，要跟self.logpos第三个值（宽度）联动
            self.logs=[] #所有日志内容
            self.log_line=['','','','','']   #log显示内容，行数最大为5，一行取self.wordscount个字
            self.log_line_flag=0    #当前行标
            self.logbackgroundshow=0
            
        def logLineUpdate(self):
            #更新战斗日志显示数据
            loglist=self.logs[self.log_line_flag:self.log_line_flag+5]
            count=len(loglist)
            self.log_line=['','','','',''] #每次初始化，使没有内容的地方为空
            for i in range(count):
                self.log_line[i]=loglist[i]

        def _showHand(self):
            #手牌处理信息
            total=len(self.Game.handcard)   #获取当前总手牌数
            for i in range(len(self.Game.handcard)):
                _x,_y,_w,_h=self.calcHandCardPos(total,i)
                if not self.Game.handcard[i].Selected:          #如果没有被锁定选择
                    if i==self.MouseOnHandCard:                         #如果被鼠标指着
                        self.screen.blit(self.adjustmentObj(self._card[self.Game.handcard[i].getName()],self.NarrowRate),(_x,_y-40))    #提高手牌位置
                    else: 
                        self.screen.blit(self.adjustmentObj(self._card[self.Game.handcard[i].getName()],self.NarrowRate),(_x,_y))       #正常显示
                else:                                           #如果锁定选择
                    _select=pygame.transform.scale(self.selectback,(_w+10,_h+10))
                    self.screen.blit(_select,(_x-5,_y-45))        #显示选择背景
                    self.screen.blit(self.adjustmentObj(self._card[self.Game.handcard[i].getName()],self.NarrowRate),(_x,_y-40))
            
            # print(self.adjustmentObj(self._card["D10"],0.3).get_rect())
    
    def ShowCemetery(self):
        #显示墓地卡牌信息  点击显示
        pass
    
    def GameDefeat(self):
        #游戏失败动画阶段
        pass
    
    def GameVictory(self):
        #游戏胜利动画阶段
        pass
    


    def CardVerification(self,Card):
        #验证卡面是否符合规则
        if (Card[0] in ('C','D','S','H') and Card[1:] in ('A','2','3','4','5','6','7','8','9','10','J','Q','K')) or (Card[0] == 'J' and Card[1:] in ('0','1')):
            return True
        else:
            return False
        
    
class RuleClass():
    def __init__(self,root):
        self.root=root
        #事件常量
        self.tipsDisplay=pygame.USEREVENT+1    #小贴士显示事件
        self.stageSwitchDelay=pygame.USEREVENT+2    #阶段切换延迟事件
        self.bossDeathDelay=pygame.USEREVENT+3      #boss死亡延迟
        self.bossDeathDelayTime=1500                #延迟1500毫秒
        #初始化
        self.cardbox=[]     #所有卡组对象
        self.enemybox=[]    #敌人卡组对象
        self.cardpub=[]     #酒馆
        self.cemetery=[]    #墓地
        self.handcard=[]    #手牌
        self.jokerpos=[]    #鬼牌位置
        self.enemypos=[]    #敌人位置
        self.tablepos=[]    #桌面    一回合结束前，卡牌不会放到墓地，而是先放置到桌面
        self.moveout=[]     #移除游戏外
        self.cardObj={}     #卡牌对象
        #花色指示器
        self.DecorShow=[1,1,1,1]    #花色指示器显示状态   顺序为梅花，方块，黑桃，红桃
        #动作按钮状态
        self.ActiveButtonState=[0,0,0]  #动作按钮状态 顺序为出牌，弃牌，过牌  0为不可用，1为可用, 2为不合法，仅出牌过牌有不合法状态
        #设置各个敌人性能
        self.MaxHandCard=8  #一个玩家最大8张牌，两个玩家最大7张，三个玩家最大6张，四个玩家最大5张，最多四个玩家
        self.invalidDecor=None  #无效花色
        self.StageNum=0     #阶段(阶段1：出牌 阶段2：技能 阶段3：伤害 阶段4：反击) 分别对应0,1,2,3
        #手牌预选
        self.Preselection=[]
        #辅助显示
        self.assist_HP=''
        self.assist_ATK=''
        self.assist_pub=''
        self.assist_cemetery=''
        #BOSS顺位
        self.BossNum=-1  #第几个boss ,初始为-1，因为每次获取会+1
        #提示显示
        self.tipwords=''
        #计算值
        self.Damage=-1
        self.Defend=-1
        self.Draw=-1
        self.Revive=-1
        self.Double=-1
        #游戏胜负
        self.Lose=False
        self.Win=False
        #BOSS等待死亡
        self.WaitKill=False
        
    def init(self):
        #====初始化====#
        self.cardbox=[]     #所有卡组对象
        self.enemybox=[]    #敌人卡组对象
        self.cardpub=[]     #酒馆
        self.cemetery=[]    #墓地
        self.handcard=[]    #手牌
        self.jokerpos=[]    #鬼牌位置
        self.enemypos=[]    #敌人位置
        self.tablepos=[]    #桌面   一回合结束前，卡牌不会放到墓地，而是先放置到桌面
        self.moveout=[]     #移除游戏外
        self.cardObj={}     #卡牌对象
        #====初始化====#
        #花色指示器
        self.DecorShow=[1,1,1,1]    #花色指示器显示状态重置
        self.invalidDecor=None      #初始化无效花色
        self.StageNum=0             #初始化阶段
        #动作按钮状态
        self.ActiveButtonState=[0,0,0]  #动作按钮状态 顺序为出牌，弃牌，过牌  0为不可用，1为可用, 2为不合法，仅出牌过牌有不合法状态
        self.createCard()   #创建卡组
        self.cardInitPos()  #卡牌初始位置配置
        self.BossNum=-1      #boss顺序重置
        self.Preselection=[]    #预选手牌重置
        #辅助显示
        self.assist_HP=''
        self.assist_ATK=''
        self.assist_pub=''
        self.assist_cemetery=''
        #提示显示
        self.tipwords=''
        #计算值
        self.Damage=-1
        self.Defend=-1
        self.Draw=-1
        self.Revive=-1
        self.Double=-1
        #游戏胜负
        self.Lose=False
        self.Win=False
        #BOSS等待死亡
        self.WaitKill=False
        
    def clearAssist(self):
        #清空辅助显示
        self.assist_HP=''
        self.assist_ATK=''
        self.assist_pub=''
        self.assist_cemetery=''
        
    def log(self,words):
        #日志方法
        self.root.Table.log(words)

    def Run(self):
        #游戏流程推进
        #判断主逻辑
        self.run_CheckCardSelectLegal() #选择卡牌合法显示
        if self.StageNum == 0:
            self.Damage,self.Defend,self.Draw,self.Revive,self.Double=self.run_SelectedAuxiliaryDisplay() #辅助显示并输出计算值
        if self.StageNum == 1 and self.root.Table.StageSwitchState==False:
            self.clearAssist()
            self.run_SkillAction()  #发动技能效果
        if self.StageNum == 2 and self.root.Table.StageSwitchState==False:
            if self.WaitKill==False:
                self.run_AttackAction() #造成伤害
                self.BeatBossCheck()    #伤害判断
        if self.StageNum == 3:
            if self.BossDontAttck():
                self.root.Table.StageSwitch()   #切换阶段
            if self.checkLose():
                if self.Lose==False:
                    self.loseGame()     #判输
                    self.root.Enemy.ChangeStage(2)  #改变boss为攻击状态
                
    def BeatBossCheck(self):
        #判断是否打败BOSS，确认打败为击杀还是感化招募
        if self.BossHP <= 0:
            #改变boss显示及进度器显示
            if self.BossHP < 0:
                self.root.Enemy.ChangeStage(4)  #改变boss为死亡状态
                self.root.Table.EnemyListChange(self.BossNum,2,self.enemypos[0].getName())
            elif self.BossHP==0:
                self.root.Enemy.ChangeStage(3)  #改变boss为招募状态
                self.root.Table.EnemyListChange(self.BossNum,3,self.enemypos[0].getName())
            if self.WaitKill==False:
                self.WaitKill=True
                pygame.time.set_timer(self.bossDeathDelay,self.bossDeathDelayTime,1)  #设置定时器
        else:
            self.root.Table.StageSwitch()   #切换阶段

    def KillBoss(self):
        #移开boss并获取新boss
        if self.BossHP < 0:             #如果击杀
            self.removeBoss()    #移除游戏外
        elif self.BossHP==0:            #如果感化招募
            self.recruitBoss()     #移动到酒馆
        self.BossGet()                  #重新获取boss
        self.root.Enemy=self.root.EnemyClass(self.root,self.getCurBossName())         #获取敌人显示
        self.root.Table.StageSwitch(0)   #切换为初始阶段
        self.log('-----新的回合-----')
        
        if self.checkWin(): #检查是否胜利
            self.winGame()
        return
                
    def checkWin(self):
        #检查是否打败了所有boss，如果是则胜利
        if len(self.enemybox)==0:
            return True
        else:
            return False

    def winGame(self):
        #游戏判定赢
        self.log('你终于打败了所有BOSS,你赢了！')
        self.Win=True

    def checkLose(self):
        #检查手牌是否不够弃牌点数，是则判输
        Total_count=0
        for card in self.handcard:
            Total_count+=card.getCardValue()
        if Total_count < self.BossATK:
            return True
        else:
            return False
    def loseGame(self):
        #游戏判定输
        self.log('你已经没有能力阻挡BOSS的攻击了,你输了')
        self.Lose=True    
    
    def BossDontAttck(self):
        #boss是否没有攻击力，如果是则跳过弃牌阶段
        if self.BossATK==0:
            return True
        else:
            return False
    
    def TransCardName(self,cardName):
        #翻译卡牌名为汉字
        _dict={'C':'梅花','D':'方片','S':'黑桃','H':'红桃','J':'鬼牌'}
        _dict2={'A':'A','2':'二','3':'三','4':'四','5':'五','6':'六','7':'七','8':'八','9':'九','10':'十','J':'J','Q':'Q','K':'K'}
        spell=_dict[cardName[0]]
        if cardName[0]!='J':
            spell+=_dict2[cardName[1:]]
        return spell
        
    def run_SkillAction(self):
        #发动技能效果
        _str='你'
        if self.Double>-1:
            _str+='可以造成双倍的伤害,'
        if self.Defend>-1:
            _str+='降低了BOSS'+str(self.Defend)+'点攻击力,'
            self.BossATK-=self.Defend       #降低攻击力
        if self.Draw>-1:
            _str+='从酒馆抽取了'+str(self.Draw)+'张牌,'
            self.DrawCard(self.Draw)        #抽牌
        if self.Revive>-1:
            _str+='从墓地复活了'+str(self.Revive)+'张牌到酒馆,'
            self.reviveCard(self.Revive)    #复活
        if self.Defend + self.Draw + self.Revive + self.Double > -3:
            self.log('----激活技能----')
            self.log(_str[:-1])
        self.root.Table.StageSwitch()   #切换阶段
            
    def run_AttackAction(self):
        #造成伤害
        _str='你造成了'+str(self.Damage)+'点伤害'
        if self.Damage>-1:
            self.log('----造成伤害----')
            self.log(_str)
            self.BossHP-=self.Damage
        self.root.Enemy.ChangeStage(1)  #改变boss为被攻击状态
            
    
    def PlayOut(self):
        #出牌动作
        
        #日志输出
        _str=''
        for card in self.Preselection:
            _str+=self.TransCardName(card.getName())+','
        _str='你打出了:'+_str[:-1]

        self.log('------出牌------')
        self.log(_str)
        
        #动作执行
        usedCard=self.Preselection[:]   #获得一个预选手牌的镜像
        for card in usedCard:
            self.selectHandCard(card,False) #取消所有预选手牌的选择
            self.movePos(card,'ct')         #使用的牌移动到墓地
        
        self.root.Table.StageSwitch()   #切换阶段
        
        
    def DiscardAction(self):
        #弃牌动作
        
        #日志输出
        _str=''
        for card in self.Preselection:
            _str+=self.TransCardName(card.getName())+','
        _str='你丢弃了:'+_str[:-1]
        
        self.log('------弃牌------')
        self.log(_str)
        
        #动作执行
        usedCard=self.Preselection[:]   #获得一个预选手牌的镜像
        for card in usedCard:
            self.selectHandCard(card,False) #取消所有预选手牌的选择
            self.movePos(card,'ct')         #使用的牌移动到墓地
            
        self.root.Enemy.ChangeStage(2)  #改变boss为攻击状态
        self.root.Table.StageSwitch()   #切换阶段
        self.log('-----新的回合-----')
    
    def PassAction(self):
        #过牌动作
        self.log('------出牌------')
        self.log('你放弃了出牌')
        self.root.Table.StageSwitch()   #切换阶段
    
    def run_SelectedAuxiliaryDisplay(self):
        #选择卡牌辅助显示,同时输出伤害，防御，抽牌，复活的计算值
        
        #Decor:C(Club)=♣,D(Diamond)=♦,S(Spade)=♠,H(Heart)=♥,J(Joker)=Joker
        _DecorToPos={'C':0,'D':1,'S':2,'H':3}  
        DecorUse=[] #使用的花色
        point=0     #总计点数
        Damage=-1   #造成伤害
        Defend=-1   #防御减伤
        Draw=-1     #抽牌数
        Revive=-1   #复活数
        Double=-1   #是否双倍
        if self.ActiveButtonState[0]!=2:    #当预选手牌非不合法时
            for card in self.Preselection:
                point+=card.getCardValue()            #计算当前总点数
                _cardDecor=card.getCardDecor()      #获取当前卡的花色
                if _cardDecor!=self.invalidDecor:   #如果当前卡并非跟boss相同花色则加入可使用花色中
                    if _cardDecor not in DecorUse:
                        DecorUse.append(_cardDecor)
            #--恢复初始状态，并在下面的判断中动态改变--
            for i in range(4):
                self.DecorShow[i]=1 
            self.assist_HP=''
            self.assist_ATK=''
            self.assist_pub=''
            self.assist_cemetery=''
            #----
            Damage = point  #设置基础伤害
            self.assist_HP='-'+str(Damage)  #伤害初始显示辅助
            if 'C' in DecorUse:      #梅花
                Damage = point * 2   #伤害为双倍总点数
                Double = 1
                self.DecorShow[0]=2
                self.assist_HP='-'+str(point)+'x2'  #伤害显示辅助
            if 'D' in DecorUse:     #方片
                Draw = point        #抽卡数为总点数
                self.DecorShow[1]=2
                _Actual_Draw=8-len(self.handcard)+len(self.Preselection)
                if _Actual_Draw > len(self.cardpub):   #如果实际最大抽卡数比剩余卡数小，则改成剩余卡数
                    _Actual_Draw=len(self.cardpub)
                if _Actual_Draw >= Draw:    #如果实际最大抽卡数比预计抽卡数大或相等
                    self.assist_pub='←'+str(Draw)   #抽取抽卡数的卡
                else:                   #否则
                    self.assist_pub='←'+str(_Actual_Draw)+'('+str(Draw)+')' #只抽取实际最大抽卡数
                    Draw = _Actual_Draw  #修改实际抽卡数
            if 'S' in DecorUse:     #黑桃
                Defend = point      #减伤为总点数值
                self.DecorShow[2]=2
                if  Defend>self.BossATK:    #超过攻击力最大值就减少剩余攻击力
                    self.assist_ATK='-'+str(self.BossATK)
                    Defend = self.BossATK
                else:                       #否则减少减伤值
                    self.assist_ATK='-'+str(Defend)
            if 'H' in DecorUse:     #红桃
                Revive = point      #复活数为总点数
                self.DecorShow[3]=2
                if len(self.cemetery)+1>=Revive:  #墓地卡数量大于等于需复活卡时
                    self.assist_cemetery='♥'+str(Revive)       #复活对应数值的卡
                else:                           #否则
                    self.assist_cemetery='♥'+str(len(self.cemetery)+1)+'('+str(Revive)+')'   #复活能复活的所有卡
                    Revive = len(self.cemetery)+1
        else:   #预选牌不合法时
            #--恢复初始状态--
            for i in range(4):
                self.DecorShow[i]=1 
            self.clearAssist()
            #----
        
        self.DecorShow[_DecorToPos[self.invalidDecor]]=0    #设置指示器无效化显示
        return Damage,Defend,Draw,Revive,Double
    
    def run_CheckCardSelectLegal(self):
        #确认选择卡牌规则是否合法流程，修改显示状态
        if self.StageNum==0:    #出牌阶段
            ret,code=self.__checkplayselectlegal()
            if ret:   #出牌规则检测合法后
                self.chageButtonState(0,1)      #出牌按钮可用
            else:
                self.chageButtonState(0,2)      #出牌按钮不合法提示
            self.chageButtonState(1,0)      #弃牌按钮不可用
            self.chageButtonState(2,1)      #过牌按钮可用
            if code==-1:
                self.tipwords=''
            elif code==0:   #手牌未选择
                self.tipwords='你还没有选择要出的牌'
            elif code==1:   #组合牌大于10
                self.tipwords='你可以选择任意n张相同点数的牌,选择的牌除了与BOSS花色一致的花色效果会同时生效,但选择组合出牌时组合牌的总点数之和不能大于10点,组合牌不能连携组合点数以外的牌。'
            elif code==2:   #多张单独牌
                self.tipwords='选择了多张单独的牌,但没有构成任何连招,如:相同牌组合出牌、跟宠物连携出牌'
            elif code==3:   #有宠物，但是有其他多张牌
                self.tipwords='你选择了一张宠物牌(牌面为A的牌),但是没有构成连招的条件,宠物牌可以单独出,也可以跟任何一张单张牌一起连携出牌,或者直接将多张宠物牌作为相同组合牌出牌,但不能跟多张不同点数的牌一起出'
            elif code==4:   #其他未尽情况
                self.tipwords='你的出牌方式不符合规则,请认真阅读出牌规范'
        elif self.StageNum==1:    #技能阶段
            self.chageButtonState(0,0)      #出牌按钮不可用
            self.chageButtonState(1,0)      #弃牌按钮不可用
            self.chageButtonState(2,0)      #过牌按钮不可用
        elif self.StageNum==2:    #伤害阶段
            self.chageButtonState(0,0)      #出牌按钮不可用
            self.chageButtonState(1,0)      #弃牌按钮不可用
            self.chageButtonState(2,0)      #过牌按钮不可用
        elif self.StageNum==3:    #反击阶段
            self.chageButtonState(0,0)      #出牌按钮不可用
            self.chageButtonState(2,0)      #过牌按钮不可用
            ret,code=self.__checkdiscardselectlegal()
            if ret:
                self.chageButtonState(1,1)      #弃牌按钮可用
            else:
                self.chageButtonState(1,2)      #弃牌按钮不合法提示
            if code==-1:    #合法
                self.tipwords=''
            elif code==0:   #手牌未选择
                self.tipwords='你还没有选择该弃的牌'
            elif code==1:   #点数不够
                self.tipwords='你选择的牌点数值不够抵消当前BOSS的攻击'
                
    
    def __checkplayselectlegal(self):
        #出牌规则合法检测
        if len(self.Preselection)==0:
            return False,0        #如果预选牌为空直接不合法
        pets=[]     #宠物牌
        singe=[]    #单独牌
        couple=[]   #组合牌
        cardpoint=[]    #卡牌点数
        for card in self.Preselection:
            cardpoint.append(card.getCardValue())  #取出卡牌点数
        for i in cardpoint:
            if i==1:
                pets.append(i)
            if cardpoint.count(i)>1:
                couple.append(i)
            else:
                singe.append(i)
        if sum(couple)>10:      #如果组合出牌总点数大于10则不合法
            return False,1
        if len(couple)==0 and len(singe)>0: #如果没有组合出牌且有单独出牌
            if len(pets)==0:        #如果没有宠物
                if len(singe)>1:    #且单独牌数量超过一张
                    return False,2    #不合法
                else:               #没有宠物但是有单张牌
                    return True,-1     #合法
            else:                   #有宠物
                if len(singe)==2:   #算上宠物，单独牌有两张，既一张宠物一张任意单牌
                    return True,-1     #合法
                elif len(singe)==1 and singe[0]==1:  #如果只有一张宠物
                    return True,-1
                else:               #其他情况
                    return False,3    #不合法
        elif len(couple)>0 and len(singe)==0:   #只有组合牌，没有单独牌，且组合点数不大于10
            return True,-1             #合法
        else:                       #其余未尽情况
            return False,4            #皆不合法

    def __checkdiscardselectlegal(self):
        #弃牌选择合法判断
        if len(self.Preselection)==0:
            return False,0        #如果预选牌为空直接不合法
        count=0
        for card in self.Preselection:
            count+=card.getCardValue()  #计算预选点数
        if count>=self.BossATK:
            return True,-1          #弃牌合法
        else:
            return False,1          #选择卡牌总点数不足

    def chageButtonState(self,num,state):
        #改变出牌等按键状态，num为顺序，state为状态，0为不可用，1为可用
        assert num in [0,1,2]
        assert state in [0,1,2]
        self.ActiveButtonState[num]=state
    
    def recruitBoss(self):
        #招募boss到酒馆
        if len(self.enemypos)>0:
            for enemy in self.enemypos:
                self.movePos(enemy,'cp')    #移动到酒馆
        self.shuffle()  #将酒馆洗牌    
    
    def removeBoss(self):
        #移除boss
        if len(self.enemypos)>0:
            for enemy in self.enemypos:
                self.movePos(enemy,'mo')
    
    def getNewBoss(self):
        #抽取一个新的boss
        if len(self.enemybox)>0:
            self.popOut('eb','ep')
    
    def getCurBossName(self):
        #获取当前boss名
        return self.enemypos[0].getName()
    
    def selectHandCard(self,pokeObj,status):
        #选择及移除手牌预选状态
        if status:
            if pokeObj not in self.Preselection:
                pokeObj.Selected=True
                self.Preselection.append(pokeObj)
                return True
            else:
                return False
        else:
            if pokeObj in self.Preselection:
                pokeObj.Selected=False
                self.Preselection.remove(pokeObj)
                return True
            else:
                return False
        
        
    def BossGet(self):
        #Boss基础资源设置
        BossDict={'J':(10,20),'Q':(15,30),'K':(20,40)}  #(ATT,HP)
        self.getNewBoss()  #从敌人卡组对象中顺序抽取一张牌到场上敌方位置
        Card=self.enemypos[0]   #获取敌方卡牌信息
        _CardNumber=Card.getCardNumber()
        self.BossATK=BossDict[_CardNumber][0]
        self.BossHP=BossDict[_CardNumber][1]
        self.invalidDecor=Card.getCardDecor()   #设置无效花色
        self.BossNum+=1 #boss顺位变化
        self.root.Table.EnemyListChange(self.BossNum,1,Card.getName())  #boss顺序，状态（此处为1：正常显示态），卡名
        
    def cardInitPos(self):
        #分配卡牌初始位置
        self.enemybox=self.enemyRandomCreate()  #敌人卡牌 J，Q，K放入
        self.jokerInitPos() #鬼牌Joker放入
        self.pubInitPos()   #酒馆卡牌放入
        self.DrawCard()     #抽卡到手牌
        
    def getHandCardCount(self):
        #获取当前手牌数
        return len(self.handcard)
        
    def DrawCard(self,GetCount=None):
        #抽卡    GetCount抽卡数，如果为None则补满
        now_count = self.getHandCardCount()         #获取当前手牌数
        Max_Draw_count = self.MaxHandCard - now_count   #计算抽满的抽卡的数
        if GetCount==None:      #为NOne则补满
            Draw_count=Max_Draw_count
        else:
            if GetCount > Max_Draw_count:   #如果抽卡数比实际抽卡数大，只抽实际能抽的卡数量
                Draw_count=Max_Draw_count
            else:
                Draw_count=GetCount
        count=0
        for i in range(Draw_count):
            if len(self.cardpub)>0:         #如果酒馆没卡了，就能抽多少抽多少
                self.popOut('cp','hc')      #从酒馆顺序抽一张到手上
                count+=1 
            else:
                return count    #返回实际抽卡数
        return count
    
    def pubInitPos(self):
        #酒馆卡牌放置   既牌堆
        for i in self.cardbox:
            if i.getCardDecor()!='J' and i.getCardNumber() not in ('J','Q','K'):
                i.setPosition('cp') #设置卡牌到酒馆(牌堆)位置
                self.cardpub.append(i)
        self.shuffle()   #酒馆洗牌
        
    def jokerInitPos(self):
        #鬼牌位置放置  单人玩家单独放置鬼牌，多人玩家时，2玩家0鬼牌，3玩家1鬼牌，4玩家2鬼牌。只有单人玩家才放置鬼牌到鬼牌位置
        for i in self.cardbox:
            if i.getCardDecor()=='J':
                i.setPosition('jp') #设置卡牌到鬼牌位置
                self.jokerpos.append(i)
        
    def enemyRandomCreate(self):
        #打乱敌人顺序 最终优先输出打乱的J，打乱的Q，打乱的K，倒序pop，所以反过来
        result=[] #顺序最终是乱序的K，乱序的Q，乱序的J
        K=[]    #临时K列表
        Q=[]    #临时Q列表
        J=[]    #临时J列表
        for i in self.cardbox:
            if i.getCardNumber()=='K':
                i.setPosition('eb') #设置卡牌到敌人列表位置
                K.append(i)
            if i.getCardNumber()=='Q':
                i.setPosition('eb') #设置卡牌到敌人列表位置
                Q.append(i)
            if i.getCardNumber()=='J':
                i.setPosition('eb') #设置卡牌到敌人列表位置
                J.append(i)
        self.randomList(K)
        self.randomList(Q)
        self.randomList(J)
        for k in K:
            result.append(k)
        for q in Q:
            result.append(q)
        for j in J:
            result.append(j)
        return result 
        
    def shuffle(self):
        #酒馆卡牌洗牌
        self.randomList(self.cardpub)
    
    def randomList(self,aList):
        #随机打乱列表，可以用作洗牌
        random.shuffle(aList)
        
    def createCard(self):
        #创建卡组对象
        self.cardbox.append(Poker("J","0"))     #创建小王
        self.cardbox.append(Poker("J","1"))     #创建大王
        self.createCardShowObj("J0")    #创建卡对象
        self.createCardShowObj("J1")    #创建卡对象
        for i in ["C","D","S","H"]:             #创建其他卡牌
            for j in ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]:
                self.cardbox.append(Poker(i,j))
                self.createCardShowObj(i+j) #创建卡对象
                
    def createCardShowObj(self,Card):
        #创建卡牌默认显示对象
        self.cardObj[Card]=pygame.image.load(base_path+'resource\\cards\\'+Card+'.jpg')
        self.cardObj[Card]=pygame.transform.scale(self.cardObj[Card],(410,570))   #标准大小410x570

    def popOut(self,sourcePos,targetPos):
        #顺序抽取卡到某个位置
        #pos: eb(enemybox) , cp(cardpub) , ct(cemetery) , hc(handcard) , jp(jokerpos) , ep(enemypos)
        assert sourcePos in ('eb','cp','ct','hc','jp','ep','mo'),posValueError
        assert targetPos in ('eb','cp','ct','hc','jp','ep','mo'),posValueError
        if sourcePos=='mo':
            return False
        if sourcePos=='eb':
            Card=self.enemybox.pop()
        elif sourcePos=='cp':
            Card=self.cardpub.pop()
        elif sourcePos=='ct':
            Card=self.cemetery.pop()
        elif sourcePos=='hc':
            Card=self.handcard.pop()
        elif sourcePos=='jp':
            Card=self.jokerpos.pop()
        elif sourcePos=='ep':
            Card=self.enemypos.pop()
        elif sourcePos=='tp':
            Card=self.tablepos.pop()
        Card.setPosition(targetPos) #改变卡设定位置
        if targetPos=='eb':
            self.enemybox.append(Card)
        elif targetPos=='cp':
            self.cardpub.append(Card)
        elif targetPos=='ct':
            self.cemetery.append(Card)
        elif targetPos=='hc':
            self.handcard.append(Card)
        elif targetPos=='jp':
            self.jokerpos.append(Card)
        elif targetPos=='ep':
            self.enemypos.append(Card)
        elif targetPos=='tp':
            self.tablepos.append(Card)
        elif targetPos=='mo':
            self.moveout.append(Card)

    def reviveCard(self,count):
        #复活卡牌
        self.cemetery.reverse()
        for i in range(count):
            self.popOut('ct','cp')
        self.cemetery.reverse()
        self.shuffle()  #洗牌

    def movePos(self,Card,Pos):
        #移动卡牌位置
        #pos: eb(enemybox) , cp(cardpub) , ct(cemetery) , hc(handcard) , jp(jokerpos) , ep(enemypos)
        assert Pos in ('eb','cp','ct','hc','jp','ep','mo'),posValueError
        if Card.getPosition()==Pos:
            return False
        if Card.getPosition()=='mo':
            return False
        
        if Card.getPosition()=='eb':
            self.enemybox.remove(Card)
        elif Card.getPosition()=='cp':
            self.cardpub.remove(Card)
        elif Card.getPosition()=='ct':
            self.cemetery.remove(Card)
        elif Card.getPosition()=='hc':
            self.handcard.remove(Card)
        elif Card.getPosition()=='jp':
            self.jokerpos.remove(Card)
        elif Card.getPosition()=='ep':
            self.enemypos.remove(Card)
        elif Card.getPosition()=='tp':
            self.tablepos.remove(Card)
        Card.setPosition(Pos)
        if Pos=='eb':
            self.enemybox.append(Card)
        elif Pos=='cp':
            self.cardpub.append(Card)
        elif Pos=='ct':
            self.cemetery.append(Card)
        elif Pos=='hc':
            self.handcard.append(Card)
        elif Pos=='jp':
            self.jokerpos.append(Card)
        elif Pos=='ep':
            self.enemypos.append(Card)
        elif Pos=='tp':
            self.tablepos.append(Card)
        elif Pos=='mo':
            self.moveout.append(Card)
        return True
    

                
            
    

if __name__=='__main__':
    Game=GameDisplayer()
    Game.GameStart()