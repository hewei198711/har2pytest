import os

from util.client import client

params = {
    "storeCode": "",  # storeCode
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_disInventoryQuota_getQuota(params=params, headers=headers):
    """
    查询新增/编辑审核类型且审核通过的库存限额
    /appStore/store/disInventoryQuota/getQuota

    参数说明:
    - storeCode: storeCode
    """

    url = "/appStore/store/disInventoryQuota/getQuota"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
