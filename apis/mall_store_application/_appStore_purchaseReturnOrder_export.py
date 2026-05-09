import os

from util.client import client

params = {
    "beginTime": "",  # 申请开始日期
    "endTime": "",  # 申请结束日期
    "orderMark": 0,  # 退货标识 1普通押货退货 2套装组合退货 3套装拆分退货 4押货修改退
    "orderSn": "",  # 退货单编号
    "orderStatus": 0,  # 处理状态 1待审核 2待退回 3待验货 4已完成 5已取消
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 页大小
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_purchaseReturnOrder_export(params=params, headers=headers):
    """
    导出押货退货单列表（分页）
    /appStore/purchaseReturnOrder/export

    参数说明:
    - beginTime: 申请开始日期
    - endTime: 申请结束日期
    - orderMark: 退货标识 1普通押货退货 2套装组合退货 3套装拆分退货 4押货修改退
    - orderSn: 退货单编号
    - orderStatus: 处理状态 1待审核 2待退回 3待验货 4已完成 5已取消
    - pageNum: 页数
    - pageSize: 页大小
    - storeCode: 服务中心编号
    """

    url = "/appStore/purchaseReturnOrder/export"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
