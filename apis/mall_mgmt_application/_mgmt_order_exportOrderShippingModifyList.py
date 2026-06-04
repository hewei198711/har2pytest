import os

from util.client import client

params = {
    "creatorCard": "",  # 开单人卡号
    "customerCard": "",  # 顾客卡号
    "orderNo": "",  # 订单编号
    "pageNum": 0,  # 页码
    "pageSize": 0,  # 页面大小
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_exportOrderShippingModifyList(params=params, headers=headers):
    """
    订单管理-修改收货地址记录-导出
    /mgmt/order/exportOrderShippingModifyList

    参数说明:
    - creatorCard: 开单人卡号
    - customerCard: 顾客卡号
    - orderNo: 订单编号
    - pageNum: 页码
    - pageSize: 页面大小
    """

    url = "/mgmt/order/exportOrderShippingModifyList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
