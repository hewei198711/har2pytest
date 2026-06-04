import os

from util.client import client

params = {
    "repairNo": "",  # repairNo
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_factory_getFactoryStatus(params=params, headers=headers):
    """
    获取返修单状态变更列表
    /mgmt/order/factory/getFactoryStatus

    参数说明:
    - repairNo: repairNo
    """

    url = "/mgmt/order/factory/getFactoryStatus"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
