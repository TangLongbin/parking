import csv
SpeedToRpm = {}
SpeedToRpm[0] = 0
RadiusToAngle_L = {}
RadiusToAngle_L[0] = 90
RadiusToAngle_R = {}
RadiusToAngle_R[0] = 90
Car_Width = 19.5

with open('SpeedData.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    rows = [row for row in reader]

for row in rows:
    SpeedToRpm[eval(row[0])] = eval(row[1])

with open('AngelData.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    rows = [row for row in reader]

for row in rows:
    if row[0] == 'L':
        RadiusToAngle_L[eval(row[1])] = eval(row[2])
    if row[0] == 'R':
        RadiusToAngle_R[eval(row[1])] = eval(row[2])


def GoodRpm(Exp = 0):
    MinRpm = 0
    MinSpeed = 0
    MaxRpm = 0
    MaxSpeed = 0
    for speed in SpeedToRpm:
        if speed >= Exp:
            MaxRpm = SpeedToRpm[speed]
            MaxSpeed = speed
            break
        MinRpm = SpeedToRpm[speed]
        MinSpeed = speed

    return int((((Exp - MinSpeed) * (MaxRpm - MinRpm)) / (MaxSpeed - MinSpeed)) + MinRpm)

def GoodAngle_L(Exp = 0):
    MinRadius = 0
    MaxRadius = 0
    MinAngle = 0
    MaxAngle = 0
    for radius in RadiusToAngle_L:
        if radius <= Exp:
            MinRadius = radius
            MinAngle = RadiusToAngle_L[radius]
            break
        MaxRadius = radius
        MaxAngle = RadiusToAngle_L[radius]
    
    return int((((MaxRadius - Exp) * (MaxAngle - MinAngle)) / (MaxRadius - MinRadius)) + MinAngle)
    
def GoodAngle_R(Exp = 0):
    MinRadius = 0
    MaxRadius = 0
    MinAngle = 0
    MaxAngle = 0
    for radius in RadiusToAngle_R:
        if radius <= Exp:
            MinRadius = radius
            MinAngle = RadiusToAngle_R[radius]
            break
        MaxRadius = radius
        MaxAngle = RadiusToAngle_R[radius]
    
    return int((((MaxRadius - Exp) * (MaxAngle - MinAngle)) / (MaxRadius - MinRadius)) + MinAngle)

def GetData(Type, Exp):
    if Type == "rpm" or Type == "RPM":
        return GoodRpm(Exp)
    if Type == "L" or Type == "l":
        return GoodAngle_L(Exp)
    if Type == "R" or Type == 'r':
        return GoodAngle_R(Exp)
