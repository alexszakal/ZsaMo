import pyads
import socket
import sys
import configparser
import BckhMotor


config = configparser.ConfigParser()
config.read('conf.ini')                          #conf.ini beolvasása

#ZSAMO Server config
HOST = config['ZSAMO_SERVER']['IP']              # Symbolic name meaning all available interfaces
PORT = config['ZSAMO_SERVER']['port']            # Arbitrary non-privileged port

ADSaddr = config['ADS_COMMUNICATION']['ADSaddr']  
ADSport = int(config['ADS_COMMUNICATION']['ADSport'])

#Initialize PLC
plc = pyads.Connection(ADSaddr, ADSport)
plc.open()

#Motor config
md = {}                                #motor dictionary: tartalmazza a motor száma - motor objektum párosokat
for i in config.sections():            #végigemegyünk minden key-en az ini file-ban
    if 'type' in config[i]:            #ellenörzi hogy motor e amit kiolvasunk az ini file-ból
        mn = config[i]                 #motor number
        md[mn['MotNum']] = BckhMotor.BckhMotor(plc, mn, mn['MotNum'], mn['unit'], mn['AbsoluteEnc'],
                                               mn['SoftLimitLow'],mn['SoftLimitHigh'], mn['Speed'],
                                               mn['Acceleration'],mn['Deceleration'], mn['Backlash'])



#Plc-be irom GVL- könyvtárba
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)

    



while 1:
    conn, addr = s.accept()
    print ('Connected by'+ addr[0])
    while 1:
        #conn, addr = s.accept()
        #print ('Connected by'+ addr[0])
        tmpdata = conn.recv(1024)
        data = tmpdata.decode('ascii')
        if not data: break

        print(data)
        
        if data == "V1,Status":
            reply = 'V1,'
            reply += str(plc.read_by_name("GVL.axes[1].status.bBusy", pyads.PLCTYPE_BOOL))
            reply += ','
            reply += str(plc.read_by_name("GVL.axes[1].status.nErrorID", pyads.PLCTYPE_UDINT))
            reply += ','
            reply += "{:.2f}".format(plc.read_by_name("GVL.axes[1].status.fActPosition", pyads.PLCTYPE_LREAL))
            reply += ','
            reply += str(plc.read_by_name("GVL.axes[1].config.fPosition", pyads.PLCTYPE_LREAL))
            reply += ';'
            conn.sendall(reply.encode('ascii'))
        else:
            tmp=data.split(',')
            plc.write_by_name("GVL.axes[1].config.fPosition", float(tmp[1]), pyads.PLCTYPE_LREAL)
            plc.write_by_name("GVL.axes[1].control.bExecute", True, pyads.PLCTYPE_BOOL)
            conn.sendall('ACK;'.encode('ascii'))
    
plc.close()
