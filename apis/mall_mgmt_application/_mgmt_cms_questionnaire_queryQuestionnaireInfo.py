import os

from util.client import client

params = {
    "id": "",  # 问卷id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_questionnaire_queryQuestionnaireInfo(params=params, headers=headers):
    """
    查看问卷
    /mgmt/cms/questionnaire/queryQuestionnaireInfo

    参数说明:
    - id: 问卷id
    """

    url = "/mgmt/cms/questionnaire/queryQuestionnaireInfo"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
