from My_G import *
from My_Matrix import *
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
content = [mod5(i) for i in range(5)]

"""test"""
deepcopy(Matrix([[content[1]]]))
# My_Matrix = Matrix.gen(content,4,4)
# a=My_Matrix
# b=Matrix.reverse(My_Matrix,mod5)
# if b is not None:
#     print(a@b)

# while True:
#     num_matrix = Matrix.gen(content,4,4)
#     if (re_matix:=Matrix.reverse(num_matrix)) is not None:
#         break
# print(num_matrix)
# in_matrix = Matrix.gen(content,4,1,mod5)
# print(in_matrix)
# out_matrix = num_matrix@in_matrix
# print(out_matrix)
# result = Matrix.solve(num_matrix, out_matrix)
# print(result)
# assert result == in_matrix


# My_Matrix = Matrix.gen(content,3,4)
# print(My_Matrix)
# My_Matrix.reshape(4,3)
# print(My_Matrix)