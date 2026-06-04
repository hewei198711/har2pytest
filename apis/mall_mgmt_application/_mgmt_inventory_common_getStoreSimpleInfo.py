import os

from util.client import client

params = {
    "storeCode": "",  # storeCode
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_common_getStoreSimpleInfo(params=params, headers=headers):
    """
    获取服务中心简单信息
    /mgmt/inventory/common/getStoreSimpleInfo

    参数说明:
    - storeCode: storeCode
    """

    url = "/mgmt/inventory/common/getStoreSimpleInfo"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
