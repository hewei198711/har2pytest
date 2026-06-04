import os

from util.client import client

data = {
    "addrKeywords": "",  # 关键词
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_saveDeliveryWarnKeywords(data=data, headers=headers):
    """
    新增货到代收点关键词
    /mgmt/order/saveDeliveryWarnKeywords

    参数说明:
    - addrKeywords: 关键词
    """

    url = "/mgmt/order/saveDeliveryWarnKeywords"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
