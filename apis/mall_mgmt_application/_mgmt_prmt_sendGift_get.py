import os

from util.client import client

params = {
    "getLogs": False,  # 是否获取操作记录
    "id": "",  # 活动id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_sendGift_get(params=params, headers=headers):
    """
    获取活动详情(详情或编辑回显)
    /mgmt/prmt/sendGift/get

    参数说明:
    - getLogs: 是否获取操作记录
    - id: 活动id
    """

    url = "/mgmt/prmt/sendGift/get"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
