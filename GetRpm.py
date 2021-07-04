import openpyxl
workbook = openpyxl.load_workbook(filename="SpeedData.xlsx", read_only=True)
sheet1 = workbook["Sheet1"]
sheet2 = workbook["Sheet2"]
SpeedToRpm = {}
SpeedToRpm[0] = 0
RadiusToAngel_L = {}
RadiusToAngel_L[0] = 90
RadiusToAngel_R = {}
RadiusToAngel_R[0] = 90
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
            RadiusToAngel_L[R] == row[1].value
        if row[0].value == 'R':
            RadiusToAngel_R[R] == row[1].value
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

def GoodAngel_L(Exp = 0):
    MinRadius = 0
    MaxRadius = 0
    MinAngel = 0
    MaxAngel = 0
    for radius in RadiusToAngel_L:
        if radius <= Exp:
            MinRadius = radius
            MinAngel = RadiusToAngel_L[radius]
            break
        MaxRadius = radius
        MaxAngel = RadiusToAngel_L[radius]
    
    return int((((MaxRadius - Exp) * (MaxAngel - MinAngel)) / (MaxRadius - MinRadius)) + MinAngel)
    
def GoodAngel_R(Exp = 0):
    MinRadius = 0
    MaxRadius = 0
    MinAngel = 0
    MaxAngel = 0
    for radius in RadiusToAngel_R:
        if radius <= Exp:
            MinRadius = radius
            MinAngel = RadiusToAngel_R[radius]
            break
        MaxRadius = radius
        MaxAngel = RadiusToAngel_R[radius]
    
    return int((((MaxRadius - Exp) * (MaxAngel - MinAngel)) / (MaxRadius - MinRadius)) + MinAngel)

def GetData(Type, Exp):
    if Type == "rpm" or Type == "RPM":
        return GoodRpm(Exp)
    if Type == "L" or Type == "l":
        return GoodAngel_L(Exp)
    if Type == "R" or Type == 'r':
        return GoodAngel_R(Exp)
