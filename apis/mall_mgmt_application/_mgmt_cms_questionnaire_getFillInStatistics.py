import os

from util.client import client

params = {
    "projectKey": "",  # 问卷key
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_questionnaire_getFillInStatistics(params=params, headers=headers):
    """
    获取问卷的回收统计结果
    /mgmt/cms/questionnaire/getFillInStatistics

    参数说明:
    - projectKey: 问卷key
    """

    url = "/mgmt/cms/questionnaire/getFillInStatistics"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
