import os
# from OAT.OAT import *
import random
import string


def be_case(test_data, result='fail'):
    """生成用例，temp_para为测试数据，result为期望结果,result为 succ or fail"""
    case_one = {'value': test_data, 'result': result}
    return case_one

a = be_case('aaaa')
print(a)