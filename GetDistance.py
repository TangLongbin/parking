import time as t
import RPi.GPIO as GPIO

#四个超声波的Tri引脚对应的GPIO编号
Tri = [11,36,40,7]
#四个超声波的Echo引脚对应的GPIO编号
Echo = [13,15,38,12]

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
#初始化
for i in Tri:
    GPIO.setup(i,GPIO.OUT,initial = GPIO.LOW)
for i in Echo:
    GPIO.setup(i,GPIO.IN)

#获取编号为x的超声波的当前数据
def GetOneDistance(x):
    #向Tri发送10us的高电平
    #发送超声波
    GPIO.output(Tri[x],1)
    t.sleep(0.000015)
    GPIO.output(Tri,0)
    
    #等待发送并设置最大等待时间
    timeout = 10000
    while GPIO.input(Echo[x]) != True and timeout > 0:
        timeout = timeout - 1
    
    #发送后记录当前时刻
    start = t.time()
    
    #等待接收并设置最大等待时间
    timeout = 10000
    while GPIO.input(Echo[x]) != False and timeout > 0:
        timeout = timeout - 1
        
    #接收后记录当前时刻并计算时间差
    end = t.time()
    T = end - start
    
    #计算距离
    Distance = T * 17000
    
    return Distance

#获取编号为所有超声波的当前数据
def GetAllDistance():
    Distance_0 = GetOneDistance(0)
    Distance_1 = GetOneDistance(1)
    Distance_2 = GetOneDistance(2)
    Distance_3 = GetOneDistance(3)
    return Distance_0,Distance_1,Distance_2,Distance_3

if __name__ == '__main__':
    while True:
        Dis = list(GetAllDistance())
        print("前:{:^8.3f}cm 后:{:^8.3f}cm 左:{:^8.3f}cm 右:{:^8.3f}cm".format(Dis[0],Dis[1],Dis[2],Dis[3]),end='\r')
