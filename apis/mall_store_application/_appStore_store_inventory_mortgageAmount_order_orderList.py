import os

from util.client import client

data = {
    "beginTime": "",  # 开始押货时间
    "endTime": "",  # 结束押货时间
    "orderSn": "",  # 押货单号
    "orderSource": 0,  # 押货单来源
    "orderStatus": 0,  # 押货单状态,1待审核 2待发货（审核通过） 3部分发货 4全部发货 5已收货 6已取消（审核不通过）
    "pageNum": 0,  # TODO: 添加参数说明
    "pageSize": 0,  # TODO: 添加参数说明
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_inventory_mortgageAmount_order_orderList(data=data, headers=headers):
    """
    服务中心获取押货单
    /appStore/store/inventory/mortgageAmount/order/orderList

    参数说明:
    - beginTime: 开始押货时间
    - endTime: 结束押货时间
    - orderSn: 押货单号
    - orderSource: 押货单来源
    - orderStatus: 押货单状态,1待审核 2待发货（审核通过） 3部分发货 4全部发货 5已收货 6已取消（审核不通过）
    """

    url = "/appStore/store/inventory/mortgageAmount/order/orderList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
