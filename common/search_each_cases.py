import xlrd
from pypinyin import lazy_pinyin
import random
import string
from common.base_data import base_data

aa = {'para': '客户昵称',
      'type': 'input',
      'input_rules': "{'input_char': 'NUM', 'input_len': '10', 'input_like': 'y', 'deal_space':'y'}",
      'target': '432'
      }

bb = {'para': '订单金额',
      'type': 'range',
      'input_rules': "{'data_type': 'num_data', 'unit': '0.01'}",
      'target': '99'
      }

cc = {'para': '创建时间',
      'type': 'range',
      'input_rules': "{'data_type': 'time_data', 'unit': '秒', }",
      'target': '2021-01-06 23:15:23'
      }
# 时间类的范围为：年、月、日、时、分、秒


class search_case(base_data):
    def __init__(self, temp_dict):
        self.target = temp_dict['target']
        self.input_rules = eval(temp_dict['input_rules'])
        self.type = temp_dict['type']
        self.para = temp_dict['para']

    def sp_test_case(self, sp_list, temp):
        """用于参数与特殊字符组合生成测试数据,然后生成用例列表,用于字符类型限制的测试数据生成
        :sp_list：特殊字符列表
        :temp：测试目标
        """
        case_list = []
        if isinstance(sp_list, list):
            for i in sp_list:
                temp_i = str(temp)[0] + str(i)
                temp_j = str(i) + str(temp)
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

    def input_test_case(self):
        """文本输入类的用例数据生成"""
        if self.type.lower() == 'input':
            case_list = []
            # 将目标作为测试数据，期望结果为正确
            right_case = self.be_case(test_data=self.target, result='succ')
            case_list.append(right_case)
            if 'input_char' in self.input_rules.keys():
                print("生成字符限制类用例...")
                if self.input_rules['input_char'].lower() == 'cn':
                    # 思考这里如何简化，当指定一种类型时，自动将另外三中错误字符生成用用例，
                    # 是否需要用到for循环去生成，还是把上面的value分装在字典还是什么里面
                    cn_use = [self.cn_to_pinyin(self.target), self.en_test_data(), self.num_test_data(),
                              self.sp_test_data()]
                    case_list = self.travel_data_case(ca_list=case_list, def_list=cn_use)

                elif self.input_rules['input_char'].lower() == 'en':
                    # 后面要考虑加入大小写
                    en_use = [self.cn_test_data(), self.num_test_data(), self.sp_test_data()]
                    case_list = self.travel_data_case(ca_list=case_list, def_list=en_use)

                elif self.input_rules['input_char'].lower() == 'num':
                    num_use = [self.cn_test_data(), self.en_test_data(), self.sp_test_data()]
                    case_list = self.travel_data_case(ca_list=case_list, def_list=num_use)

                else:
                    print("无法生成字符校验无效等价类用例，请检查<input_char>值是否为cn/en/num ！")

            if 'input_len' in self.input_rules.keys():
                print("生成长度限制类用例...")
                # 长度校验主要通过边界值法进行创建，一半规定输入最多限制输入位数进行搜索，不会限制最少输入位数
                try:
                    max_len = eval(self.input_rules['input_len'])
                    if isinstance(max_len, int):
                        less_len = max_len - 1
                        over_len = max_len + 1
                        case_len_1 = self.be_case(test_data=max_len*self.target[0], result='succ')
                        case_len_2 = self.be_case(test_data=less_len*self.target[0], result='succ')
                        case_len_3 = self.be_case(test_data=over_len*self.target[0])
                        case_list.extend([case_len_1, case_len_2, case_len_3])
                    else:
                        print('无法生成长度校验用例，max_len非数字，请检查<input_len>值是否为数字字符串！')
                except Exception as e:
                    print(e)

            if 'input_like' in self.input_rules.keys():
                print("生成模糊搜索限制类用例...")
                # y表示支持模糊搜索，n表示精确搜索
                if self.input_rules['input_like'].lower() == 'y':
                    case_like_1 = self.be_case(test_data=self.target[:-1], result='succ')
                    case_like_2 = self.be_case(test_data=self.target[0], result='succ')
                    case_like_3 = self.be_case(test_data=self.target + self.cn_test_data())
                    case_list.extend([case_like_1, case_like_2, case_like_3])
                elif self.input_rules['input_like'].lower() == 'n':
                    case_like_4 = self.be_case(test_data=self.target[:-1])
                    case_like_5 = self.be_case(self.target * 2)
                    case_like_6 = self.be_case(self.target + self.cn_test_data())
                    case_list.extend([case_like_4, case_like_5, case_like_6])
                else:
                    print('无法生成精确/模糊搜索用例，请检查<input_like>是否为 y 或 n ')

            if 'deal_space' in self.input_rules.keys():
                print("生成过滤空格限制类用例...")
                # y表示会过滤空格，n表示不会过滤空格
                if self.input_rules['deal_space'].lower() == 'y':
                    case_space_1 = self.be_case(self.target + ' ', result='succ')
                    case_space_2 = self.be_case(' ' + self.target, result='succ')
                    case_space_4 = self.be_case(' ', result='succ')
                    case_list.extend([case_space_1, case_space_2, case_space_4])
                    if len(self.target) > 1:
                        case_space_3 = self.be_case(self.add_space(self.target), result='succ')
                        case_list.append(case_space_3)

                elif self.input_rules['deal_space'].lower() == 'n':
                    case_space_1 = self.be_case(self.target + ' ')
                    case_space_2 = self.be_case(' ' + self.target)
                    case_space_3 = self.be_case(' ')
                    case_list.extend([case_space_1, case_space_2, case_space_3])
                    if len(self.target) > 1:
                        case_space_4 = self.be_case(self.add_space(self.target))
                        case_list.append(case_space_4)

            return case_list
        else:
            print('非input类型的输入')

    def range_test_case(self):
        """输入范围类的用例生成"""
        if self.type.lower() == 'range':
            case_list = []
            if self.input_rules['data_type'].lower() == 'num_data':
                unit = eval(self.input_rules['unit'])
                over_data = self.sum_data(self.target, unit)
                over_more = self.sum_data(self.target, unit*2)
                less_data = self.subtr_data(self.target, unit)
                less_more = self.subtr_data(self.target, unit*2)
                case_1 = self.be_case({'start': less_data, 'end': over_data}, result='succ')
                case_2 = self.be_case({'start': less_data, 'end': ''}, result='succ')
                case_3 = self.be_case({'start': '', 'end': over_data}, result='succ')
                case_4 = self.be_case({'start': less_more, 'end': less_data})
                case_5 = self.be_case({'start': over_data, 'end': over_more})
                case_6 = self.be_case({'start': over_data, 'end': ''})
                case_7 = self.be_case({'start': '', 'end': less_data})
                case_8 = self.be_case({'start': over_data, 'end': less_data})
                for i in range(1, 9):



                pass
        else:
            print("非range类输入")



if __name__ == '__main__':
    # pass
    case = search_case(temp_dict=aa)
    cases = case.input_test_case()
    print(len(cases))
    for i in cases:
        print(i)
