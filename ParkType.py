import MoveControl
import GetDistance
import time

#车身参数(cm)
Car_Width = 20
Car_Length = 25

#车位边界参数
V_Margin = 15 #垂直边界余量
P_Margin = 10 #水平边界余量
V_Depth = Car_Length + V_Margin #垂直最小深度
P_Width = Car_Width + P_Margin  #水平最小宽度

#测试车位时的设定速度(cm/s)
V_Set = 15

def Init():
    #初始化
    #判断当前车辆停靠方向(左/右)
    L_Distance = GetDistance.GetOneDistance(2)
    R_Distance = GetDistance.GetOneDistance(3)
    if L_Distance <= R_Distance:
        return 'L'
    else:
        return 'R'

def ParkType():
    #判断车位类型(V/P)
    #V表示垂直泊车
    #P表示平行泊车
    #返回('L/R' , 'V/P' , Length , Width)
    x = Init()
    #左右对应的超声波编号
    Dir = {'L' : 2 , 'R' : 3}

    MoveControl.GoStraight(1, V_Set)

    #flag = 0表示垂直泊车
    #flag = 1表示水平泊车
    #默认垂直泊车
    flag = 0
    P_Type = {0 : 'V' , 1 : 'P'}

    S_Measure = GetDistance.GetOneDistance(Dir[x])
    if S_Measure >= P_Width:
        S_1 = 0
    else:
        while S_Measure < P_Width:
            S_1 = S_Measure
            S_Measure = GetDistance.GetOneDistance(Dir[x])

    #疑似车位出现,开始计时
    t_begin = time.time()
    
    #有效测量次数&测量平均值
    Measure_count = 0
    Measure_average = 0

    while S_Measure >= P_Width:

        #累计测量数据
        Measure_average += S_Measure
        Measure_count += 1

        #如果测量距离不满足垂直泊车,则改为平行泊车
        if S_Measure < V_Depth:
            flag = 1

        #目前累计的长度
        t_end = time.time()
        T = t_end - t_begin
        Length_Now = T * V_Set

        #当满足垂直泊车的宽度或满足平行泊车的长度时,结束测量并返回车位类型
        if (flag == 0 and Length_Now >= P_Width) or (flag == 1 and Length_Now >= V_Depth):
            #停车
            MoveControl.GoStraight(0)
            Measure_average /= Measure_count
            return x , P_Type[flag] , Length_Now , Measure_average - S_1

        S_Measure = GetDistance.GetOneDistance(Dir[x])
        S_2 = S_Measure

    #测量距离突变,停止计时并计算时间差
    t_end = time.time()
    T = t_end - t_begin
    Length_Now = T * V_Set
    Measure_average /= Measure_count

    #停车并返回车位类型
    MoveControl.GoStraight(0)
    if (flag == 0 and Length_Now >= P_Width) or (flag == 1 and Length_Now >= V_Depth):
        return x , P_Type[flag] , Length_Now , Measure_average - (S_1 + S_2) / 2
        
    #若车位不满足条件,则进行下一次车位测量
    return ParkType()