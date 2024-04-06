import math
import struct
import time
import matplotlib.pyplot as plt


# addr = ('127.0.0.1', 1180) #clinet端ip地址 //192.168.4384

class imu:
    def __init__(self):
        
        self.ACCData=[0.0]*58           #52
        self.FrameState = 0            #通过值判断属于哪一种情况
        self.Bytenum = 0               #读取到这一段的第几位

        #头段	
        SOF = 0xa5
        data_length = 30 #data段长度
        self.seq = 0x00 #包序号，每一次加一
        crc8 = 0x00 
        #命令字
        cmd_id = 0x0302 
        #数据段
        key_1 = 0xff
        key_2 = 0xff
        blank = 0x0001

        a = [0.0]*3
        w = [0.0]*3
        m = [0.0]*3

        Angle = [0.0]*3

        kz=[0.0]*3    #输入的控制变量1,2

        q=[0.0]*4  
        end_float = float("inf")
 

    def DueData(self, inputdata):   #读取的数据到数组里
        self.seq = self.seq + 1  #每次传输更新包序号
        if (self.seq > 255):
            self.seq = 0
    
        for data in inputdata:  #输入的数据进行遍历    

            if self.FrameState==0:   #当未确定状态的时候，进入以下判断

                if data==0x50 : #0x55位于第一位时候，开始读取数据，增大self.Bytenum

                    self.Bytenum=0
                    self.FrameState=1
                    continue    

            elif self.FrameState==1: # acc    #已确定数据

                if self.Bytenum<57:            # 读取51个数据    51
                    self.ACCData[self.Bytenum+1]=data # 从0开始
                    self.Bytenum+=1

                else:
                 #校验
                    if (self.ACCData[49] * 256.0 * 256.0 + self.ACCData[50] * 256.0 + self.ACCData[51] - 1000000) * 0.001 == 128 :

                        # g = get_gyro(self)   #陀螺仪
                        # a = get_acc(self) #加速度
                        # Angle = get_angle(self)  #角度

                        # kz=get_kz(self.ACCData)  #输入的控制变量
                        # q=get_q (self.ACCData)

                                    #各数据归零，进行新的循环判断

                        self.Bytenum=0

                        self.FrameState=0
            
 

    def get_gyro(self):   #陀螺仪 angular acceleration

        gyro_x = (self.ACCData[1] * 256.0 * 256.0 + self.ACCData[2] * 256.0 + self.ACCData[3] - 1000000) * 0.001; # gx
        gyro_y = (self.ACCData[4] * 256.0 * 256.0 + self.ACCData[5] * 256.0 + self.ACCData[6] - 1000000) * 0.001; # gy
        gyro_z = (self.ACCData[7] * 256.0 * 256.0 + self.ACCData[8] * 256.0 + self.ACCData[9] - 1000000) * 0.001; # gz

        # print("gro x: ", gyro_x, "pitch: ", gyro_y, "yaw: ", gyro_z, end = "\r")
        return gyro_x, gyro_y, gyro_z

    def get_acc(self): #axis accelerator

        acc_x = (self.ACCData[10] * 256.0 * 256.0 + self.ACCData[11] * 256.0 + self.ACCData[12] - 1000000) * 0.001;  # ax
        acc_y = (self.ACCData[13] * 256.0 * 256.0 + self.ACCData[14] * 256.0 + self.ACCData[15] - 1000000) * 0.001;  # ay
        acc_z = (self.ACCData[16] * 256.0 * 256.0 + self.ACCData[17] * 256.0 + self.ACCData[18] - 1000000) * 0.001;  # az

        return acc_x, acc_y, acc_z

    def get_mg(self): #magnetometer

        mg_x = (self.ACCData[19] * 256.0 * 256.0 + self.ACCData[20] * 256.0 + self.ACCData[21] - 1000000) * 0.001;  # mx
        mg_y = (self.ACCData[22] * 256.0 * 256.0 + self.ACCData[23] * 256.0 + self.ACCData[24] - 1000000) * 0.001;  # my
        mg_z = (self.ACCData[25] * 256.0 * 256.0 + self.ACCData[26] * 256.0 + self.ACCData[27] - 1000000) * 0.001;  # mz

        return mg_x, mg_y, mg_z

    def get_angle(self): #euler angle

        angle_x = (self.ACCData[28] * 256.0 * 256.0 + self.ACCData[29] * 256.0 + self.ACCData[30] - 1000000) * 0.001;  # roll angle_x
        angle_y = (self.ACCData[31] * 256.0 * 256.0 + self.ACCData[32] * 256.0 + self.ACCData[33] - 1000000) * 0.001;  # pitch
        angle_z = (self.ACCData[34] * 256.0 * 256.0 + self.ACCData[35] * 256.0 + self.ACCData[36] - 1000000) * 0.001;  # yaw

        # if(abs(angle_y) > 70 ):
        #     print("Y-axis Face down")
            
        # if(abs(angle_x) > 70 ):
        #     print("x-axis Face down")
        return angle_x,angle_y,angle_z

 

    def check_angle(cur, pre):

        change = cur - pre
        
        delta_r, delta_p, delta_yaw = change
        print(delta_r,delta_p, delta_yaw, end = "\r")
    
        # if(delta_r > 1 & random.randint(0,1)):
        #     # print("Roll rotate")
        # if(delta_p > 1):
        #     # print("pitch rotate")
        # if(delta_yaw > 1):
        #     # print("yaw rotate")

    def get_kz(self):
        kz_x = (self.ACCData[52] * 256.0 * 256.0 + self.ACCData[53] * 256.0 + self.ACCData[54] - 1000000) * 0.001;  # 1
        kz_y = (self.ACCData[55] * 256.0 * 256.0 + self.ACCData[56] * 256.0 + self.ACCData[57] - 1000000) * 0.001;  #2
        kz_z = 0;  #

        return kz_x,kz_y,kz_z

 
    def get_q(self):

        q_0 = (self.ACCData[37] * 256.0 * 256.0 + self.ACCData[38] * 256.0 + self.ACCData[39] - 1000000) * 0.001;  # q0
        q_1 = (self.ACCData[40] * 256.0 * 256.0 + self.ACCData[41] * 256.0 + self.ACCData[42] - 1000000) * 0.001;  #q1
        q_2 = (self.ACCData[43] * 256.0 * 256.0 + self.ACCData[44] * 256.0 + self.ACCData[45] - 1000000) * 0.001;  #q2
        q_3 = (self.ACCData[46] * 256.0 * 256.0 + self.ACCData[47] * 256.0 + self.ACCData[48] - 1000000) * 0.001;  #q3

        return q_0,q_1,q_2,q_3



