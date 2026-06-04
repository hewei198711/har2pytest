import os

from util.client import client

params = {
    "beginTime": "",  # 开始退货时间
    "companyCode": "",  # 所属分公司编号
    "companyCodeList": [],  # 分公司编号列表
    "endTime": "",  # 结束退货时间
    "finishBeginTime": "",  # 完成开始日期
    "finishEndTime": "",  # 完成结束日期
    "orderMark": 0,  # 押货退货单标识 1普通押货退货 2套装组合退货 3套装拆分退货 4押货修改退
    "orderSn": "",  # 押货退货单号
    "orderSource": 0,  # 退货单来源 1服务中心退货 2运营后台退货
    "orderStatus": 0,  # 处理状态 1待审核 2待退回 3待验货 4已完成 5已取消
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 页大小
    "pushStatus": 0,  # 推送状态 1待推送 2推送成功
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_returnOrder_listOrder(params=params, headers=headers):
    """
    后台查询押货退货单列表
    /mgmt/inventory/returnOrder/listOrder

    参数说明:
    - beginTime: 开始退货时间
    - companyCode: 所属分公司编号
    - companyCodeList: 分公司编号列表
    - endTime: 结束退货时间
    - finishBeginTime: 完成开始日期
    - finishEndTime: 完成结束日期
    - orderMark: 押货退货单标识 1普通押货退货 2套装组合退货 3套装拆分退货 4押货修改退
    - orderSn: 押货退货单号
    - orderSource: 退货单来源 1服务中心退货 2运营后台退货
    - orderStatus: 处理状态 1待审核 2待退回 3待验货 4已完成 5已取消
    - pageNum: 页数
    - pageSize: 页大小
    - pushStatus: 推送状态 1待推送 2推送成功
    - storeCode: 服务中心编号
    """

    url = "/mgmt/inventory/returnOrder/listOrder"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
