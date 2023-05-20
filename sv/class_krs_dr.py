#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Kondo KRS servo control program
# 2023.5.10
# by T.Nishimura @AiRRC
#---------------------------------
#
import serial
import time
#
class KRSdriver():
  def __init__(self):
    # initialize
    self.buf2=bytearray(2)
    self.buf3=bytearray(3)
    self.buf4=bytearray(4)
    self.buf6=bytearray(6)
    self.buf8=bytearray(8)
    self.temp_=bytearray(2)
    # set serial
    self.con = serial.Serial('/dev/ttySC2',650000)
    self.con.bytesize=8
    self.con.parity=serial.PARITY_EVEN
    self.con.stopbits=1
    self.con.timeout=0.1
    self.con.setDTR(False) 

    try:
      print(self.con)
    except:
      try:
        self.con.open()
        print ("comm: opened")
      except:
        print ("comm:Port erorr")
        sys.exit()

  def conclose(self):
    self.con.close()
#
# set free
  def set_free(self,sid):
    self.set_angle_sl(sid,0)
#
# set angle (slave mode)
  def set_angle_sl(self,sid,tangle):

    if tangle==0:
      tangle=0
    elif(tangle>11500):
      tangle=11500
      print ("over angle ",sid)
    elif(tangle<3500 ):
      tangle=3500
      print ("under angle ",sid)

    cmd1=sid&0x1f
    cmd=0x80+cmd1
    self.buf3[0]=cmd  #cmd+id
    self.buf3[1]=(tangle>>7)&0x7f
    self.buf3[2]=tangle&0x7f
    self.con.write(self.buf3)
#
# set and read angle
  def set_angle(self,sid,tangle):

    if tangle==0:
      tangle=0
    elif(tangle>11500):
      tangle=11500
    elif(tangle<3500 ):
      tangle=3500

    cmd1=sid&0x1f
    cmd=0x80+cmd1
    self.buf3[0]=cmd #cmd+id
    self.buf3[1]=(tangle>>7)&0x7f
    self.buf3[2]=tangle&0x7f
    self.con.write(self.buf3)
    buf_read=self.con.read(3)
    if (len(buf_read)==3):
      self.temp_[0]=int(buf_read[1])
      self.temp_[1]=int(buf_read[2])
      val=self.temp_[1]|(self.temp_[0]<<7)
      return(val)
    else:
      print ("angle read error")
      return(0)
#
#read_angle
  def read_angle(self,sid):
    cmd1=sid&0x1f 
    cmd=0xA0+cmd1
    self.buf2[0]=cmd #cmd+id
    self.buf2[1]=0x05 #angle
    self.con.write(self.buf2)
    buf_read=self.con.read(4)
    if (len(buf_read)==4):
      self.temp_[0]=int(buf_read[2])
      self.temp_[1]=int(buf_read[3])
      val=self.temp_[1]|(self.temp_[0]<<7)
      return(val)
    else:
      print ("read position error")
      return(0)
#
#---------------------------------
def main():
  print('Started')
  krs=KRSdriver()
  sid=1
  a=2500
#
  print (krs.read_angle(sid))
  time.sleep(1)
  print (krs.set_angle(sid,7500+a))
  time.sleep(1)
  print (krs.set_angle(sid,7500-a))
  time.sleep(1)
  print (krs.read_angle(sid))
  krs.conclose()
#---------------------------------
if __name__ == '__main__':
    main()
