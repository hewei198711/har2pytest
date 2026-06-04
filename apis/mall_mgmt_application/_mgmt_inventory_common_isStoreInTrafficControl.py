import os

from util.client import client

params = {
    "storeCode": "",  # storeCode
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_common_isStoreInTrafficControl(params=params, headers=headers):
    """
    店铺是否处于交通管控
    /mgmt/inventory/common/isStoreInTrafficControl

    参数说明:
    - storeCode: storeCode
    """

    url = "/mgmt/inventory/common/isStoreInTrafficControl"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
