import random
import machine
from machine import Pin,I2C,ADC
import ssd1306
from time import sleep
import framebuf
class tanchishe(object):
    def __init__(self,oled):
        self.p12=Pin(12,Pin.OUT,value=1)
        self.w=8
        self.h=8
        self.st=8
        self.a1=ADC(Pin(35))
        self.a2=ADC(Pin(34))
        self.game_status="play"
        self.base_x=20
        self.base_y=20
        self.snoke=[[10,10],[20,10],[30,10]]
        self.by="right"
        self.oled=oled
        self.oled.fill(0)
        self.oled.rect(0,0,128,64,1)
        self.oled.fill_rect(self.snoke[0][0],self.snoke[0][1],self.w,self.h,1)
        self.oled.fill_rect(self.snoke[1][0],self.snoke[1][1],self.w,self.h,1)
        self.oled.fill_rect(self.snoke[2][0],self.snoke[2][1],self.w,self.h,1)
        self.oled.show()

    def begin(self):
      #初始化
      self.game_status="play"
      self.base_x=20
      self.base_y=20
      self.snoke=[[10,10],[20,10],[30,10]]
      self.by="right"
      self.level=1
    def suiji(self):
      #生成随机坐标
      self.base_x = random.randint(10,100)
      self.base_y = random.randint(10,50)

    def over(self):
      #结束
      self.oled.fill(0)
      self.oled.text('game over',25,25)
      self.oled.show()

    def base(self):
      #生成食物
      self.oled.text('*',self.base_x,self.base_y)
      self.oled.rect(0,0,128,64,1)
    def check(self):
      #检测
      if (abs(self.base_x-self.snoke[0][0]))<=4 and (abs(self.base_y-self.snoke[0][1]))<=4:
        if self.by=="up":
          new=[self.snoke[-1][0],self.snoke[-1][1]+self.st]
          self.snoke.append(new)
          self.suiji()
        if self.by=="down":
            new=[self.snoke[-1][0],self.snoke[-1][1]-self.st]
            self.snoke.append(new)
            self.suiji()
        if self.by=="left":
            new=[self.snoke[-1][0]+self.st,self.snoke[-1][1]]
            self.snoke.append(new)
            self.suiji()
        if self.by=="right":
            new=[self.snoke[-1][0]-self.st,self.snoke[-1][1]]
            self.snoke.append(new)
            self.suiji()

      for x ,y in self.snoke:
        if x >128 or x <0 or y>64 or y<0:
          self.game_status="over"

    def right(self):
      self.oled.fill(0)
      self.base()
      new=[self.snoke[0][0]+self.st,self.snoke[0][1]]
      self.snoke.insert(0,new)
      self.snoke.pop()
      for x in range(len(self.snoke)):
        self.oled.fill_rect(self.snoke[x][0],self.snoke[x][1],self.w,self.h,1)
      self.oled.show()

    def up(self):
      self.oled.fill(0)
      self.base()
      new=[self.snoke[0][0],self.snoke[0][1]-self.st]
      self.snoke.insert(0,new)
      self.snoke.pop()
      for x in range(len(self.snoke)):
        self.oled.fill_rect(self.snoke[x][0],self.snoke[x][1],self.w,self.h,1)
      self.oled.show()


    def down(self):
      self.oled.fill(0)
      self.base()
      new=[self.snoke[0][0],self.snoke[0][1]+self.st]
      self.snoke.insert(0,new)
      self.snoke.pop()
      for x in range(len(self.snoke)):
        self.oled.fill_rect(self.snoke[x][0],self.snoke[x][1],self.w,self.h,1)
      self.oled.show()
    def left(self):
      self.oled.fill(0)
      self.base()
      new=[self.snoke[0][0]-self.st,self.snoke[0][1]]
      self.snoke.insert(0,new)
      self.snoke.pop()
      for x in range(len(self.snoke)):
        self.oled.fill_rect(self.snoke[x][0],self.snoke[x][1],self.w,self.h,1)
      self.oled.show()


    def test(self):
      x=self.a1.read()
      y=self.a2.read()
      if x==0:
        if self.by=="down":
          self.game_status="over"
        self.by="up"
      elif x==4095:
        if self.by=="up":
          self.game_status="over"
        self.by="down"
      elif y==0:
        if self.by=="left":
          self.game_status="over"
        self.by="right"
      elif y==4095:
        if self.by=="right":
          self.game_status="over"
        self.by="left"
    def main(self):
        while 1:
          if self.game_status=="play":
            self.check()
            self.test()
            if self.by=="right":
              self.right()
            elif self.by=="left":
              self.left()
            elif self.by=="up":
              self.up()
            elif self.by=="down":
              self.down()
            if len(self.snoke)<=10:
              sleep(0.5)
            if len(self.snoke)>10 and len(self.snoke)<=15:
              sleep(0.4)
            if len(self.snoke)>15 and len(self.snoke)<=20:
              sleep(0.3)
            if len(self.snoke)>20 and len(self.snoke)<=25:
              sleep(0.2)
            if len(self.snoke)>25 and len(self.snoke)<=30:
              sleep(0.1)
            #print('snoke:%s'%snoke)
            #print('base:%s,%s' %(base_x,base_y))
          if self.game_status=="over":
            self.over()
            sleep(5)
            self.begin()