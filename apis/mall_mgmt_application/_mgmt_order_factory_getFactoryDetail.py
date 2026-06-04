import os

from util.client import client

params = {
    "repairNo": "",  # repairNo
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_factory_getFactoryDetail(params=params, headers=headers):
    """
    获取返厂维修单详情
    /mgmt/order/factory/getFactoryDetail

    参数说明:
    - repairNo: repairNo
    """

    url = "/mgmt/order/factory/getFactoryDetail"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
