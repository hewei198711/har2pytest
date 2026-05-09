import os

from util.client import client

params = {
    "storeCode": "",  # storeCode
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_inventory_mortgageAmount_detailTotalMsg(params=params, headers=headers):
    """
    服务中心账款管理 -- 押货余额详情(综合信息)
    /appStore/store/inventory/mortgageAmount/detailTotalMsg

    参数说明:
    - storeCode: storeCode
    """

    url = "/appStore/store/inventory/mortgageAmount/detailTotalMsg"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
