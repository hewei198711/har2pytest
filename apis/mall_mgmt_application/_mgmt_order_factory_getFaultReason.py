import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_factory_getFaultReason(headers=headers):
    """
    获取故障原因
    /mgmt/order/factory/getFaultReason
    """

    url = "/mgmt/order/factory/getFaultReason"
    with client.get(url=url, headers=headers) as r:
        return r
