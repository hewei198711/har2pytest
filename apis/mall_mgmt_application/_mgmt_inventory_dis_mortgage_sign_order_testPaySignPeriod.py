import os
from urllib.parse import urlencode

from util.client import client

data = {
    "signOrderSn": "",  # signOrderSn
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_inventory_dis_mortgage_sign_order_testPaySignPeriod(data=data, headers=headers):
    """
    测试支付签约单
    /mgmt/inventory/dis/mortgage/sign/order/testPaySignPeriod

    参数说明:
    - signOrderSn: signOrderSn
    """

    url = "/mgmt/inventory/dis/mortgage/sign/order/testPaySignPeriod"
    data = urlencode(data)  # application/x-www-form-urlencoded传参需要特殊处理

    with client.post(url=url, data=data, headers=headers) as r:
        return r
