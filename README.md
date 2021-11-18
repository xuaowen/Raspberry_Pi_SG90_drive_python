# Raspberry_Pi_SG90_drive_python
树莓派 舵机驱动

灰色线为GND接地、红色线为VCC接5V供电、黄色线为脉冲输入
运行前 请将脉冲输入所连接的树莓派GPIO引脚号 填写入下面的gpio_pin中
您可以直接运行此文件来测试他是否正常工作，你的舵机应该会开始运动
在其他py文件中 使用 import sg90_drive 来导入他
使用函数 sg90_drive.gs90_angle(角度或‘stop’) 来使用他 
