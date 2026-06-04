import os
from urllib.parse import urlencode

from util.client import client

data = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_weshop_getWechatShopOrderDetail(data=data, headers=headers):
    """
    订单管理-微信小店订单详情
    /mgmt/weshop/getWechatShopOrderDetail

    参数说明:
    - id: id
    """

    url = "/mgmt/weshop/getWechatShopOrderDetail"
    data = urlencode(data)  # application/x-www-form-urlencoded传参需要特殊处理

    with client.post(url=url, data=data, headers=headers) as r:
        return r
