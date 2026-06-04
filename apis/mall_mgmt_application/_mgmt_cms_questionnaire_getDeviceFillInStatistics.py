import os

from util.client import client

params = {
    "projectKey": "",  # 问卷key
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_questionnaire_getDeviceFillInStatistics(params=params, headers=headers):
    """
    问卷答案按登录设备统计
    /mgmt/cms/questionnaire/getDeviceFillInStatistics

    参数说明:
    - projectKey: 问卷key
    """

    url = "/mgmt/cms/questionnaire/getDeviceFillInStatistics"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
