import os

from util.client import client

params = {
    "loginMobile": "",  # loginMobile
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_kos_getAlreadySignUpRecordList(params=params, headers=headers):
    """
    查询卡号已报名纪录
    /mgmt/cms/kos/getAlreadySignUpRecordList

    参数说明:
    - loginMobile: loginMobile
    """

    url = "/mgmt/cms/kos/getAlreadySignUpRecordList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
