import os

from util.client import client

params = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_getWechatChangeDetail(params=params, headers=headers):
    """
    获取微信资料变更详情
    /mgmt/store/getWechatChangeDetail

    参数说明:
    - id: id
    """

    url = "/mgmt/store/getWechatChangeDetail"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
