# My_G_matrix 
实现了在G上的运算以及提供了matrix模块供解线性方程组求逆等操作
## 使用方法
### My_G模块
```python
class GF_mod5_method:
    @staticmethod
    def add(a, b):
        return (a + b)%5
    @staticmethod
    def mul(a, b):
        return (a * b)%5
    @staticmethod
    def get_I():    
        return 1
    @staticmethod
    def get_0():
        return 0

GF_mod5=Group("GF_mod5",GF_mod5_method ,[i for i in range(5)])
mod5=Data_gen(GF_mod5)
```
- 实现G_method协议的方法类传入给Group,同时需要自己给出域中所有元素
- 用Data_gen(G_method)获得数据生成器
- 用数据生成器传入值获得域中元素(所有魔术方法已经自行绑定)

### My_Matrix模块
```python
from My_G import *
from My_Matrix import *
def gf_multiply(a, b):
    result = 0
    while b > 0:
        if b & 1:  # 如果b的最低位是1
            result ^= a  # 在GF(2^6)中，乘法是异或操作
        a <<= 1  # 左移一位，相当于乘以2
        if a & 0b100000000:  # 如果结果溢出，进行模2^8运算
            a ^= 0x1D  # GF(2^8)中的不可约多项式
        b >>= 1  # 右移一位，相当于除以2
    return result%256  # 返回结果

class GF2_8_method:
    @staticmethod
    def add(a, b):
        return a ^ b
    @staticmethod
    def mul(a, b):
        return gf_multiply(a, b)
    @staticmethod
    def get_I():    
        return 1
    @staticmethod
    def get_0():
        return 0
    
GF2_8 = Group("GF2_8",GF2_8_method ,[i for i in range(256)])
GF2_8_data = Data_gen(GF2_8)

gfmat_my=Matrix([[GF2_8_data(i) for i in mat]]).reshape(24, 24) 
re=Matrix.reverse(gfmat_my,GF2_8_data)
target_my=Matrix([[GF2_8_data(i) for i in target]]).reshape(24, 1)
result2 = re@target_my
result = Matrix.solve(gfmat_my, target_my) 
assert result == result2
for i in result.reshape(1,24).data[0]:
    print(chr(i.value),end='')
```
- reverse函数第二个参数接受的是数据生成器默认是int
- solve函数第一个参数是系数矩阵，第二个参数是列向量，返回解，无解则为None

## 未来可能的改动
- 给类加入__slot__方法减少空间的开销
- 对于输入会增加验证功能防止潜在错误发生
- 输入域的定义域可以不完整会进行自扩充

## 版本要求
仅在python3.11下进行了测试
