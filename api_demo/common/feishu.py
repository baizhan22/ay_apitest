
import requests
import json

class fs():
    def send_feishu_card(self,d,api_info,method,urls,respons):
        """
        :param d: 接口名称
        :param method: 请求方式
        :param body: 请求参数
        :param Expected_result: 预期结果
        :param actual_result: 实际结果
        :param respons: 接口响应结果
        :return:
        """
        print('1')
        url = ''

        # 构建卡片内容
        card_content = {
            "config": {
                "wide_screen_mode": True
            },
            "header": {
                "title": {
                    "tag": "plain_text",
                    "content": "自动化测试错误报警"
                }
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "tag": "plain_text",
                        "content": f"接口名称:{d}"
                    }
                },
                {
                    "tag": "div",
                    "text": {
                        "tag": "plain_text",
                        "content": f"用例信息:{api_info}"
                    }
                },
                {
                    "tag": "div",
                    "text": {
                        "tag": "plain_text",
                        "content": f"请求地址:{urls}"
                    }
                },
                {
                    "tag": "div",
                    "text": {
                        "tag": "plain_text",
                        "content": f"请求方式:{method}"
                    }
                },

                {
                    "tag": "div",
                    "text": {
                        "tag": "plain_text",
                        "content": f"断言结果:{respons}"
                    }
                },

                {
                    "tag": "hr"
                },
                {
                    "tag": "note",
                    "elements": [
                        {
                            "tag": "plain_text",
                            "content": "这是一条备注信息"
                        }
                    ]
                }
            ]
        }

        headers = {'Content-Type': 'application/json'}
        data = {
            'msg_type': 'interactive',
            'card': card_content
        }
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            return '卡片发送成功！'
        else:
            return '卡片发送失败！'


