import re
class Contains:
    def wh(self, Expected_result, actual_result, assert_result, error=None):
        """
        :param Expected_result: 预期结果
        :param actual_result:   实际结果
        :param assert_result:   断言结果
        :param error:           报错信息
        :return:                返回存储的断言结果
        """

        resluts = []
        whh_result = {
            "Expected_result": Expected_result,
            'actual_result': actual_result,
            'assert_result': assert_result
        }
        resluts.append(whh_result)
        return resluts

    def text1(self,kwargs):
        """
        单个数据时可以使用text1进行包含断言
        :param kwargs:
        :return:
        """
        field_value=''
        results = []
        response_json= kwargs[0].json() # 将响应转换为json，以便后续递归搜索

        for i in kwargs[1]:
            for key, value in i.items():
                try:
                    # 递归搜索JSON对象中的字段
                    def search_field(data, field):
                        if isinstance(data, dict):
                            for key, value in data.items():
                                if key == field:
                                    return value
                                elif isinstance(value, (list, dict)):
                                    result = search_field(value, field)
                                    if result:
                                        return result
                        elif isinstance(data, list):
                            for item in data:
                                if isinstance(item, (list, dict)):
                                    result = search_field(item, field)
                                    if result:
                                        return result

                    # 调用递归函数搜索字段并返回对应的值
                    field_value = search_field(response_json, key)

                    # 断言找到的字段值与预期值是否相等
                    assert field_value == value, f"JSON field assertion failed: {key} should be {value}, but got {field_value}"
                    result = self.wh(Expected_result=value, actual_result=f'{field_value}',assert_result=False)
                    results.append(result)
                except ValueError:
                    result = self.wh(Expected_result=value, actual_result='在返回结果中没有查询到{}字段'.format(key),assert_result=False)
                    results.append(result)

        return results


    def clean_string(self,value)->str:
        # 去除空格和换行符等不可见字符
        cleaned_value = str(value).replace(',', '')  # 删除逗号
        cleaned_value=cleaned_value.replace('}','')  # 删除括号
        cleaned_value = re.sub(r'\s+', '', cleaned_value)  # 去除其他不可见字符
        return cleaned_value

    def text2(self, kwargs):
        """
        :param kwargs[0]:接口的响应数据
        :param kwargs[1]:要进行断言的数据
        :return:
        """
        results = []
        response_str = str(kwargs[0].json())  # 将响应转换为字符串，以便后续使用正则表达式

        for i in kwargs[1]:
            for key, value in i.items():
                try:
                    # 查找 key 的索引
                    index = response_str.index(str(key)) + len(str(key))
                    # 查找 value 的索引
                    end = response_str.index(str(value), index) + len(str(value))
                    # 提取子串
                    v = response_str[index:end + 1]
                    m = re.search(r'(:\s*["\']([^"\']+)[\'"])|(:\s*([^"\']+))', v)
                    extracted_value = ''
                    cleaned_extracted_value=''
                    if m:
                        # 匹配双引号内的内容
                        if m.group(2):
                            extracted_value = m.group(2)
                        # 匹配单引号内的内容
                        elif m.group(4):
                            extracted_value = m.group(4)
                        # 没有引号时直接对比
                        elif m.group(5):
                            extracted_value = m.group(5)
                        # 进行字符串清理和规范化
                        cleaned_extracted_value =self.clean_string(extracted_value)
                        cleaned_value = self.clean_string(value)
                        # 判断提取的值是否与 value 相等
                        if cleaned_extracted_value == cleaned_value:
                            # 直接返回一个成功的断言结果
                            result = self.wh(Expected_result=value,actual_result=f'{cleaned_extracted_value}', assert_result=True)
                            results.append(result)
                            continue  # 进行下一个断言
                    # 若代码能够运行到这里，说明提取的值与期望值不相等
                    result = self.wh(Expected_result=value, actual_result=f'{cleaned_extracted_value}',assert_result=False)
                    results.append(result)
                except ValueError:
                    result = self.wh(Expected_result=value, actual_result='在返回结果中没有查询到{}字段'.format(key),assert_result=False)
                    results.append(result)

        return results
