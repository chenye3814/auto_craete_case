import os
# from OAT.OAT import *

file_path = R'C:\Users\Administrator\Desktop\model.txt'
command_run = R'pict ' + file_path
# 使用os.popen执行命令可以获取到返回结果，使用os.system能够执行但是拿不到结果
# mode：打开文件的模式，默认为'r'，用法与open()相同
# buffering：0意味着无缓冲；1意味着行缓冲；其它正值表示使用参数大小的缓冲。负的bufsize意味着使用系统的默认值，一般来说，对于tty设备，它是行缓冲；对于其它文件，它是全缓冲。
result_run = os.popen(command_run, mode='r')
a = result_run.readlines()
# 读出的结果内容是这样的：['SEX\tCLASS\tSCROE\n', 'M\t4\tBAD\n', 'M\t1\t无成绩\n', 'M\t无班级\tOK\n',
# 第一行是每个参数的名称，需要转换成参数列表，中间涉及到的空格、换行符号等需要处理一下
paras = a[0]
paras_list = paras.replace('\n', '').split('\t')
# 定义case_list用来存储生成的测试用例，每个测试用例以字典形式存储
case_list = []

for i in range(1, len(a)):
    dict_case = {}
    list_i = a[i].replace('\n', '').split('\t')
    # print(list_i)
    for j in range(len(paras_list)):
        dict_case[paras_list[j]] = list_i[j]
    case_list.append(dict_case)

print(case_list)