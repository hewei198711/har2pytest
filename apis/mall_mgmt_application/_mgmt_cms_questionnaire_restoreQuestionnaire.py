import os

from util.client import client

data = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_questionnaire_restoreQuestionnaire(data=data, headers=headers):
    """
    恢复问卷
    /mgmt/cms/questionnaire/restoreQuestionnaire

    参数说明:
    - id: id
    """

    url = "/mgmt/cms/questionnaire/restoreQuestionnaire"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
