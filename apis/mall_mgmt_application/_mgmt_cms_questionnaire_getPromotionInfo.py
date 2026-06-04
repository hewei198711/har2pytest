import os

from util.client import client

params = {
    "id": "",  # 问卷id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_questionnaire_getPromotionInfo(params=params, headers=headers):
    """
    获取问卷推广信息
    /mgmt/cms/questionnaire/getPromotionInfo

    参数说明:
    - id: 问卷id
    """

    url = "/mgmt/cms/questionnaire/getPromotionInfo"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
