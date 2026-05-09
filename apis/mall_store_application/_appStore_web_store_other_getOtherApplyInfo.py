import os

from util.client import client

params = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_web_store_other_getOtherApplyInfo(params=params, headers=headers):
    """
    查询其他申请记录
    /appStore/web/store/other/getOtherApplyInfo

    参数说明:
    - id: id
    """

    url = "/appStore/web/store/other/getOtherApplyInfo"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
