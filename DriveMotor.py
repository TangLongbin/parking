import serial
from time import sleep

ser = serial.Serial("/dev/ttyAMA0",115200,timeout=0.5)
buf = bytearray(10)
read_buf = bytearray(10)  
read_angle_real = 0       #the real position(angle) of steering engine
read_angle = 0            #the position(angle) which is set last time
time = 100                #the time which is required for steering engine to move once

def checksum(buf):
    sum = 0
    for x in range(2,8):
        sum += buf[x]
    return (sum % 256)

def motorleft(rpm):
    buf[0] = 0xFA
    buf[1] = 0xAF
    buf[2] = 0x02
    buf[3] = 0x01
    if rpm < 0:
        buf[4] = 0xFE
        if rpm < -65535:
            buf[6] = 0xFF
            buf[7] = 0xFF
        else:
            buf[6] = (-rpm) // 256
            buf[7] = (-rpm) % 256
    else:
        buf[4] = 0xFD
        if rpm > 65535:
            buf[6] = 0xFF
            buf[7] = 0xFF
        else:
            buf[6] = rpm // 256
            buf[7] = rpm % 256
    buf[5] = 0x00
    buf[8] = checksum(buf)
    buf[9] = 0xED
    ser.write(buf)
    if __name__ == '__main__':
        print(buf)
    return 1

def motorright(rpm):
    buf[0] = 0xFA
    buf[1] = 0xAF
    buf[2] = 0x03
    buf[3] = 0x01
    if rpm < 0:
        buf[4] = 0xFD
        if rpm < -65535:
            buf[6] = 0xFF
            buf[7] = 0xFF
        else:
            buf[6] = (-rpm) // 256
            buf[7] = (-rpm) % 256
    else:
        buf[4] = 0xFE
        if rpm > 65535:
            buf[6] = 0xFF
            buf[7] = 0xFF
        else:
            buf[6] = rpm // 256
            buf[7] = rpm % 256
    buf[5] = 0x00
    buf[8] = checksum(buf)
    buf[9] = 0xED
    ser.write(buf)
    if __name__ == '__main__':
        print(buf)
    return 1

def motorangle(angle):
    correct = -10  # Adjust the angle
    angle = angle + correct
    if angle < 10:
        angle = 10
    if angle > 170:
        angle = 170
    buf[0] = 0xFA
    buf[1] = 0xAF
    buf[2] = 0x01
    buf[3] = 0x01
    buf[4] = angle
    buf[5] = time // 20
    buf[6] = 0x00
    buf[7] = time // 20
    buf[8] = checksum(buf)
    buf[9] = 0xED
    ser.write(buf)
    if __name__ == '__main__':
        print(buf)
    return 1


#Need Fix
def motorread():
    buf[0] = 0xFA
    buf[1] = 0xAF
    buf[2] = 0x01
    buf[3] = 0x02
    buf[4] = 0x00
    buf[5] = 0x00
    buf[6] = 0x00
    buf[7] = 0x00
    buf[8] = checksum(buf)
    buf[9] = 0xED
    ser.write(buf)
    read_buf = ser.read(10)
    if ((read_buf[0]==0xFA)and(read_buf[1]==0xAF)and(read_buf[2]==0x01)and(read_buf[8]==checksum(read_buf))and(read_buf[9]==0xED)):
        read_angle = read_buf[4]*256 + read_buf[5]
        read_angle_real = read_buf[6]*256 + read_buf[7]
        for x in range(0,10):
            read_buf[x] = 0x00
        return 1
    else:
        return -1
    
def GoForward(rmp):
    motorright(rmp)
    motorleft(rmp)
    return 1

def GoBack(rmp):
    motorright(-rmp)
    motorleft(-rmp)
    return 1

def Rest():
    motorright(0)
    motorleft(0)
    motorangle(90)
    return 1

def TurnRight(angle):
    angle = 90 - angle
    motorangle(angle)
    return 1


def TurnLeft(angle):
    angle = angle + 90
    motorangle(angle)
    return 1

if __name__ == '__main__':
    Rest()
