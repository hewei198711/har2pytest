import os

from util.client import client

params = {
    "repairNo": "",  # repairNo
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_order_store_factory_getFactoryStatus(params=params, headers=headers):
    """
    获取返修单状态变更列表
    /appStore/order/store/factory/getFactoryStatus

    参数说明:
    - repairNo: repairNo
    """

    url = "/appStore/order/store/factory/getFactoryStatus"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
