import openpyxl
workbook = openpyxl.load_workbook(filename="SpeedData.xlsx", read_only=True)
sheet1 = workbook["Sheet1"]
sheet2 = workbook["Sheet2"]
SpeedToRpm = {}
SpeedToRpm[0] = 0
RadiusToAngle_L = {}
RadiusToAngle_L[0] = 90
RadiusToAngle_R = {}
RadiusToAngle_R[0] = 90
row_index = 0
V = 0
R = 0

for row in sheet1.rows:
    row_index += 1

    if row_index == 1:
        continue

    V += row[1].value / row[2].value

    if row_index % 3 == 1:
        V /= 3.00
        SpeedToRpm[V] = row[0].value
        V = 0
    else:
        continue

row_index = 0
Car_Width = 19.5

for row in sheet2.rows:
    row_index += 1

    if row_index == 1:
        continue

    R += (row[2].value  + Car_Width) / 2
    if row_index % 3 == 1:
        R /= 3.00
        if row[0].value == 'L':
            RadiusToAngle_L[R] = row[1].value
        if row[0].value == 'R':
            RadiusToAngle_R[R] = row[1].value
        R = 0
    else:
        continue

workbook.close()

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
