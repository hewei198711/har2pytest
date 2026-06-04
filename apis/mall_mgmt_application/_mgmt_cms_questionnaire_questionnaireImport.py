import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_cms_questionnaire_questionnaireImport(headers=headers):
    """
    问卷导入
    /mgmt/cms/questionnaire/questionnaireImport
    """

    url = "/mgmt/cms/questionnaire/questionnaireImport"
    with client.post(url=url, headers=headers) as r:
        return r
