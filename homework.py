#导入所需要的包
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as signal
import pylab as pl
import matplotlib

#读取源文件数据并根据时间进行去重处理
df=pd.read_excel(r'D:\jupyter\excel_output.xls')
df=df.drop_duplicates(subset='GPSTime',keep='first')
df.to_excel('excel_output.xls')
columns = df.columns.values.tolist()

#提取位置信息
location=[]
for i in columns:
    if 'location' in i:
        location.append(i)
location=df[location]

l=np.array(location)
l.shape[0]


#提取速度数据并将其转换为列表格式
GPSpdValue=[]
for i in columns:
    if 'GPSpdValue' in i:
        GPSpdValue.append(i)
GPSpdValue=df[GPSpdValue]
v=np.array(GPSpdValue)

#提取时间数据并将其转换为列表格式
GPSTime=[]
for i in columns:
    if 'GPSTime' in i:
        GPSTime.append(i)
GPSTime=df[GPSTime]
t=np.array(GPSTime)

#提取里程数据并将其转换为列表格式
mileageValue=[]
for i in columns:
    if 'mileageValue' in i:
        mileageValue.append(i)
mileageValue=df[mileageValue]
m=np.array(mileageValue)

#提取油量数据并将其转换为列表格式
oilValue = []
for i in columns:
    if 'oilValue' in i:
        oilValue.append(i)
oilValue=df[oilValue]
p=np.array(oilValue)

#绘制里程与油量的关系图
plt.plot(mileageValue,oilValue)
# plt.plot(GPSTime,oilValue)
plt.xlabel('mileageValue')
plt.ylabel('oilValue')
plt.show()

#提取并存储相邻时段内的油量变化
f=[]
for i in range(len(p)-1):
    f.append(p[i+1]-p[i])
    
#对误差进行一阶滞后滤波处理
def FirstOrderLag(inputs,a):
	tmpnum = inputs[0]							
	for index,tmp in enumerate(inputs):
		inputs[index] = (1-a)*tmp + a*tmpnum
		tmpnum = tmp
	return inputs

f1=FirstOrderLag(f,1)

#绘制滤波后的图像
plt.plot(range(0,p.shape[0]-1),f1)

#分析前后油量变化的数据特征
df1 = pd.DataFrame(f) 
df1.describe()

#找出加油时的时间段
n=0
time=[]
count=[]
init=[]
l1=[]
out=[]
for i in range(len(p)-1):
    if((p[i+1]-p[i]>7.8)and(p[i+2]-p[i+1]>7.8)):
        n=n+1
        # print(i)
        count.append(i)
        time.append(t[i])  
        init.append(p[i])
        l1.append(l[i])
# print(n)      
 
       
#打印出加油时的时间，初始油量以及位置信息数据
print('')
print('')
print('')
print('加油时间点')
print('')
flag=1
print('第1次加油时间为：',time[0])
# print(init[0])
# print(l1[0])
for i in range(n-1):
    if count[i+1]-count[i]>10:
        flag=flag+1
        print(f"第{flag}次加油时间为：",time[i+1])
        # print(init[i+1])
        # print(l1[i+1])


#提取出每次加油前油量的数据
print('')
print('')
print('')
print('加油前油量')
print('')
oilbefore=1
print('第1次加油前油量为：',init[0])
for i in range(n-1):
    if count[i+1]-count[i]>10:
        oilbefore=oilbefore+1
        print(f"第{oilbefore}次加油前油量为：",init[i+1])
        
 #提取出每次加油前的位置信息  
print('')
print('')
print('')
print('加油前位置信息')  
print('')   
localbefore=1
print('第1次加油前位置为：',l1[0])
for i in range(n-1):
    if count[i+1]-count[i]>10:
        localbefore=localbefore+1
        print(f"第{localbefore}次加油前位置为：",l1[i+1])

#打印出加油次数
print('')
print('')
print('')
print('加油次数为：',flag)  
print('')     
full=[p[3],p[111],p[1254],p[2410],p[2710],p[4749],p[6119],p[9678],p[9820],p[10489],p[12746]]
empty=[[97.8],[228.1],[274.0],[124.0],[238.7],[87.4],[80.3],[80.9],[134.8],[203.0],[93.1]]

#求出每次的加油量
print('')
print('')
print('每次加油的油量')
print('')
oil1=[]
for i in range(1,12):
    oil1.append(full[i-1]-empty[i-1])
    print(f'第{i}次的加油量为：',oil1[i-1])
    
#计算11次总的加油量
print('')
print('')
print('')
print('全程加油的总油量')
oilsum=222.2+77.4+46+196+81.3+232.6+138.7+82.7+185.2+117+226
print('11次总的加油量为：',oilsum)

#计算出全程的理论耗油量
print('')
print('')
print('')
print('全程的理论耗油量')
oilcustom=oilsum-(p[p.shape[0]-1]-p[0])
print('全程油量的理论消耗值为：',oilcustom)

#计算全程油量的实际消耗值
print('')
print('全程的实际耗油量')
ps=[]
for i in range(10):
    ps.append(full[i]-empty[i+1])
    print(f'第{i+1}次的耗油量为：',ps[i])
print('')
print('')
print('')   
s=0
for i in range(10):
    s=s+ps[i]
print('全程油量的实际消耗值为：',s)   
print('')
print('')
print('')

#计算油量消耗的变化率
print('计算耗油量的浮动率')
delta=oilcustom-s
yita=delta/oilcustom
print('耗油量的浮动比率是：',yita)
    

