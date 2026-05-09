import os

from util.client import client

params = {
    "month": "",  # month
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _appStore_deliveryServiceCharge_list(params=params, headers=headers):
    """
    配送服务费列表
    /appStore/deliveryServiceCharge/list

    参数说明:
    - month: month
    """

    url = "/appStore/deliveryServiceCharge/list"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
