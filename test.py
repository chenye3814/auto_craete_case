import os
# from OAT.OAT import *
import random
import string
import datetime
import re

strTime = '2019-07-11 11:13'  # 给定一个时间，此是个字符串

strTime_1 = '2019-06'
startTime = datetime.datetime.strptime(strTime, "%Y-%m-%d %H:%M")  # 把strTime转化为时间格式,后面的秒位自动补位的
print(startTime)
print(type(startTime))
print(startTime.strftime("%Y-%m-%d %H:%M:%S")) # 格式化输出，保持和给定格式一致
# startTime时间加 一分钟
startTime2 = (startTime + datetime.timedelta(seconds=1)).strftime("%Y-%m-%d %H:%M:%S")
# print(startTime2)

print('-----------------------------')
# time_strp_list = ['0000-00-00 00:00:00', '0000-00-00 00:00', '0000-00-00 00', '0000-00-00']
# mat = re.match(r'\d{4}-\d{12}-\d{2} \d{2}:\d{2}:\d{2}', strTime)


def find_time_strp(str_time):
    """获取输入的时间字符串，返回其时间格式
    ：str_time：时间字符串
    return：time_strp：时间格式"""
    regex_strp_dict = {r'\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2}': '%Y-%m-%d %H:%M:%S',
                       r'\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}': '%Y-%m-%d %H:%M',
                       r'\d{4}-\d{1,2}-\d{1,2} \d{1,2}': '%Y-%m-%d %H',
                       r'\d{4}-\d{1,2}-\d{1,2}': '%Y-%m-%d',
                       r'\d{4}-\d{1,2}': '%Y-%m',
                       r'\d{4}': '%Y',
                       r'\d{4}/\d{1,2}/\d{1,2} \d{1,2}:\d{1,2}:\d{1,2}': '%Y/%m/%d %H:%M:%S',
                       r'\d{4}/\d{1,2}/\d{1,2} \d{1,2}:\d{1,2}': '%Y/%m/%d %H:%M',
                       r'\d{4}/\d{1,2}/\d{1,2} \d{1,2}': '%Y/%m/%d %H',
                       r'\d{4}/\d{1,2}/\d{1,2}': '%Y/%m/%d',
                       r'\d{4}/\d{1,2}': '%Y/%m',
                       }
    time_strp = False
    for regex in regex_strp_dict.keys():
        mat = re.fullmatch(regex, str_time)
        if mat is not None:
            time_strp = regex_strp_dict[regex]
            break
    return time_strp


a = find_time_strp(strTime)
if a is not False:
    print(a)
else:
    print("该格式的时间尚不能处理")

# def find_time():
#
