import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_order_riskctrl_importAddrKeywords(headers=headers):
    """
    导入收货地址关键词
    /mgmt/order/riskctrl/importAddrKeywords
    """

    url = "/mgmt/order/riskctrl/importAddrKeywords"
    with client.post(url=url, headers=headers) as r:
        return r
