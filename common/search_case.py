import os
import chardet


class search_create():
    def __init__(self, file_path):
        self.file_path = file_path

    def run_cmd(self):
        """运行pict命令，获取到的结果存储到一维数组中"""
        command_run = R'pict ' + self.file_path
        try:
            result_run = os.popen(command_run, mode='r')
            result_list = result_run.readlines()
            return result_list
        except Exception as e:
            return False

    def get_paras(self, temp):
        """通过结果列表的首行，获取参数列表，并存储到一维数组中"""
        if isinstance(temp, list):
            paras = temp[0]
            paras_list = paras.replace('\n', '').split('\t')
            return paras_list
        else:
            return False

    def get_case_list(self, result_lists, paras_lists):
        """将参数名和vlaue组合生成多组用例，存储在数组中"""
        case_list = []
        if isinstance(result_lists, list) and isinstance(paras_lists, list):
            for i in range(1, len(result_lists)):
                dict_case = {}
                list_i = result_lists[i].replace('\n', '').split('\t')
                for j in range(len(paras_lists)):
                    dict_case[paras_lists[j]] = list_i[j]
                case_list.append(dict_case)
            return case_list
        else:
            return False

    def one_step_create(self):
        result_list = self.run_cmd()
        paras_list = self.get_paras(result_list)
        if result_list and paras_list:
            cases = self.get_case_list(result_lists=result_list, paras_lists=paras_list)
            return cases
        else:
            return False

    def change_encode(self):
        """如果文件非ANSI编码，转为ANSI编码"""
        # 简体中文系统下，ANSI 编码代表 GB2312 编码
        with open(self.file_path, 'rb') as f:
            encode = chardet.detect(f.read())
            if encode['encoding'] != 'GB2312':
                print(encode)
            print(type(encode))


if __name__ == '__main__':
    for i in range(1, 10):
        filepath = R'../file_dirs/order%s.txt' % i
        # print(filepath)
        a = search_create(file_path=filepath)
        a.change_encode()
        li = a.one_step_create()
        # print(li)
        print(len(li))
    # for i in li:
    #     print(i)
    # b = search_create(file_path=R'C:\Users\Administrator\Desktop\order1.txt')
    # li2 = b.one_step_create()
    # print(li2)
