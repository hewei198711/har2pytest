import os

from util.client import client

data = {
    "ids": [],  # id
    "isRefundCheck": 0,  # 退款申请校验:0-禁用,1启用
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_product_itemExt_batchRefundCheck(data=data, headers=headers):
    """
    退款产品配置批量启用/禁用
    /mgmt/product/itemExt/batchRefundCheck

    参数说明:
    - ids: id
    - isRefundCheck: 退款申请校验:0-禁用,1启用
    """

    url = "/mgmt/product/itemExt/batchRefundCheck"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
