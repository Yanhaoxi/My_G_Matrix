from My_G import *
def gf_multiply(a, b):
    result = 0
    while b > 0:
        if b & 1:  # 如果b的最低位是1
            result ^= a  # 在GF(2^6)中，乘法是异或操作
        a <<= 1  # 左移一位，相当于乘以2
        if a & 0b1000000:  # 如果结果溢出，进行模2^6运算
            a ^= 0b1011011  # 0b10000101是GF(2^6)中的不可约多项式
        b >>= 1  # 右移一位，相当于除以2
    return result%64  # 返回结果

class GF2_6_method:
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


"""test"""
GF2_6=Group("GF2_6",GF2_6_method ,[i for i in range(64)])
GF2_6_data = Data_gen(GF2_6)
assert not GF2_6_data(1).is_zero()
assert GF2_6_data(1).is_one()
assert GF2_6_data(1).reverse == 1
assert GF2_6_data(1) + GF2_6_data(1) == GF2_6_data(0)
assert (GF2_6_data(1) + GF2_6_data(1)).is_zero()
assert GF2_6_data(1) * 1 == GF2_6_data(1)
assert GF2_6_data(1) == 1
assert GF2_6_data(0) == 0
assert 1 == GF2_6_data(1)
