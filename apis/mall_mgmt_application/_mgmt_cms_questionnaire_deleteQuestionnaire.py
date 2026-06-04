import os

from util.client import client

data = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_questionnaire_deleteQuestionnaire(data=data, headers=headers):
    """
    删除问卷
    /mgmt/cms/questionnaire/deleteQuestionnaire

    参数说明:
    - id: id
    """

    url = "/mgmt/cms/questionnaire/deleteQuestionnaire"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
