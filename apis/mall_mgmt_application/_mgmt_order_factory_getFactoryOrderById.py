import os

from util.client import client

params = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_factory_getFactoryOrderById(params=params, headers=headers):
    """
    根据ID获取返修单
    /mgmt/order/factory/getFactoryOrderById

    参数说明:
    - id: id
    """

    url = "/mgmt/order/factory/getFactoryOrderById"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
