# -*- coding: utf-8 -*-
#Motor class for the Beckhoff PLC motors
import math #-> for testing math.isnan(x)
import pyads

class BckhMotor:
    #Constructor of Class
    def __init__(self, plc,
                 MotNum, # [int] Number of motor in PLC
                 unit,   # [string] Unit 
                 AbsEnc, # [bool] is it absolute?
                 SLimLow=float("-inf"), SLimHigh=float("inf"), #Soft limits
                 Speed=-1.0, Acc=-1.0, Dec=-1.0, BckLash=0.0):
        self.plc = plc
        self.MotNum = MotNum
        self.unit = unit
        self.AbsEnc = AbsEnc
        self.SLimHigh = SLimHigh
        self.SLimLow = SLimLow
        self.Speed = Speed
        self.Acc = Acc
        self.Dec = Dec
        self.BckLash = BckLash

        plc.write_by_name("GVL.axes[{}].control.bEnable".format(self.MotNum), True, pyads.PLCTYPE_BOOL)
        
        if Speed>0:
            plc.write_by_name("GVL.axes[{}].config.fVelocity".format(self.MotNum), Speed, pyads.PLCTYPE_LREAL)
        else:
            self.Speed = plc.read_by_name("GVL.axes[{}].config.fVelocity".format(self.MotNum), pyads.PLCTYPE_LREAL)
            
        if Acc>0:
            plc.write_by_name("GVL.axes[{}].config.fAcceleration".format(self.MotNum), Acc, pyads.PLCTYPE_LREAL)
        else:
            self.Acc = plc.read_by_name("GVL.axes[{}].config.fAcceleration".format(self.MotNum), pyads.PLCTYPE_LREAL)
               
        if Dec>0:
            plc.write_by_name("GVL.axes[{}].config.fDeceleration".format(self.MotNum), Dec, pyads.PLCTYPE_LREAL)
        else:
            self.Dec = plc.read_by_name("GVL.axes[{}].config.fDeceleration".format(self.MotNum), pyads.PLCTYPE_LREAL)
            
   
        plc.write_by_name("GVL.axes[{}].control.eCommand".format(self.MotNum), 0, pyads.PLCTYPE_INT) #???
        pass
 
    
    def getPosition(self):
        reply = 'V1,'
        reply += str(self.plc.read_by_name("GVL.axes[{}].status.bBusy".format(self.MotNum), pyads.PLCTYPE_BOOL))
        reply += ','
        reply += str(self.lc.read_by_name("GVL.axes[{}].status.nErrorID".format(self.MotNum), pyads.PLCTYPE_UDINT))
        reply += ','
        reply += "{:.2f}".format(self.plc.read_by_name("GVL.axes[{}].status.fActPosition".format(self.MotNum), pyads.PLCTYPE_LREAL))
        reply += ','
        reply += str(self.plc.read_by_name("GVL.axes[{}].config.fPosition".format(self.MotNum), pyads.PLCTYPE_LREAL))
        reply += ';'
        return reply
        pass
    
    def move(self,targetPos):
        self.plc.write_by_name("GVL.axes[{}].config.fPosition".format(self.MotNum), float(targetPos), pyads.PLCTYPE_LREAL)
        self.plc.write_by_name("GVL.axes[{}].control.bExecute".format(self.MotNum), True, pyads.PLCTYPE_BOOL)
        return True #with v1
        pass
    
    def moving(self):
        return self.plc.read_by_name("GVL.axes[{}].status.bBusy".format(self.MotNum), pyads.PLCTYPE_BOOL)
        
    
    
    

