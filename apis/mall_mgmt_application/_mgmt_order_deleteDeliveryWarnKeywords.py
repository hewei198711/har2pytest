import os

from util.client import client

data = {
    "ids": [],  # 主键id集合
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_deleteDeliveryWarnKeywords(data=data, headers=headers):
    """
    删除货到代收点关键词
    /mgmt/order/deleteDeliveryWarnKeywords

    参数说明:
    - ids: 主键id集合
    """

    url = "/mgmt/order/deleteDeliveryWarnKeywords"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
