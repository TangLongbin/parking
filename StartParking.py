import ParkType
import MoveControl
import GetDistance
import time
from math import pi, sqrt

P_Esp = 5 # 前后居中误差
V_Esp = 4 # 左右居中误差
L_rw = 5 # 后悬长度

V_Park = 20 # 泊车时的速度
V_Adjusting = 10 # 调整时的速度
R_Adjusting = 1 # 调整时的半径

def Center_check_P(front , back):
    # 每次调整约1cm
    if front > back:
        MoveControl.GoStraight(1 , V_Adjusting)
    else:
        MoveControl.GoStraight(-1 , V_Adjusting)
    time.sleep(0.1)
    MoveControl.GoStraight(0)

    return 1

def Center_check_V(left , right):
    #每次进行细微调整
    if left > right:
        MoveControl.GoStraight(1 , V_Adjusting , 'L' , R_Adjusting)
        time.sleep(0.1)
        MoveControl.GoStraight(0)
        MoveControl.GoStraight(1 , V_Adjusting , 'R' , R_Adjusting)
        time.sleep(0.1)
        MoveControl.GoStraight(0)
        MoveControl.GoStraight(-1 , V_Adjusting)
        time.sleep(0.2)
        MoveControl.GoStraight(0)
    else:
        MoveControl.GoStraight(1 , V_Adjusting , 'R' , R_Adjusting)
        time.sleep(0.1)
        MoveControl.GoStraight(0)
        MoveControl.GoStraight(1 , V_Adjusting , 'L' , R_Adjusting)
        time.sleep(0.1)
        MoveControl.GoStraight(0)
        MoveControl.GoStraight(-1 , V_Adjusting)
        time.sleep(0.2)
        MoveControl.GoStraight(0)
    return 1

def V_Parking(data):
    W = ParkType.Car_Width
    L = ParkType.Car_Length
    L_base = L - 2*L_rw # 轴距(默认前后悬长度相同)
    R = (L_base * (W/2)) / (L - L_rw - L_base) # 转向半径
    X_Ar = sqrt((R + (W/2))**2 + L_rw**2) - (data[2]/2)

    #设定最佳泊车起点
    MoveControl.GoStraight(1 , V_Park)
    T = (X_Ar - data[2]) / V_Park
    time.sleep(T)
    MoveControl.GoStraight(0)

    #按照计算数据进行泊车
    MoveControl.GoStraight(-1 , V_Park , 'L' if data[0] == 'L' else 'R' , R)
    T = (R * (pi/2.0)) / V_Park
    time.sleep(T)
    MoveControl.GoStraight(0)
    
    return 1

def V_adjust(data):
    Left_dis = GetDistance.GetOneDistance(2)
    Back_dis = GetDistance.GetOneDistance(1)
    Front_dis = data[3] - ParkType.Car_Length - Back_dis
    Right_dis = GetDistance.GetOneDistance(3)

    if (abs(Front_dis - Back_dis) <= P_Esp) and (abs(Left_dis - Right_dis) <= V_Esp):
        return 1

    if abs(Front_dis - Back_dis) >  P_Esp:
        Center_check_P(Front_dis , Back_dis)
    
    if abs(Left_dis - Right_dis) > V_Esp:
        Center_check_V(Left_dis , Right_dis)

    return V_adjust(data)

def P_Parking(data):
    x_p = data[2] # 车位长度
    y_p = data[3] # 车位宽度
    W = ParkType.Car_Width # 车宽
    L_2 = L_rw # 后悬长度
    L_1 = ParkType.Car_Length - L_2 # 后悬轴到车前端的距离
    E_1 = data[4] + W/2.0
    
    R_m = ((x_p - L_2)**2 - L_1**2 + (y_p/2.0)**2 - (W/2.0)**2) / (W + y_p) # 第二段泊车半径
    E_2 = ((x_p - L_2) * (2*E_1 - W)) / (W + y_p)
    R_1 = E_1/2.0 + y_p/4 - R_m + ((E_2 + x_p - L_2)**2) / (2*E_1 + y_p) # 第一段泊车半径

    #设定最佳泊车起点
    MoveControl.GoStraight(1 , V_Park)
    T = (E_2 - L_2) / V_Park
    time.sleep(T)
    MoveControl.GoStraight(0)
    
    #按照计算数据进行泊车
    phi = pi/4.0 # 两段圆弧对应的圆心角

    MoveControl.GoStraight(-1 , V_Park , 'L' if data[0] == 'L' else 'R' , R_1)
    T = (R_1 * phi) / V_Park
    time.sleep(T)
    MoveControl.GoStraight(0)

    MoveControl.GoStraight(-1 , V_Park , 'R' if data[0] == 'L' else 'L' , R_m)
    T = (R_m * phi) / V_Park
    time.sleep(T)
    MoveControl.GoStraight(0)

    return 1

def P_adjust(data):
    Front_dis = GetDistance.GetOneDistance(0) # 前侧余量
    if data[0] == 'L':
        Left_dis = GetDistance.GetOneDistance(2) # 左侧余量
        Right_dis = data[3] - ParkType.Car_Width - Left_dis # 右侧余量
    else:
        Right_dis = GetDistance.GetOneDistance(3)
        Left_dis = data[3] - ParkType.Car_Width - Right_dis
    Back_dis = GetDistance.GetOneDistance(1) # 后侧余量

    if (abs(Front_dis - Back_dis) <= P_Esp) and (abs(Left_dis - Right_dis) <= V_Esp):
        return 1
    
    if abs(Front_dis - Back_dis) >  P_Esp:
        Center_check_P(Front_dis , Back_dis)
    
    if abs(Left_dis - Right_dis) > V_Esp:
        Center_check_V(Left_dis , Right_dis)

    return P_adjust(data)

def StarPaking():
    Data = ParkType.ParkType()
    #返回('L/R' , 'V/P' , Length , Width , E)
    #'L/R' : 泊车方向
    #'V/P' : 泊车类型
    #Length : 车位长度
    #Width : 车位宽度
    #E : 车的下边界与车位上边界的距离

    #调整起始位置
    MoveControl.GoStraight(1,20)
    time.sleep(0.5)
    MoveControl.GoStraight(0)

    #根据车位类型进行泊车
    if Data[1] == 'V':
        V_Parking(Data)
        V_adjust(Data)
    if Data[1] == 'P':
        P_Parking(Data)
        P_adjust(Data)

    #停车确认
    MoveControl.GoStraight(0)
    return 1