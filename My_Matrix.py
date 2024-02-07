from typing import Sequence, Union, List, Tuple, Any,Protocol
from copy import deepcopy
from random import choice
class Matrix_element(Protocol):
    """
    Matrix_element 协议:需要实现add mul reverse is_zero is_one truediv sub neg六个方法
    1/x 已经用 x**-1 实现
    如果可以的话还需要实现
    __radd__: 解决int + Matrix_element
    __rmul__: 解决int * Matrix_element
    __eq__: 解决Matrix_element == 1 ,Matrix_element == 0
    """
    def __add__(self,other:'Matrix_element')->'Matrix_element':
        pass
    def __mul__(self,other:'Matrix_element')->'Matrix_element':
        pass
    def reverse(self)->'Matrix_element':
        pass
    def is_zero(self)->bool:
        pass
    def is_one(self)->bool:
        pass
    def __truediv__(self,other:'Matrix_element')->'Matrix_element':
        pass
    def __sub__(self,other:'Matrix_element')->'Matrix_element':
        pass
    def __neg__(self)->'Matrix_element':
        pass
    def __pow__(self,other:int)->'Matrix_element':
        pass

class Matrix:
    def __init__(self, data, verify=True):
        if verify:
            self.verify_matrix(data)
        self.data = data
        if (row:=len(data))==0:
            self.cols = 0
        else:
            self.cols = len(data[0])
        self.rows = row

    def __deepcopy__(self, memo):
        # 复制原始矩阵中的元素到新实例中（保持引用）
        data = [[element for element in row] for row in self.data]
        # 创建一个新的 Matrix 对象来存储新的数据
        new_matrix = Matrix(data, verify=False)
        
        return new_matrix

    def __str__(self):
        return '['+'\n'.join(['['+','.join(map(str, row))+']' for row in self.data])+']'
    
    def __repr__(self):
        return f'{self.data}'

    @staticmethod
    def verify_matrix(data)->None|ValueError:
        if not all(len(row) == len(data[0]) for row in data):
            raise ValueError("矩阵行不对齐")
        return None

    @staticmethod
    def swap_rows(matrices:Sequence['Matrix'], row1, row2):
        for matrix in matrices:
            matrix.data[row1], matrix.data[row2] = matrix.data[row2], matrix.data[row1]

    @staticmethod
    def multiply_row(matrices:Sequence['Matrix'], row, scalar):
        for matrix in matrices:
            matrix.data[row] = [scalar * elem for elem in matrix.data[row]]

    @staticmethod
    def add_scaled_row(matrices:Sequence['Matrix'], source_row, target_row, scalar):
        for matrix in matrices:
            matrix.data[target_row] = [scalar * elem_source + elem_target for elem_source, elem_target in
                                       zip(matrix.data[source_row], matrix.data[target_row])]
    @staticmethod
    def gauss_elimination(matrix_list:Sequence['Matrix']):

        # 兼容性问题在My_GF.py中通过修改__eq__解决（赋予0,1加法单位元，乘法单位元的意义）
        assert len(matrix_list)!=0
        matrix=matrix_list[0]
        row, col = 0, 0
        data,rows,cols=matrix.data,matrix.rows,matrix.cols
        # process:判断是否为0,为0则试图寻找，找到则交换行并处理，找不到则列+1，不为0则处理
        while row < rows and col < cols:
            flag=0
            if matrix.data[row][col]==0: #.is_zero():
                for i in range(row+1,rows):
                    if not data[i][col]==0:#.is_zero():
                        Matrix.swap_rows(matrix_list,row,i)
                        flag=1
                        break
                if flag==0:
                    col+=1
                    continue
            if data[row][col]!=1:
                scalar = data[row][col]**-1#.reverse()
                Matrix.multiply_row(matrix_list, row, scalar)
            for i in range(rows):
                if i==row:
                    continue
                if data[i][col]!=0:
                    scalar = -data[i][col]
                    Matrix.add_scaled_row(matrix_list, row, i, scalar)
            row+=1
            col+=1
            continue
        return matrix_list, row-1,col-1 #返回是否可逆
    
    @staticmethod
    def solve(matrix:'Matrix', target:'Matrix'):#target为列向量
        """
        deepcopy在矩阵类中被设计好了传入的矩阵不会被更改
        """
        assert (rows:=matrix.rows)==target.rows and len(target.data[0])==1
        cols = matrix.cols

        matrix_list = [deepcopy(matrix), deepcopy(target)]#深拷贝
        # matrix_list = [matrix, target]
        matrix_list,row_final,col_final= Matrix.gauss_elimination(matrix_list)#列表内是引用，被更改
        matrix,target=matrix_list[0],matrix_list[1]#新的引用
        if row_final==col_final:
            return target
        
        for i in range(row_final+1,rows):
            if target.data[i][0]!=0:
                return None #无解
            
        solution=[0]*cols
        data=matrix.data
        for i in range(rows):
            for j in range(i,cols):
                if data[i][j]==1:
                    solution[j]=target.data[i][0]
                    break
        
        return solution

    @staticmethod
    def I_gen(row_col:int,factory=int):
        """返回单位矩阵,默认为int类型,可以通过传入factory更改类型"""
        return Matrix([[factory(i==j) for j in range(row_col)] for i in range(row_col)])
    
    @staticmethod
    def reverse(matirx:'Matrix',factory=int):
        """返回逆矩阵,不可逆则返回None(由于设计问题在判断为不可逆时比理想开销大)"""
        assert (row_col:=matirx.rows)==matirx.cols
        I=Matrix.I_gen(row_col,factory)
        matirx=deepcopy(matirx)
        matrix_list = [matirx, I]
        matrix_list,row_final,col_final= Matrix.gauss_elimination(matrix_list)
        if row_final!=col_final:
            return None
        return matrix_list[1]
    
    @staticmethod
    def gen(content:Sequence[Matrix_element],rows:int,cols:int):
        return Matrix([[choice(content) for _ in range(cols)] for _ in range(rows)])

    
    @staticmethod
    def product(one: 'Matrix', another: 'Matrix') -> 'Matrix':
        assert one.cols == another.rows, "Incompatible dimensions for matrix multiplication"
        result = [[sum(a*b for a, b in zip(one_row, another_col)) 
                   for another_col in zip(*another.data)] 
                  for one_row in one.data]
        return Matrix(result)
    
    def __matmul__(self,other:'Matrix')->'Matrix':
        return Matrix.product(self,other)

    def __eq__(self,other) -> bool:
        if isinstance(other,Matrix):
            return self.data==other.data
        else:
            return self.data==other
        
    def reshape(self, rows: int, cols: int) -> 'Matrix':
        assert rows * cols == self.rows * self.cols, "Invalid reshape dimensions"
        # 创建一个新的二维数组来存储重组后的数据
        new_data = [[0] * cols for _ in range(rows)]
        # 将原始矩阵的数据逐行逐列复制到新的二维数组中
        for i in range(self.rows):
            for j in range(self.cols):
                index = i * self.cols + j
                new_i, new_j = divmod(index, cols)
                new_data[new_i][new_j] = self.data[i][j]
        # 创建一个新的 Matrix 对象来存储新的数据
        return Matrix(new_data)

        

