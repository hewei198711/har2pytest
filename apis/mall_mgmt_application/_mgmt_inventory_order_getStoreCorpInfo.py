import os

from util.client import client

params = {
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_order_getStoreCorpInfo(params=params, headers=headers):
    """
    获取服务中心仓库信息
    /mgmt/inventory/order/getStoreCorpInfo

    参数说明:
    - storeCode: 服务中心编号
    """

    url = "/mgmt/inventory/order/getStoreCorpInfo"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
