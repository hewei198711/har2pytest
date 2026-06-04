import os

from util.client import client

params = {
    "key": "",  # key
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_loginGift_getImportFailedList(params=params, headers=headers):
    """
    下载登录有礼活动导入顾客失败列表
    /mgmt/prmt/loginGift/getImportFailedList

    参数说明:
    - key: key
    """

    url = "/mgmt/prmt/loginGift/getImportFailedList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
