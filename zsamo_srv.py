import pyads
import socket
import sys
import configparser
import BckhMotor
import argparse





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



#Motor dictionary
mot_dict = {}                                #motor dictionary: tartalmazza a motor száma - motor objektum párosokat
for i in config.sections():            #végigemegyünk minden key-en az ini file-ban
    if "BCKHFF_MO" in config[i]['type']:            #ellenörzi hogy motor e amit kiolvasunk az ini file-ból
        mn = config[i]                 #motor name
        mot_dict[i] = BckhMotor.BckhMotor(plc, mn['MotNum'], mn['unit'], mn['AbsoluteEnc'],
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
        motor_name = data
        if not data: break

        #data elejének kezelése: move/getPos eltávolítása, elmentése
        move = False
        getPos = False
        if data.startswith('move'):
            data = data.replace('move ',"")
            move = True
        elif data.startswith('getPos'):
            data = data.replace('getPos ', '')
            getPos = True
        
        #parser létrehozása
        parser = argparse.ArgumentParser()
        parser.add_argument('-a','--axisName' ,help = 'A tengely nevét kéri.')
        parser.add_argument('-t','--targetPos', type = int, help = 'A tengely új helyét kéri.')
        parser.add_argument('-mo','--movingOne', help = 'Lekéri egy tengely mozgásállaptát.')
        parser.add_argument('-ma','--movingAll', action="store_true", help = 'Lekéri az összes tengely mozgásállaptát.')
        args = parser.parse_args(data.split())

        #Lekéri ehy adott tengely állását.
        if getPos:
            conn.sendall(mot_dict[args.axisName].getPosition().encode('ascii'))

        #Adott pozícióba állítja a tengelyt.
        if move:
            if mot_dict[args.axisName].move(args.targetPos):
                conn.sendall('ACK;'.encode('ascii'))
        
        #Lekéri egy tengely mozgásállaptát.
        if args.movingOne:
            if mot_dict[args.movingAx].moving:
                conn.sendall('The {} axis is moving'.format(args.movingAx).encode('ascii'))
            else:
                conn.sendall('The {} axis is not moving'.format(args.movingAx).encode('ascii'))
        
        #Lekéri az összes tengely mozgásállaptát.            
        if args.movingAll:
            reply='Moving axis: '
            for nev in mot_dict.keys:
                if mot_dict[nev].moving:
                    reply += nev + ', '
            if reply == 'Moving axis: ': #ellenörzés: ha minden tengely áll
                reply = 'There are no moving axis.'
                conn.sendall(reply.encode('ascii'))
            else: conn.sendall(reply[0:-2].encode('ascii'))

    
plc.close()
