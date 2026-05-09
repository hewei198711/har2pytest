import os

from util.client import client

params = {
    "orderSn": "",  # orderSn
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_mobile_returnOrder_sn_orderSn(params=params, headers=headers):
    """
    SN押货退货详情
    /appStore/mobile/returnOrder/sn/{orderSn}

    参数说明:
    - orderSn: orderSn
    """

    url = f"/appStore/mobile/returnOrder/sn/{params['orderSn']}"
    with client.get(url=url, headers=headers) as r:
        return r
