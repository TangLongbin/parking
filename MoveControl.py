import DriveMotor
import GetDistance
import time
import GetRpm_Angle

def GoStraight(Direction = 1,speed = 10,LorR = ' ',radius = 0):
    rpm = GetRpm_Angle.GetData('rpm', speed)
    angle = GetRpm_Angle.GetData(LorR, radius)
    if LorR == 'R':
        DriveMotor.TurnRight(angle)
    elif LorR == 'L':
        DriveMotor.TurnLeft(angle)
    elif LorR == ' ':
        DriveMotor.motorangle(90)
    else:
        return 0
    
    if Direction == 1:
        DriveMotor.GoForward(rpm)
    elif Direction == -1:
        DriveMotor.GoBack(rpm)
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
    GoStraight(1,20,'L',50)
    time.sleep(10)
    GoStraight(0)