import os

from util.client import client

data = {
    "id": 0,  # 问卷id
    "releaseStatus": 0,  # 发布状态  3：开始发布; 4：停止答题
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_questionnaire_changeReleaseStatus(data=data, headers=headers):
    """
    (问卷)开始发布/停止答题
    /mgmt/cms/questionnaire/changeReleaseStatus

    参数说明:
    - id: 问卷id
    - releaseStatus: 发布状态  3：开始发布; 4：停止答题
    """

    url = "/mgmt/cms/questionnaire/changeReleaseStatus"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
