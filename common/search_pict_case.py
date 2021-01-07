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

    def check_encode(self):
        """检查当前文件的编码"""
        with open(self.file_path, 'rb') as f1:
            content = f1.read()
            # print(type(content)),返回类型为bytes
            # chardet.detect()函数会返回当前读取对象的编码
            encode = chardet.detect(content)
            f1.close()
            file_encode = encode['encoding']
        return file_encode

    def change_encode(self):
        """如果文件非ANSI编码，转为ANSI编码"""
        # 简体中文系统下，ANSI 编码代表 GB2312 编码
        file_encode = self.check_encode()
        # print('file_encode:', file_encode)

        if file_encode != 'GB2312':
            # 目前只能把utf-8文件转为gb2312，其他编码方式暂时不行
            print(self.file_path + '文件编码方式不正确,准备进行转编码...')
            # 获取文件文本内容
            with open(self.file_path, 'rb') as f:
                content = f.read()
                f.close()
            if file_encode == 'utf-8':
                # 因为指定了写的编码方式：encoding='GB2312'，需要将bytes类型的content转为str后，才能顺利写入文件
                con = str(content, encoding='utf-8')
                with open(self.file_path, 'w', encoding='GB2312') as fw:
                    try:
                        fw.write(con)
                        fw.close()
                        print('编码成功')
                    except Exception as e:
                        print('文件编码失败', e)
                        return False
            else:
                print(self.file_path, '暂时无法编码')
                return False
        else:
            # print('编码方式正确')
            pass

if __name__ == '__main__':
    """
    for i in range(1, 10):
        filepath = R'../file_dirs/order%s.txt' % i
        # print(filepath)
        a = search_create(file_path=filepath)
        if a.change_encode() is not False:
        # a.change_encode()
            li = a.one_step_create()
            # print(li)
            print(len(li))
        else:
            print('文件编码时出现错误')
    """
    # for i in li:
    #     print(i)
    b = search_create(file_path=R'../file_dirs/order1.txt')
    if b.change_encode() is not False:
        li2 = b.one_step_create()
    # print(li2)
        print(len(li2))
        for j in li2:
            print(j)
    else:
        print("出错了")