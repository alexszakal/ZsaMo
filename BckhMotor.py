# -*- coding: utf-8 -*-
#Motor class for the Beckhoff PLC motors
import math #-> for testing math.isnan(x)
import pyads

class BckhMotor:
    #Constructor of Class
    def __init__(self, plc, mn,
                 MotNum, # [int] Number of motor in PLC
                 unit,   # [string] Unit 
                 AbsEnc, # [bool] is it absolute?
                 SLimLow=float("-inf"), SLimHigh=float("inf"), #Soft limits
                 Speed=-1.0, Acc=-1.0, Dec=-1.0, BckLash=0.0):
        self.plc = plc
        self.mn = mn
        self.MotNum = MotNum
        self.unit = unit
        self.AbsEnc = AbsEnc
        self.SLimHigh = SLimHigh
        self.SLimLow = SLimLow
        self.Speed = Speed
        self.Acc = Acc
        self.Dec = Dec
        self.BckLash = BckLash

        plc.write_by_name(f'GVL.axes[{self.MotNum}].control.bEnable', True, pyads.PLCTYPE_BOOL)
        if Speed>0:
            plc.write_by_name(f'GVL.axes[{self.MotNum}].config.fVelocity', Speed, pyads.PLCTYPE_LREAL)
        if Acc>0:
            plc.write_by_name(f'GVL.axes[{self.MotNum}].config.fAcceleration', Acc, pyads.PLCTYPE_LREAL)
        if Dec>0:
            plc.write_by_name('GVL.axes[{self.MotNum}].config.fDeceleration', Dec, pyads.PLCTYPE_LREAL)
            
        plc.write_by_name("GVL.axes[1].control.eCommand", 0, pyads.PLCTYPE_INT) #???
        pass
 
    
    def getPosition(self,data):
        if data == "V1,Status":
            reply = 'V1,'
            reply += str(self.plc.read_by_name("GVL.axes[1].status.bBusy", pyads.PLCTYPE_BOOL))
            reply += ','
            reply += str(self.lc.read_by_name("GVL.axes[1].status.nErrorID", pyads.PLCTYPE_UDINT))
            reply += ','
            reply += "{:.2f}".format(self.plc.read_by_name("GVL.axes[1].status.fActPosition", pyads.PLCTYPE_LREAL))
            reply += ','
            reply += str(self.plc.read_by_name("GVL.axes[1].config.fPosition", pyads.PLCTYPE_LREAL))
            reply += ';'
            conn.sendall(reply.encode('ascii'))
        pass
    
    def move(self,targetPos):
        tmp=data.split(',')
        self.plc.write_by_name(f'GVL.axes[{self.MotNum}].config.fPosition', float(tmp[1]), pyads.PLCTYPE_LREAL)
        self.plc.write_by_name(f'GVL.axes[{self.MotNum}].control.bExecute', True, pyads.PLCTYPE_BOOL)
        conn.sendall('ACK;'.encode('ascii'))
        pass
    
    
    

