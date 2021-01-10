import time
import datetime
import random
from pypinyin import lazy_pinyin
import string
import re
from dateutil.relativedelta import relativedelta

class base_data(object):
    def be_case(self, test_data, result='fail'):
        """生成用例，
        :test_data：测试数据
        :result：期望结果,result为 succ or fail，默认为'fail',因为大部分数据设计的是无效等价类"""
        case_one = {'value': test_data, 'result': result}
        return case_one

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

    def cul_data(self, data, unit, times=1):
        """计算 目标值 加减 最小单位的值
        :data：目标值
        :unit：数字最小单位
        :times：最小单位的倍数，用于计算加减任何值，可为正数或负数
        """
        data = eval(data)
        unit = eval(unit)
        sum_data = data + unit*times
        return sum_data

    def find_time_strp(self, str_time):
        """获取输入的时间字符串，返回其时间格式，如：%Y-%m-%d %H:%M:%S
        ：str_time：时间字符串
        return：time_strp：时间格式
        """
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

    def date_data(self, str_time, time_strp):
        """把str_time转化为时间格式,后面的秒位自动补位的
        :str_time：目标时间字符串，
        :time_strp：格式化标准
        :return strp_time：数据类型为时间类型的时间
        """
        if time_strp is not False:
            # datetime.strptime()会自动补秒，所以返回的时间格式的数据，无论传入的一定是到秒的
            strp_time = datetime.datetime.strptime(str_time, time_strp)
            return strp_time
        else:
            print("转换时间时发生错误，请检查输入的时间格式是否正确")
            return False

    def cul_time(self, str_time, d_value, dw):
        """根据传入的时间字符串，将其转为时间类型后，进行计算，并返回与给定的字符串格式一致的结果值
        :str_time：时间字符串
        :d_value：进行加减的值，正数表示+，负数表示-
        :dw：单位:秒、分、时、天、月、年
        :return 计算后的结果字符串，格式与给定的一致
        """
        time_strp = self.find_time_strp(str_time)
        strp_time = self.date_data(str_time, time_strp)
        if strp_time is not False:
            if dw == '秒':
                cul_time = (strp_time + relativedelta(seconds=d_value)).strftime(time_strp)
            elif dw == '分':
                cul_time = (strp_time + relativedelta(minutes=d_value)).strftime(time_strp)
            elif dw == '时':
                cul_time = (strp_time + relativedelta(hours=d_value)).strftime(time_strp)
            elif dw == '天':
                cul_time = (strp_time + relativedelta(days=d_value)).strftime(time_strp)
            elif dw == '月':
                cul_time = (strp_time + relativedelta(months=d_value)).strftime(time_strp)
            elif dw == '年':
                cul_time = (strp_time + relativedelta(years=d_value)).strftime(time_strp)
            return cul_time
        else:
            print('请检查输入的时间格式是否正确')
            return False


if __name__ == '__main__':
    a = base_data()
    b = a.cul_data('0', '0.01')
    print(b)