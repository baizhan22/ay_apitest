from common.yaml_util import YamlUtil
import requests as  rs
# -*- coding: utf-8 -*-
from common.api_logging import Logging
from common.api_assert import Asserts
from common.yaml_hotloading import Hot_Loading
from common.config import api_config
class RequestUtil(YamlUtil):
    def __init__(self):
        self.session=rs.Session()
        self.log=Logging()
        self.asserts=Asserts()

    def request_method(self, **kwargs):
        """
        对接口发起请求
        :param kwargs:
        :return:
        """
        kwargs['request']=api_config(kwargs['request'])
        rq = kwargs['request']

        asserts = kwargs['assert']
        if rq.get('data'):
            if isinstance(rq['data'],str) :
                rq['data'] = eval(rq['data'])
        elif rq.get('params'):
            if isinstance(rq['params'], str):
                rq['params'] = eval(rq['params'])
        self.log.log_INFO(**kwargs)
        respons = self.session.request(**rq)
        respons_extract=Hot_Loading().jsonpth_config(respons=respons,**kwargs)
        if respons_extract !=False:
            self.log.init_logger().info('参数提取完成')
        self.asserts.asserts_preprocess(respons,asserts,kwargs)

    #检测yaml文件格式
    def gjz(self,**kwargs):
        """
        对YAML文件内的数据进行格式检测
        然后再进行热加载处理
        :param kwargs:
        :return:
        """
        if 'request' in kwargs.keys() and 'assert' in kwargs.keys() and 'api_name' in kwargs.keys():
            rq = kwargs['request']
            if 'url' in rq.keys() and 'method' in rq.keys():
                self.log.init_logger().info('YAML文件格式检测通过')
                kwargs=Hot_Loading().loading_ccnfig(**kwargs)
                self.log.init_logger().info('YAML文件热加载完成')
                self.request_method(**kwargs)
            else:
                self.log.log_error('POST请求的二级关键字必须包含:url,data')
                assert 1==2
        else:
            self.log.log_error('一级关键字必须包换:name,request,assert')
            assert 1 == 2

