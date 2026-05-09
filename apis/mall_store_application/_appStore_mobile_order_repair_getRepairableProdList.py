import os

from util.client import client

params = {
    "keyword": "",  # keyword
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_mobile_order_repair_getRepairableProdList(params=params, headers=headers):
    """
    查询可维修商品列表
    /appStore/mobile/order/repair/getRepairableProdList

    参数说明:
    - keyword: keyword
    """

    url = "/appStore/mobile/order/repair/getRepairableProdList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
