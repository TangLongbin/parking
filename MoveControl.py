import DriveMotor
import GetDistance
import time

def GoStraight(Direction = 1,rmp = 10,LorR = ' ',angle = 0):
    if LorR == 'R':
        DriveMotor.TurnRight(angle)
    elif LorR == 'L':
        DriveMotor.TurnLeft(angle)
    elif LorR == ' ':
        DriveMotor.motorangle(90)
    else:
        return 0
    
    if Direction == 1:
        DriveMotor.GoForward(rmp)
    elif Direction == -1:
        DriveMotor.GoBack(rmp)
    elif Direction == 0:
        DriveMotor.Rest()
    else:
        return 0
    return 1

def Check():
    GoStraight(1)
    DriveMotor.sleep(1)
    DriveMotor.motorangle(180)
    DriveMotor.sleep(1)
    DriveMotor.motorangle(0)
    DriveMotor.sleep(1)
    DriveMotor.Rest()
    return 1

if __name__ == '__main__':
    # Check()
    GoStraight(1,1000,'L',30)
    time.sleep(10)
    GoStraight(0)