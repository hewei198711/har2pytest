import os

from util.client import client

data = {
    "importText": "",  # 问卷导入文本
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_questionnaire_textRecognition(data=data, headers=headers):
    """
    问卷导入文本识别
    /mgmt/cms/questionnaire/textRecognition

    参数说明:
    - importText: 问卷导入文本
    """

    url = "/mgmt/cms/questionnaire/textRecognition"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
