import os

from util.client import client

data = {
    "creatorCard": "",  # 开单人卡号
    "customerCard": "",  # 购货人卡号
    "docType": 0,  # 单据类型：1=购货单 2=发货单
    "operatorUser": "",  # 操作人员
    "orderNo": "",  # 订单编号
    "pageNum": 0,  # TODO: 添加参数说明
    "pageSize": 0,  # TODO: 添加参数说明
    "printChannel": 0,  # 打印渠道：1=商城前端 2=店铺端 3=运营后台
    "printEndTime": "",  # 打印结束时间
    "printStartTime": "",  # 打印开始时间
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_orderPrintRecord_list(data=data, headers=headers):
    """
    订单打印记录列表
    /mgmt/order/orderPrintRecord-list

    参数说明:
    - creatorCard: 开单人卡号
    - customerCard: 购货人卡号
    - docType: 单据类型：1=购货单 2=发货单
    - operatorUser: 操作人员
    - orderNo: 订单编号
    - printChannel: 打印渠道：1=商城前端 2=店铺端 3=运营后台
    - printEndTime: 打印结束时间
    - printStartTime: 打印开始时间
    """

    url = "/mgmt/order/orderPrintRecord-list"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
