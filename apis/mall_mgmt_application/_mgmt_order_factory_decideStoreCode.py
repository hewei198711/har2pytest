import os

from util.client import client

params = {
    "storeCode": "",  # storeCode
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_factory_decideStoreCode(params=params, headers=headers):
    """
    根据服务中心编码判断是否为正式网点
    /mgmt/order/factory/decideStoreCode

    参数说明:
    - storeCode: storeCode
    """

    url = "/mgmt/order/factory/decideStoreCode"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
