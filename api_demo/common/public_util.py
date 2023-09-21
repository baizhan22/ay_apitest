import time
import random
import chardet
from common.yaml_util import YamlUtil
import openpyxl
import datetime
class Public(YamlUtil):
    def end_time(self,name):
        # 获取当前时间
        current_time = datetime.datetime.now()
        # 格式化输出当前时间
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        time = {
            name: formatted_time
        }
        self.write_extract_yaml(time)
        return formatted_time

    import datetime

    def get_time(self):
        # 获取当前时间
        current_time = datetime.datetime.now()

        # 计算上一个月的时间
        previous_month = current_time.month - 1
        if previous_month == 0:
            previous_month = 12
            year = current_time.year - 1
        else:
            year = current_time.year

        # 构建上一个月的时间对象
        previous_month_date = datetime.datetime(year, previous_month, current_time.day, current_time.hour,
                                                current_time.minute, current_time.second)

        # 格式化输出上一个月的时间
        formatted_previous_month = previous_month_date.strftime("%Y-%m-%d %H:%M:%S")

        return formatted_previous_month

    def memo_number(self):
        w=int(self.read_extract_yaml('memoCount'))+1
        print(w)
        return w


    def rdm(self):
        w=random.randint(1,30)
        return int(200)

    def postxl(self,p):
        data={}

        for i in range(0,int(p)):
            key1 = f"items[{i}][province]"
            key2 = f"items[{i}][city]"
            key3 = f"items[{i}][district]"
            key4 = f"items[{i}][town]"
            key5 = f"items[{i}][tid]"
            data[key1] = "上海"
            data[key2] = "上海市"
            data[key3] = "宝山区"
            data[key4] = "高境镇"
            data[key5] = "471149125946179550"

        return data

    def read_excel(self,file_path):
        """
        :param file_path: excel文件路径
        :param workbook   把从excel表中的数据读取出来
        :param data:      把workbook里面的数据以行划分的为一组
        :param title:     把所有的商品标题进行合并展示
        :param status     订单的状态
        :param t:         商品标题
        :param d_sum:     商品数量的总数
        :return:  data,title,status
        """
        workbook = openpyxl.load_workbook(file_path)
        sheet = workbook.active

        data = []
        title=[]
        status=[]

        for row in sheet.iter_rows(values_only=True):
            data.append(list(row))
        t=data[0].index('商品标题')
        su=data[0].index('订单状态')

        for row in data:
            if row[t]=='商品标题':
                continue
            else:
                if row[t] not in title:
                    title.append(row[t])

        for row in data:
            if row[su] == '订单状态':
                continue
            else:
                if row[su] not in status:
                    status.append(row[su])

        d_sum =data[0].index('商品数量')
        s=0
        for row in data:
            if row[d_sum] == '商品数量':
                continue
            else:
                s=s+row[d_sum]
        print(f'商品总数为:{s}个')
        print(title)
        print(status)
        return data,title,status


    def excel_result(self,data,title,status=None,v1=None,v2=None):
        """
        :param data: 所有的订单信息以list数据结构来进行存储的
        :param title: 商品标题
        :param v1:    筛选条件1
        :param v2:    筛选条件2
        :return:
        """
        s = 0
        if v1 != None and v2 != None:
            for row in data:
                if title[v1] in row and status[v2] not in row:
                    print(row)
                    s = s + row[5]
        else:
            for row in data:
                if title[v1] in row :
                    print(row)
                    s = s + row[5]
        print(f'商品标题为:{title[v1]}')
        print(f'符合条件的商品数量为:{s}个')



    def detect_encoding(self,text):
        """
        :param text: 要检测的数据
        :return:
        """
        # 将字符串转换为字节流
        text_bytes = text.encode()

        result = chardet.detect(text_bytes)
        encoding = result['encoding']
        confidence = result['confidence']

        # 输出结果
        print("编码格式: ", encoding)
        print("可信度: ", confidence)

