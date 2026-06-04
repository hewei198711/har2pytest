import os

from util.client import client

params = {
    "projectKey": "",  # projectKey
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_questionnaire_getLinkQuestionnaire(params=params, headers=headers):
    """
    获取关联问卷
    /mgmt/cms/questionnaire/getLinkQuestionnaire

    参数说明:
    - projectKey: projectKey
    """

    url = "/mgmt/cms/questionnaire/getLinkQuestionnaire"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
