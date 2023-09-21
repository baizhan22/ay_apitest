from common.assert_equals import Equals
from common.assert_contains import Contains
from common.api_logging import Logging
from common.feishu import fs
class Asserts():
    def __init__(self):
        self.log=Logging()
        self.fs=fs()
    def method_assert(self,respons,asserts,kwargs):
        """
        :param respons: 接口响应的结果
        :param asserts: 要进行断言的数据
        :param report: 选择断言方式后进行断言并把结果收集到列表中然后在预处理模块进行最后的断言
        :return:
        """

        result=[]
        for i in asserts:
            for key,value in i.items():
                p=[respons,value,kwargs]
                assert_result=getattr(Asserts(),key)(p)
                for s in assert_result:
                    assert_result=s[0]
                    result.append(assert_result)

        return result



    def asserts_preprocess(self,respons,asserts,kwargs):
        """
        :param respons: 接口响应的结果
        :param asserts: 要进行断言的数据
        :return: raise断言失败后把捕获到的异常进行上抛
        """
        w=self.method_assert(respons,asserts,kwargs)
        assert_result=[]
        for i in w:
            if True==i.get('assert_result'):
                self.log.log_aserrt_result(i.get('Expected_result'), i.get('actual_result'), i.get('assert_result'))
            else:
                assert_result.append(i.get('assert_result'))
                self.log.log_aserrt_result(i.get('Expected_result'), i.get('actual_result'), i.get('assert_result'))
        try:
            assert  False not in assert_result
            # self.fs.send_feishu_card(d=kwargs['api_name'], method=kwargs['request']['method'],urls=kwargs['request']['url'], respons="成功")
        except:
            # self.log.init_logger().error(f'响应结果{respons.json()}')
            self.fs.send_feishu_card(d=kwargs['api_name'],api_info=kwargs['api_info'],method=kwargs['request']['method'],urls=kwargs['request']['url'],respons="失败")
            raise

    def equals(self,kwargs):
        """
        相等断言
        :param kwargs: 里面包含了respons参数和asserts参数
        :return: result把断言结果返回给上级方法
        """
        eq=Equals()
        result=[]
        for key,value in kwargs[1].items():
            p=[kwargs[0],value]
            equals_result=getattr(eq,key)(p)
            result.append(equals_result)
        return result



    def contains(self,kwargs):
        """
        包含函数
        :param kwargs: 里面包含了respons参数和asserts参数
        :return: result把断言结果返回给上级方法
        """
        eq = Contains()
        result = []
        for key, value in kwargs[1].items():
            p = [kwargs[0], value]
            equals_result = getattr(eq, key)(p)
            result.append(equals_result)
        # if 'text2' in kwargs[1].keys() :
        #     return result[0]
        # else:
        #     return result
        return result[0]