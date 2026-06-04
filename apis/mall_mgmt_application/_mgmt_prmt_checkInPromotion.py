import os

from util.client import client

params = {
    "serialNo": "",  # serialNo
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_checkInPromotion(params=params, headers=headers):
    """
    校验商品是否在活动中
    /mgmt/prmt/checkInPromotion

    参数说明:
    - serialNo: serialNo
    """

    url = "/mgmt/prmt/checkInPromotion"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
