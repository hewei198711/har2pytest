import os

from util.client import client

data = {
    "from": 0,  # TODO: 添加参数说明
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 每页显示数
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_shippingAddressHistoryList(data=data, headers=headers):
    """
    订单管理-修改收货地址记录-修改历史记录
    /mgmt/order/shippingAddressHistoryList

    参数说明:
    - pageNum: 页数
    - pageSize: 每页显示数
    """

    url = "/mgmt/order/shippingAddressHistoryList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
