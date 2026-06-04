import os

from util.client import client

params = {
    "orderNo": "",  # orderNo
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_orderSign_getSignInfoByOrderNo(params=params, headers=headers):
    """
    根据子订单号查询签约单信息
    /mgmt/orderSign/getSignInfoByOrderNo

    参数说明:
    - orderNo: orderNo
    """

    url = "/mgmt/orderSign/getSignInfoByOrderNo"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
