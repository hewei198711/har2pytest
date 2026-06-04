import os
from urllib.parse import urlencode

from util.client import client

data = {
    "orderRemark": "",  # orderRemark
    "orderSn": "",  # orderSn
    "pushMark": "",  # pushMark
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_inventory_dis_mortgage_order_batchCancel(data=data, headers=headers):
    """
    押货单批量取消
    /mgmt/inventory/dis/mortgage/order/batchCancel

    参数说明:
    - orderRemark: orderRemark
    - orderSn: orderSn
    - pushMark: pushMark
    """

    url = "/mgmt/inventory/dis/mortgage/order/batchCancel"
    data = urlencode(data)  # application/x-www-form-urlencoded传参需要特殊处理

    with client.post(url=url, data=data, headers=headers) as r:
        return r
