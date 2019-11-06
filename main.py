import serial
import time
import threading

es920lr = None

loraRxData = ''
loraInitFalg = False
passFlag = False

rxPanID = ''
srcid = ''
dstid = ''
length = ''
rssi = ''
data = None

deviceInfo = []

def test01TH(ser):
    global loraRxData
    global loraInitFalg
    global passFlag
    global rxPanID
    global srcid
    global dstid
    global length
    global rssi
    global data

    print("Plesas Device Restart...")
    while True:
        time.sleep(1)
        if ser.readable():
            while ser.readable():
                loraRxData = ser.readline()
                # print(loraRxData)
                # b'\r Configuration Mode\n'
                # if loraRxData == b'\r ?. help        help\n':
                if loraRxData == b'\r Configuration Mode\n':
                    loraInitFalg = True
                elif b'--> receive data info' in loraRxData:
                    t1 = str(loraRxData).split("panid = ")
                    t2 = t1[1].split(', srcid = ')
                    t3 = t2[1].split(', dstid = ')
                    t4 = t3[1].split(', length = ')
                    t5 = t4[1].split(']')
                    rxPanID = t2[0]
                    srcid = t3[0]
                    dstid = t4[0]
                    length = t5[0]

                elif b'Receive Data' in loraRxData:
                    a1 = loraRxData.split(b'Data(')
                    a2 = a1[1].split(b')\r\n')
                    a3 = str(a1[0]).split('RSSI(')
                    a4 = a3[1].split('):PAN')
                    rssi = a4[0]
                    data = a2[0]
                    print(rssi, ' ', rxPanID, ' ', srcid, ' ', dstid, ' ', length, ' ', data.hex())

def test02TH(ser):
    global loraRxData
    global loraInitFalg
    global passFlag
    global initTHFlag

    initTHFlag = True
    while initTHFlag:
        time.sleep(1)
        if (loraRxData == b'Select Mode [1.terminal or 2.processor]\r\n'):
            ser.write(bytes('1\r\n', encoding='ascii'))
            loraRxData = ''

        if loraInitFalg == True:
            time.sleep(1)
            print("init Start...")
            ser.write(bytes('a\r\n', encoding='ascii'))
            time.sleep(0.3)
            ser.write(bytes('1\r\n', encoding='ascii'))
            time.sleep(0.3)
            ser.write(bytes('d\r\n', encoding='ascii'))
            time.sleep(0.3)
            ser.write(bytes(deviceInfo[0] + '\r\n', encoding='ascii'))
            time.sleep(0.3)
            ser.write(bytes('e\r\n', encoding='ascii'))
            time.sleep(0.3)
            ser.write(bytes(deviceInfo[1] + '\r\n', encoding='ascii'))
            time.sleep(0.3)
            ser.write(bytes('f\r\n', encoding='ascii'))
            time.sleep(0.3)
            ser.write(bytes(deviceInfo[2] + '\r\n', encoding='ascii'))
            time.sleep(0.3)
            ser.write(bytes('o\r\n', encoding='ascii'))
            time.sleep(0.3)
            ser.write(bytes('1\r\n', encoding='ascii'))
            time.sleep(0.3)
            ser.write(bytes('p\r\n', encoding='ascii'))
            time.sleep(0.3)
            ser.write(bytes('1\r\n', encoding='ascii'))
            time.sleep(0.3)
            ser.write(bytes('z\r\n', encoding='ascii'))
            loraInitFalg = False
            print('init Done...')

if __name__ == "__main__":

    deviceInfo.append(input("please set channel (1 - 5) > "))
    deviceInfo.append(input("please set PAN ID (0001 - FFFE) > "))
    deviceInfo.append(input("please set Own Node ID (000000 - FFFFFE) > "))
    deviceInfo.append(input("please set COM Port (COM1 - xx) > "))
    es920lr = serial.Serial(deviceInfo[3], 115200)
    threading.Thread(target=test01TH, args=(es920lr,)).start()
    threading.Thread(target=test02TH, args=(es920lr,)).start()
