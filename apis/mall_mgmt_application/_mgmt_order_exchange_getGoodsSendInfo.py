import os

from util.client import client

params = {
    "exchangeNo": "",  # exchangeNo
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_exchange_getGoodsSendInfo(params=params, headers=headers):
    """
    获取货品回寄信息
    /mgmt/order/exchange/getGoodsSendInfo

    参数说明:
    - exchangeNo: exchangeNo
    """

    url = "/mgmt/order/exchange/getGoodsSendInfo"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
