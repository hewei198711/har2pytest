import os
from urllib.parse import urlencode

from util.client import client

data = {
    "orderId": 0,  # 换货单id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_inventory_dis_mortgage_exchangeOrder_confirm(data=data, headers=headers):
    """
    确认收货
    /mgmt/inventory/dis/mortgage/exchangeOrder/confirm

    参数说明:
    - orderId: 换货单id
    """

    url = "/mgmt/inventory/dis/mortgage/exchangeOrder/confirm"
    data = urlencode(data)  # application/x-www-form-urlencoded传参需要特殊处理

    with client.post(url=url, data=data, headers=headers) as r:
        return r
