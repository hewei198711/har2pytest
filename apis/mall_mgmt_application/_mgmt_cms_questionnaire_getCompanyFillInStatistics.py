import os

from util.client import client

params = {
    "projectKey": "",  # 问卷key
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_questionnaire_getCompanyFillInStatistics(params=params, headers=headers):
    """
    问卷答案按分公司地区统计
    /mgmt/cms/questionnaire/getCompanyFillInStatistics

    参数说明:
    - projectKey: 问卷key
    """

    url = "/mgmt/cms/questionnaire/getCompanyFillInStatistics"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
