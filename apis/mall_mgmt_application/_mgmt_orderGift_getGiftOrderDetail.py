import os

from util.client import client

params = {
    "orderNo": "",  # orderNo
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_orderGift_getGiftOrderDetail(params=params, headers=headers):
    """
    赠品领取单管理-详情
    /mgmt/orderGift/getGiftOrderDetail

    参数说明:
    - orderNo: orderNo
    """

    url = "/mgmt/orderGift/getGiftOrderDetail"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
