import os

from util.client import client

data = {
    "ids": [],  # 主键id集合
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_riskctrl_deleteAddrKeywords(data=data, headers=headers):
    """
    删除收货地址关键词
    /mgmt/order/riskctrl/deleteAddrKeywords

    参数说明:
    - ids: 主键id集合
    """

    url = "/mgmt/order/riskctrl/deleteAddrKeywords"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
