import os

from util.client import client

params = {
    "orderStatus": 0,  # 状态 1待审核 2待收货 3已完成 4已取消
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 每页大小
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_mobile_diffOrder_orderList(params=params, headers=headers):
    """
    APP货损货差单分页查询
    /appStore/mobile/diffOrder/orderList

    参数说明:
    - orderStatus: 状态 1待审核 2待收货 3已完成 4已取消
    - pageNum: 页数
    - pageSize: 每页大小
    """

    url = "/appStore/mobile/diffOrder/orderList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
