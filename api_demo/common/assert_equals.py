import jsonpath
class Equals:

    def wh(self,Expected_result,actual_result,assert_result,error=None):
        resluts = []
        whh_result={
            "Expected_result":Expected_result,
            'actual_result':actual_result,
            'assert_result':assert_result
        }

        resluts.append(whh_result)
        return resluts

    def status_code(self,kwargs):
        """
        对响应的接口进行状态码断言
        :param kwargs:
        :return:
        """
        try:
            assert kwargs[0].status_code==int(kwargs[1])
            resluts=self.wh(Expected_result=f"响应码为{kwargs[1]}",actual_result=f"响应码为{kwargs[0].status_code}",assert_result=True)
        except AssertionError as e:
            resluts=self.wh(Expected_result=f"响应码为{kwargs[1]}", actual_result=f"响应码为{kwargs[0].status_code}", assert_result=False)
        return resluts

    def code(self,kwargs):
        try:
            assert kwargs[0].json()['code']== int(kwargs[1])
            resluts = self.wh(Expected_result=f"状态码为{kwargs[1]}", actual_result=f"状态码为{kwargs[0].json()['code']}", assert_result=True)
        except AssertionError as e:
            resluts = self.wh(Expected_result=f"状态码为{kwargs[1]}", actual_result=f"状态码为{kwargs[0].json()['code']}", assert_result=False)
        return resluts

    def api_time(self,kwargs):
        """
        对响应的接口进行响应时间断言
        :param kwargs:
        :return:
        """
        try:
            assert kwargs[0].elapsed.total_seconds() <= kwargs[1]
            resluts = self.wh(Expected_result=kwargs[1], actual_result=f"响应时间{kwargs[0].elapsed.total_seconds()*1000}ms小于{kwargs[1]}ms", assert_result=True)
        except AssertionError as e:
            resluts = self.wh(Expected_result=kwargs[1], actual_result=f"响应时间{kwargs[0].elapsed.total_seconds()*1000}ms大于{kwargs[1]}ms", assert_result=False)

        return resluts

    def  type_NotNone(self,kwargs):
        try:
            assert kwargs[0].json()[kwargs[1]] != ' '
            resluts = self.wh(Expected_result=f"查询字段为{kwargs[1]}", actual_result="该字段存在数据，不为空", assert_result=True)
        except AssertionError as e:
            resluts = self.wh(Expected_result=f"查询字段为{kwargs[1]}", actual_result="该字段存在数据，不为空", assert_result=False)
        return resluts

    def  message(self,kwargs):
        try:
            assert str(kwargs[0].json()['message']) == str(kwargs[1])
            resluts = self.wh(Expected_result=f"{kwargs[1]}", actual_result=f"查询结果为{kwargs[0].json()['message']}", assert_result=True)
        except AssertionError as e:
            resluts = self.wh(Expected_result=f"{kwargs[1]}", actual_result=f"查询结果为{kwargs[0].json()['message']}", assert_result=False)
        return resluts

    def sub_code(self, kwargs):
        try:
            # print(kwargs[1])
            print(kwargs[0].json()['sub_code'])
            assert str(kwargs[0].json()['sub_code']) == str(kwargs[1])
            resluts = self.wh(Expected_result=f"{kwargs[1]}", actual_result=f"查询结果为{kwargs[0].json()['sub_code']}",assert_result=True)
        except AssertionError as e:
            resluts = self.wh(Expected_result=f"{kwargs[1]}", actual_result=f"查询结果为{kwargs[0].json()['sub_code']}",assert_result=False)
        return resluts


