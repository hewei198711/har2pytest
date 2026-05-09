import os

from util.client import client

params = {
    "orderSn": "",  # orderSn
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_dis_mortgage_returnOrder_appDetailSn(params=params, headers=headers):
    """
    APP押货退详情SN
    /appStore/store/dis/mortgage/returnOrder/appDetailSn

    参数说明:
    - orderSn: orderSn
    """

    url = "/appStore/store/dis/mortgage/returnOrder/appDetailSn"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
