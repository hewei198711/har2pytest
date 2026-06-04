import os

from util.client import client

data = {
    "id": 0,  # id
    "isRefundCheck": 0,  # 退款申请校验:0-禁用,1启用
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_product_itemExt_refundCheck(data=data, headers=headers):
    """
    退款产品配置启用/禁用
    /mgmt/product/itemExt/refundCheck

    参数说明:
    - id: id
    - isRefundCheck: 退款申请校验:0-禁用,1启用
    """

    url = "/mgmt/product/itemExt/refundCheck"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
