import os

from util.client import client

params = {
    "orderNo": "",  # orderNo
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_signAfter_isSignApplyReturn(params=params, headers=headers):
    """
    签约购订单是否可申请退货退款
    /mgmt/signAfter/isSignApplyReturn

    参数说明:
    - orderNo: orderNo
    """

    url = "/mgmt/signAfter/isSignApplyReturn"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
