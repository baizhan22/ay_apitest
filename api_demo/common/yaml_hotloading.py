import json
import jsonpath
from common.public_util import Public


class Hot_Loading:

    def loading_ccnfig(self,**kwargs):
        """
        :param index:字符的起始位置
        :param end:  字符的结束位置
        :param v:    以index开始到end+1结束这个范围内的所有字符
        :param name: 函数的方法名字
        :param values: 括号内的字符
        :param values_new: 把括号内的字符以逗号为分割，分割成多个参数
        :param str_data: 已经热加载完成的数据再通过字符串替换的方式替换已经的字符
        :param kwargs :  把str_data转换为json格式的数据
        :return: 把已经处理好的kwargs数据返回
        """
        data_type=type(kwargs)
        if isinstance(kwargs,dict) or isinstance(kwargs,list):
            str_data=json.dumps(kwargs)
        else:
            str_data=str(kwargs)
        for i in range(1,str_data.count('${')+1):
            if '${' in str_data and '}' in str_data:
                index=str_data.index("${")
                end=str_data.index('}',index)
                v=str_data[index:end+1]
                name=v[2:v.index('(')]
                values=v[v.index('(')+1:v.index(')')]
                values_new = values.split(",")
                if values_new[0] !='':
                    new_value=getattr(Public(),name)(*values_new)
                    if type(new_value) == list:
                        str_data = str_data.replace(v, str(new_value[0]))
                    else:
                        str_data = str_data.replace(v, str(new_value))
                else:
                    new_value = getattr(Public(), name)()
                    if type(new_value)==list:
                        str_data = str_data.replace(v, str(new_value[0]))
                    else:
                        str_data = str_data.replace(v, str(new_value))
        if isinstance(kwargs, dict) or isinstance(kwargs, list):
            kwargs= json.loads(str_data)
        else:
            kwargs=str_data
        return kwargs

    def jsonpth_config(self,respons,**kwargs):
        """
        :param respons: 接口的响应结果
        :param kwargs:  yaml内的测试用例数据
        :param extract  判断这个测试用例里面有没有extract参数，如果有就进行数据提取
        :param w: 通过jsonpath的方式进行路径定位
        :param Public().write_extract_yaml({key:w[0]}): 把提取出来的数据保存到extract.yaml文件中，做接口关联
        :return: 如果没有extract参数的话那么就返回None这个状态码
        """
        if kwargs.get('extract') !=None:
            for i in kwargs.get('extract'):
                for key,value in i.items():
                    if '$.' in value:
                        w=jsonpath.jsonpath(respons.json(),value)
                        Public().write_extract_yaml({key:w[0]})
            return True
        else:
            return False