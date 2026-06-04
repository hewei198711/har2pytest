import os

from util.client import client

data = {
    "pageNum": 0,  # 页码
    "pageSize": 0,  # 每页页数
    "title": "",  # 问卷名称
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_questionnaire_getQuestionnaireLinkList(data=data, headers=headers):
    """
    获取问卷关联列表
    /mgmt/cms/questionnaire/getQuestionnaireLinkList

    参数说明:
    - pageNum: 页码
    - pageSize: 每页页数
    - title: 问卷名称
    """

    url = "/mgmt/cms/questionnaire/getQuestionnaireLinkList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
