import os

from util.client import client

data = {
    "idList": [],  # 问卷id列表
    "pageNum": 0,  # 页码
    "pageSize": 0,  # 每页页数
    "title": "",  # 问卷标题
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_questionnaire_queryQuestionnaireLiteList(data=data, headers=headers):
    """
    查询问卷列表lite
    /mgmt/cms/questionnaire/queryQuestionnaireLiteList

    参数说明:
    - idList: 问卷id列表
    - pageNum: 页码
    - pageSize: 每页页数
    - title: 问卷标题
    """

    url = "/mgmt/cms/questionnaire/queryQuestionnaireLiteList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
