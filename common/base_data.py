import time
import datetime
import random
from pypinyin import lazy_pinyin
import string


# strTime = '2019-07-11 11:03:50'  # 给定一个时间，此是个字符串
# startTime = datetime.datetime.strptime(strTime, "%Y-%m-%d %H:%M:%S")  # 把strTime转化为时间格式,后面的秒位自动补位的
# print(startTime)
# print(type(startTime))
# print(startTime.strftime("%Y-%m-%d %H:%M:%S")) # 格式化输出，保持和给定格式一致
# # startTime时间加 一分钟
# startTime2 = (startTime + datetime.timedelta(seconds=1)).strftime("%Y-%m-%d %H:%M:%S")
# print(startTime2)


class base_data(object):
    def cn_test_data(self):
        """随机生成一位中文字符,用于字符类型限制的测试数据生成"""
        cns = ["伟", "华", "建", "国", "洋", "刚", "里", "万", "爱", "民", "牧", "陆", "路", "昕", "鑫", "兵", "硕", "志", "宏", "峰", "磊",
               "雷", "文", "明", "浩", "光", "超", "军", "达"]
        random_cn = random.choice(cns)
        return random_cn

    def cn_to_pinyin(self, temp):
        """中文转为拼音,使用lazy_pinyin()函数转为拼音，该函数返回的是数组，如：['zhao', 'ge']
        ,用于字符类型限制的测试数据生成"""
        temp_en = ''.join(lazy_pinyin(temp))
        return temp_en

    def en_test_data(self):
        """随机生成一位英文字母,用于字符类型限制的测试数据生成"""
        random_str = ''.join(random.sample(string.ascii_letters, 1))
        return random_str

    def num_test_data(self):
        """生成随机数字,用于字符类型限制的测试数据生成"""
        random_num = random.randint(1, 9)
        return str(random_num)

    def sp_test_data(self):
        """特殊字符生成的列表，需要添加新的则在value_sp里面加即可，用空格隔开,用于字符类型限制的测试数据生成"""
        value_sp = '# , * + - / \" \' $ % ( : ; ? \\ &'
        sp_list = value_sp.split(' ')
        return sp_list

    def add_space(self, temp):
        """用于生成空格的测试数据，分别在目标的中增加空格"""
        if len(temp) > 1:
            str_list = []
            for i in temp:
                str_list.append(i)
            str_list.insert(1, ' ')
            return ''.join(str_list)

    def sum_data(self, data, unit):
        """计算 目标值 加 最小单位的值
        :data：目标值
        :unit：数字最小单位
        """
        sum_data = data + unit
        return sum_data

    def subtr_data(self, data, unit):
        """计算 目标值 减 最小单位的值
        :data：目标值
        :unit：数字最小单位
        """
        subtr_data = data - unit
        return subtr_data




if __name__ == '__main__':
    a = base_data()
    b = a.subtr_data(0, 0.01)
    print(b)