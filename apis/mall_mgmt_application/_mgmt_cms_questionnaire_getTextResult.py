import os

from util.client import client

data = {
    "pageNum": 0,  # 页码
    "pageSize": 0,  # 每页页数
    "questionKey": "",  # 问题key
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_questionnaire_getTextResult(data=data, headers=headers):
    """
    获取问卷统计的填空题答案分页
    /mgmt/cms/questionnaire/getTextResult

    参数说明:
    - pageNum: 页码
    - pageSize: 每页页数
    - questionKey: 问题key
    """

    url = "/mgmt/cms/questionnaire/getTextResult"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
