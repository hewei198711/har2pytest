import os

from util.client import client

params = {
    "year": "",  # year
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_order_getPerDashExamine(params=params, headers=headers):
    """
    业绩看板-店交付业绩考核
    /appStore/order/getPerDashExamine

    参数说明:
    - year: year
    """

    url = "/appStore/order/getPerDashExamine"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
