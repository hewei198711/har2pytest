import os

from util.client import client

params = {
    "beginTime": "",  # 开始押货时间
    "customFlag": 0,  # 是否为定制品押货单 0否 1是
    "endTime": "",  # 结束押货时间
    "logisticsEvaluation": "",  # 物流评价 0未评价 1非常满意 2满意 3不满意 4一般
    "orderMark": 0,  # 标志 1普通押货单 2仅调账不发货 3套装组合押货 4套装拆分押货
    "orderSn": "",  # 押货单号
    "orderSource": 0,  # 押货单来源
    "orderStatus": 0,  # 押货单状态,1待审核 2待发货（审核通过） 3部分发货 4全部发货 5已收货 6已取消（审核不通过）
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_purchaseOrder_export(params=params, headers=headers):
    """
    押货单列表导出
    /appStore/purchaseOrder/export

    参数说明:
    - beginTime: 开始押货时间
    - customFlag: 是否为定制品押货单 0否 1是
    - endTime: 结束押货时间
    - logisticsEvaluation: 物流评价 0未评价 1非常满意 2满意 3不满意 4一般
    - orderMark: 标志 1普通押货单 2仅调账不发货 3套装组合押货 4套装拆分押货
    - orderSn: 押货单号
    - orderSource: 押货单来源
    - orderStatus: 押货单状态,1待审核 2待发货（审核通过） 3部分发货 4全部发货 5已收货 6已取消（审核不通过）
    """

    url = "/appStore/purchaseOrder/export"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
