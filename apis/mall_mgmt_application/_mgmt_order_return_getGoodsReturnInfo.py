import os

from util.client import client

params = {
    "returnNo": "",  # returnNo
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_return_getGoodsReturnInfo(params=params, headers=headers):
    """
    获取货品退回信息
    /mgmt/order/return/getGoodsReturnInfo

    参数说明:
    - returnNo: returnNo
    """

    url = "/mgmt/order/return/getGoodsReturnInfo"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
