import os

from util.client import client

data = {
    "projectId": 0,  # 问卷id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_questionnaire_copyQuestionnaire(data=data, headers=headers):
    """
    复制问卷
    /mgmt/cms/questionnaire/copyQuestionnaire

    参数说明:
    - projectId: 问卷id
    """

    url = "/mgmt/cms/questionnaire/copyQuestionnaire"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
