import xlrd
from pypinyin import lazy_pinyin
import random
import string

aa = {'para': '客户昵称',
      'type': 'input',
      'input_rules': "{'input_char': 'cn', 'input_len': '5', 'input_like': 'yes'}",
      'target': '赵哥'
      }


class search_own(object):
    def __init__(self, temp_dict):
        self.target = temp_dict['target']
        self.input_rules = eval(temp_dict['input_rules'])
        self.type = temp_dict['type']
        self.para = temp_dict['para']

    def be_case(self, test_data, result='fail'):
        """生成用例，temp_para为测试数据，result为期望结果,result为 succ or fail，默认为'fail',因为大部分数据设计的是无效等价类"""
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

    def sp_test_case(self, sp_list, temp):
        """用于参数与特殊字符组合生成测试数据,然后生成用例列表,用于字符类型限制的测试数据生成
        :sp_list：特殊字符列表
        :temp：测试目标
        """
        case_list = []
        if isinstance(sp_list, list):
            for i in sp_list:
                temp_i = str(temp)[0] + str(i)
                temp_j = str(i)+str(temp)
                case_1 = self.be_case(temp_i)
                case_2 = self.be_case(temp_j)
                case_list.extend([case_1, case_2])
            return case_list

    def travel_data_case(self, ca_list, def_list):
        """传入待使用的测试数据生成的函数，遍历这些方法、生成测试数据并生成用例
        :case_list：测试用例列表
        :def_list：待执行的函数列表
        """
        for data in def_list:
            # 如果data是列表，说明传输的是一个特殊字符列表，该列表需要遍历处理一下,
            # 分为：单独传入特殊字符，和特殊字符与目标数据组合的两种形式的用例
            # 后面考虑在目标中间插入特殊字符等 尝试
            if isinstance(data, list):
                for sp_char in data:
                    case_1 = self.be_case(test_data=sp_char)
                    ca_list.append(case_1)
                case_2 = self.sp_test_case(sp_list=data, temp=self.target)
                ca_list.extend(case_2)

            else:
                # 如果不是列表，则data是生成某一字符数据的函数，如生成汉字、字母、数字的函数
                case_1 = self.be_case(test_data=data)
                case_2 = self.be_case(test_data=self.target + data)
                case_3 = self.be_case(test_data=data + self.target)
                ca_list.extend([case_1, case_2, case_3])
        return ca_list

    def input_test_data(self):
        """文本输入类的用例数据生成"""
        if self.type == 'input':
            case_list = []
            # 将目标作为测试数据，期望结果为正确
            right_case = self.be_case(test_data=self.target, result='succ')
            case_list.append(right_case)
            if self.input_rules['input_char']:
                if self.input_rules['input_char'] == 'cn':
                    # 思考这里如何简化，当指定一种类型时，自动将另外三中错误字符生成用用例，
                    # 是否需要用到for循环去生成，还是把上面的value分装在字典还是什么里面
                    cn_use = [self.cn_to_pinyin(self.target), self.en_test_data(), self.num_test_data(), self.sp_test_data()]
                    case_list = self.travel_data_case(ca_list=case_list, def_list=cn_use)

                elif self.input_rules['input_char'] == 'en':
                    # 后面要考虑加入大小写
                    en_use = [self.cn_test_data(), self.num_test_data(), self.sp_test_data()]
                    case_list = self.travel_data_case(ca_list=case_list, def_list=en_use)

                elif self.input_rules['input_char'] == 'num':
                    num_use = [self.cn_test_data(), self.en_test_data(), self.sp_test_data()]
                    case_list = self.travel_data_case(ca_list=case_list, def_list=num_use)

                else:
                    print("输入字符类型为cn/en/num时才能创建用例，请检查<input_char>值是否正确")
        return case_list
"""
            if self.input_rules['input_len']:
                n = eval(self.input_rules['input_len'])
                # m = len(target)
                a = n - 1
                b = n + 1
                # shang = n/m
                case_len_a = n * '赵'
                case_len_b = a * '赵'
                case_len_c = b * '赵'

            if self.input_rules['input_like']:
                if self.input_rules['input_like'] == 'yes':
                    case_like_a = self.target
                    case_like_b = self.target[1]
                    case_like_c = self.target * 2
                else:
                    case_like_a = self.target
                    case_like_b = self.target[1]
                    case_like_c = self.target * 2
"""

if __name__ == '__main__':
    case = search_own(temp_dict=aa)
    cases = case.input_test_data()
    print(len(cases))
    for i in cases:
        print(i)
