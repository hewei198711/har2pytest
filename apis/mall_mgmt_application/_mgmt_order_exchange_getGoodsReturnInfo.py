import os

from util.client import client

params = {
    "exchangeNo": "",  # exchangeNo
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_exchange_getGoodsReturnInfo(params=params, headers=headers):
    """
    获取货品退回信息
    /mgmt/order/exchange/getGoodsReturnInfo

    参数说明:
    - exchangeNo: exchangeNo
    """

    url = "/mgmt/order/exchange/getGoodsReturnInfo"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
