import os

from util.client import client

params = {
    "getLogs": False,  # 是否获取操作日志
    "id": "",  # 购物有礼活动id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_shoppedGift_get(params=params, headers=headers):
    """
    获取购物有礼活动信息
    /mgmt/prmt/shoppedGift/get

    参数说明:
    - getLogs: 是否获取操作日志
    - id: 购物有礼活动id
    """

    url = "/mgmt/prmt/shoppedGift/get"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
