import os

from util.client import client

params = {
    "orderSn": "",  # orderSn
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_dis_mortgage_returnOrder_detailSn_orderSn(params=params, headers=headers):
    """
    押货退详情SN
    /appStore/store/dis/mortgage/returnOrder/detailSn/{orderSn}

    参数说明:
    - orderSn: orderSn
    """

    url = f"/appStore/store/dis/mortgage/returnOrder/detailSn/{params['orderSn']}"
    with client.get(url=url, headers=headers) as r:
        return r
