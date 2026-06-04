import os

from util.client import client

params = {
    "columnQuestionKey": "",  # 问题key(列)
    "rowQuestionKey": "",  # 问题key(行)
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_questionnaire_crossOverAnalysis(params=params, headers=headers):
    """
    问卷交叉分析
    /mgmt/cms/questionnaire/crossOverAnalysis

    参数说明:
    - columnQuestionKey: 问题key(列)
    - rowQuestionKey: 问题key(行)
    """

    url = "/mgmt/cms/questionnaire/crossOverAnalysis"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
