import os

from util.client import client

data = {
    "checkRemarks": "",  # 审核意见
    "id": 0,  # id
    "questionnaireStatus": 0,  # 审核状态 0：审核通过;3 审核不通过
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_questionnaire_checkQuestionnaire(data=data, headers=headers):
    """
    审核问卷
    /mgmt/cms/questionnaire/checkQuestionnaire

    参数说明:
    - checkRemarks: 审核意见
    - id: id
    - questionnaireStatus: 审核状态 0：审核通过;3 审核不通过
    """

    url = "/mgmt/cms/questionnaire/checkQuestionnaire"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
