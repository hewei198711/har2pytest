import os

from util.client import client

params = {
    "isOption": "",  # 是否选择题 1.是 不传或其他都为否
    "projectKey": "",  # 问卷key
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_questionnaire_getQuestionList(params=params, headers=headers):
    """
    查询问卷题目
    /mgmt/cms/questionnaire/getQuestionList

    参数说明:
    - isOption: 是否选择题 1.是 不传或其他都为否
    - projectKey: 问卷key
    """

    url = "/mgmt/cms/questionnaire/getQuestionList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
