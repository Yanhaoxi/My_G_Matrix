from typing import List, Hashable, Protocol, TypeVar ,Sequence, Union, TypeVar,Optional
from collections import UserDict
from copy import deepcopy

class G_method(Protocol):
    """G_method 协议:需要实现add mul get_I get_0四个静态方法"""
    @staticmethod
    def add(a, b):
        pass

    @staticmethod
    def mul(a, b):
        pass

    @staticmethod
    def get_I():
        pass

    @staticmethod
    def get_0():
        pass

G_able = TypeVar('G_able', bound=G_method)
T = TypeVar('T', bound=Hashable)

class Group:
    """
    0,1是有默认为乘法单位元和加法单位元
    __init__:
        Etc:
        G_mod5=Group('G_mod5', mod5_method(),[i for i in range(5)])
        目前content不具备自扩展能力,只有自己保证运算封闭该模块才能正常运行
    attributes:
        (T必须是可哈希的类型,不然会报错)
        gname: str
        content: List[T]
        add: G_method.add
        mul: G_method.mul
        g_1: G_method.get_I()
        g_0: G_method.get_0()
        g_mul_dict: dict[T, dict[T, T]]
        g_add_dict: dict[T, dict[T, T]]
        g_re_mul: dict[T, T|None] 0不具有乘法逆元返回None
        g_re_add: dict[T, T]
    """
    def gen_add_dict(self,value):
        return {i:self.add(value,i) for i in self.content}
    
    def gen_mul_dict(self,value):
        return {i:self.mul(value,i) for i in self.content}
    
    def gen_re_mul(self,mul_dict):
        for i,j in mul_dict.items():
            if j == self.g_1:
                return i
        return None #没有乘法逆元
    
    def gen_re_add(self,add_dict):
        for i,j in add_dict.items():
            if j == self.g_0:
                return i
        return None #没有加法逆元

    def __init__(self, Gname, G_method: G_able, content: Sequence[T]):
        self.gname:str = Gname
        self.content:List[T] = list(content)
        assert len(self.content) > 1, "An abnormal G must have at least two elements"
        self.add = G_method.add
        self.mul = G_method.mul
        self.g_1 = G_method.get_I()
        self.g_0 = G_method.get_0()
        self.g_mul_dict: dict[T, dict[T, T]] = {i: self.gen_mul_dict(i) for i in content}
        self.g_add_dict: dict[T, dict[T, T]] = {i: self.gen_add_dict(i) for i in content}
        self.g_re_mul:dict[T,T|None] = {i: self.gen_re_mul(self.g_mul_dict[i]) for i in content}
        self.g_re_add:dict[T,T] = {i: self.gen_re_add(self.g_add_dict[i]) for i in content}
        

    def __repr__(self):
        content_str = list(map(str, self.content))
        return f"Group(Gname={self.gname}, content={content_str})"
            
    def dis_dict(self):
        print(f'g_mul_dict:{self.g_mul_dict}')
        print(f'g_add_dict:{self.g_add_dict}')
        print(f'g_re_mul:{self.g_re_mul}')
        print(f'g_re_add:{self.g_re_add}')
        
class fdata:
    """
    不建议直接使用,该类依附于Data_gen,给value赋值时会自动填充muldict,adddict,readd,remul
    加法单位元判断标准:self+self==self
    乘法单位元判断标准:self*self==self and self!=0
    所有的对象都保存在Data_gen的content属性中(通过Data_gen的__call__方法调用)
    由于为了兼容My_Matrix模块不得不加入__pow__方法,与其他运算符不同当为0时会返回1,可能会引起错误故增加打印警告
    扩展了__eq__的判断:0,1是有默认为乘法单位元和加法单位元
    reverse属性:返回逆元,没有逆元时会报错
    """
    def __init__(self, value:T ,g_mul_dict:dict[T,'fdata'], g_add_dict:dict[T,'fdata'], g_re_mul:dict[T,Optional['fdata']],g_re_add:dict[T,'fdata']):
        if value is None:
            return 
        else:
            self.value = value
            self.muldict:dict[T,'fdata'] = g_mul_dict
            self.adddict:dict[T,'fdata'] = g_add_dict
            self.readd = g_re_add
            self.remul = g_re_mul
    
    def is_zero(self):
        return self+self==self
    
    def is_one(self):
        if self.value == 0:
            return False
        return self*self==self
    
    @property
    def reverse(self)->Optional['fdata']:
        if (result:=self.remul[self.value]) is None:
            raise ValueError(f"{self.value} has no reverse element")
        return result
    
    def __radd__(self, other):
        return self + other
    
    def __rmul__(self, other):
        return self * other
    
    def __add__(self, other:'fdata'|T)->'fdata':
        if isinstance(other, fdata):
            return self.adddict[other.value]
        return self.adddict[other]

    def __mul__(self, other:'fdata'|T)->'fdata':
        if isinstance(other, fdata):
            return self.muldict[other.value]
        return self.muldict[other]
       
    def __neg__(self):
        return self.readd[self.value]
    
    def __sub__(self, other):
        return self + (-other)
    
    def __truediv__(self, other):
        return self * other.reverse
    
    def __pow__(self, other):
        if other==0:
            print("warning:x**0 may cause error,return int(1)")
            return 1
        if other==1:
            return self
        if other<0:
            return self.reverse.__pow__(-other)
        return self * (self ** (other-1))
    
    def __repr__(self):
        if self.value is None:
            return "None"
        return f"d_{self.value}"
    
    def __str__(self):
        return f"{self.value}"
    
    def __eq__(self, other):
    #扩展了等于的定义，可以和0，1比较
        try:
            return self.value == other.value
        except:
            if other==0:
                return self.is_zero()
            if other==1:
                return self.is_one()
            else :
                raise ValueError("can't compare")

class Data_dict(UserDict):
    def __init__(self, G, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.G=G
    def __getitem__(self, key):
        if key==0:
            return self.data[self.G.g_0]
        elif key==1:
            return self.data[self.G.g_1]
        else:
            return self.data[key]

class Data_gen:
    def __init__(self, G:'Group'):
        """接受来自Group的G,生成fdata的实例,并用fdata实例填充muldict,adddict,readd,remul"""
        def generate_dic_2D(dict_2D: dict[T, dict[T, T]]) -> dict[T, dict[T, int]]:
            new_dict_2D = {i: {k: 0 for k, _ in j.items()} for i, j in dict_2D.items()}
            return new_dict_2D
        self.g_mul_dict = generate_dic_2D(G.g_mul_dict)
        self.g_add_dict = generate_dic_2D(G.g_add_dict)
        self.g_re_mul = {i: None for i in G.content}
        self.g_re_add = {i: None for i in G.content}
        for i, j in G.g_mul_dict.items():
            for k, l in j.items():
                self.g_mul_dict[i][k] = fdata(l, self.g_mul_dict[l], self.g_add_dict[l], self.g_re_mul, self.g_re_add)#type:ignore
        for i, j in G.g_add_dict.items():
            for k, l in j.items():
                self.g_add_dict[i][k] = fdata(l, self.g_mul_dict[l], self.g_add_dict[l], self.g_re_mul, self.g_re_add)#type:ignore
        for k, l in G.g_re_mul.items():#type:ignore
            if l is None:
                self.g_re_mul[k] = None
                continue
            self.g_re_mul[k] = fdata(l, self.g_mul_dict[l], self.g_add_dict[l], self.g_re_mul, self.g_re_add)#type:ignore
        for k, l in G.g_re_add.items():
            self.g_re_add[k] = fdata(l, self.g_mul_dict[l], self.g_add_dict[l], self.g_re_mul, self.g_re_add)#type:ignore
        

        self.content=Data_dict(G,{i:fdata(i, self.g_mul_dict[i], self.g_add_dict[i], self.g_re_mul, self.g_re_add) for i in G.content})#type:ignore
    
    def __call__(self,value):
        return self.content[value]




    
