import os
def generate_code_template(file_name,casename=None,yaml_name=None,fixtrue=''):
    """
    :param file_name: 测试文件的名字
    :param casename:  测试文件的类名
    :param yaml_name: 测试用例的名字
    :param fixtrue:   前置后置夹具，如果没有可以不用填写
    :return:
    """
    template = f'''
import os
import pytest
from common.yaml_util import YamlUtil
from common.api_util import RequestUtil

class Test_{casename}:
    @pytest.mark.parametrize('caseinfo',YamlUtil().read_testcase_yaml("{yaml_name}"))
    def test_{casename}(self,caseinfo{fixtrue}):
        RequestUtil().gjz(**caseinfo)

if __name__ == '__main__':
    pytest.main(['-vs','{file_name}'])
    os.system("allure generate ../temp -o ../report --clean")
    '''


    code = template.format(file_name=file_name, casename=casename, yaml_name=yaml_name,fixtrue=fixtrue)
    return code


def save_code_template(file_name, code):
    file_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/testsuite/' + file_name  # 设置保存文件的文件夹路径
    with open(file_path, 'w') as file:
        file.write(code)
    print('代码模板已保存到:', file_path)

if __name__ == '__main__':
    file_name='test_'+input('请输入测试文件名:')+'.py'
    casename=input('请输入测试文件的类名:')
    yaml_name=input('请输入测试用例名:')+'.yaml'
    fixtrue=input('你是否要添加前置或后置夹具,如果是请填写方法名:')
    if fixtrue=='':
        code_template = generate_code_template(file_name, casename,yaml_name)
    else:
        fixtrue=','+fixtrue
        code_template = generate_code_template(file_name, casename, yaml_name, fixtrue)
    save_code_template(file_name, code_template)
