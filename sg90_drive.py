# SG90舵机 驱动
# 徐奥雯编写   XUAOWEN-ASSETS  E-MAIL:CHINA@XUAOWEN.CN  WECHAT:US-00000
# 灰色线为GND接地、红色线为VCC接5V供电、黄色线为脉冲输入
# 运行前 请将脉冲输入所连接的树莓派GPIO引脚号 填写入下面的gpio_pin中
# 您可以直接运行此文件来测试他是否正常工作，你的舵机应该会开始运动
# 在其他py文件中 使用 import sg90_drive 来使用他
# 使用函数 sg90_drive.gs90_angle(角度或‘stop’) 来使用他 

import RPi.GPIO as gpio
import time

gpio_pin = 4  ## 设置黄色线连接的树莓派GPIO口（BCM引脚编号）  手动改此行数据

gpio.setmode(gpio.BCM)  # BCM引脚编号模式
gpio.setup(gpio_pin, gpio.OUT)  # 设置出

# 舵机的控制信号为周期是20ms的脉宽调制（PWM）信号，其中脉冲宽度从0.5ms-2.5ms，相对应舵盘的位置为0－180度，呈线性变化。
# 周期为20ms 就是0.02秒一次  一秒就是50次 频率是50Hz  （计算式：1/0.02=50Hz）
# 脉冲宽度从0.5ms-2.5ms 除以20ms得出占空比 为 2.5% - 12.5%  对应0-180度
# 12.5%-2.5%=10%  180度-0度=180度  10/180 = 0.0555556 %/度   也就是角度每增加1度‘占空比’增加加0.0555556%
# 根据角度算出’占空比‘：’占空比‘等于（2.5+角度*0.0555556） 把0.0555556替换为10/180 算式为（2.5+角度*10/180）

gs90_pwm = gpio.PWM(gpio_pin, 50)   # 实例  （针脚 ， 50Hz频率  每秒多少次）

# 占空比控制也被称为电控脉宽调制技术
# 简单的控制线路只能实现接通工作元件电路或切断工作元件线路这两种工况，也就是开或关，无论如何是不能够实现一定范围的从渐开到渐闭的无极线性调控。
# 而占空比控制技术却另辟蹊径，通过对以一定频率加在工作元件上的电压信号进行占空比控制，利用控制简单开关电路的接通和关闭的比率大小，
# 实现了对工作元件上的电压信号的电压平均值的控制，从而最终实现了对流经工作元件的电流控制。
gs90_pwm.start(0)  # 占空比 （范围：0.0 - 100.0）  表示在一个周期内，工作时间与总时间的比值

# gs90_pwm.ChangeFrequency(100)  # 更新频率 设置新频率，单位为 Hz
# gs90_pwm.ChangeDutyCycle(10)  # 更新占空比 （范围：0.0 - 100.0）  表示在一个周期内，工作时间与总时间的比值


def gs90_angle(angle):
    '''angle 输入0-180度 如果输入 'stop' 则停止'''
    if isinstance(angle, str):  # 判断数据类型
        if angle.upper() == 'STOP':
            gs90_pwm.ChangeDutyCycle(0)  # 更新占空比 （范围：0.0 - 100.0）  表示在一个周期内，工作时间与总时间的比值
        else:
            print('输入有误')
    elif isinstance(angle, int) or isinstance(angle, float):  # 判断数据类型
        gs90_pwm.ChangeDutyCycle(2.5 + angle * 10 / 180)  # 更新占空比 （范围：0.0 - 100.0）  表示在一个周期内，工作时间与总时间的比值


if __name__ == '__main__':

    gs90_angle(0)
    time.sleep(0.3)
    gs90_angle('stop')
    time.sleep(5)

    gs90_angle(180)
    time.sleep(0.3)
    gs90_angle('stop')
    time.sleep(5)

    gs90_pwm.stop()  # 关闭该引脚的 PWM
    gpio.cleanup()  # 清理 在退出时使用



