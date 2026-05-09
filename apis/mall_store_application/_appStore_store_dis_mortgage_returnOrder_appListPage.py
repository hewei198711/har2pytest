import os

from util.client import client

params = {
    "beginTime": "",  # 申请开始日期
    "companyCode": "",  # 分公司编号
    "companyCodeList": [],  # 分公司编号列表
    "companyCodes": [],  # 分公司编号列表
    "discountType": 0,  # 折扣类型 1:A->65%, 2:B->70%, 3:C->75%, 4:D->85%
    "endTime": "",  # 申请结束日期
    "finishBeginTime": "",  # 完成开始日期
    "finishEndTime": "",  # 完成结束日期
    "orderMark": 0,  # 退货标识 1普通押货退货 2套装组合退货 3套装拆分退货 4押货修改退
    "orderSn": "",  # 退货单编号
    "orderSource": 0,  # 押货单来源 1服务中心押货 2运营后台押货
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


def _appStore_store_dis_mortgage_returnOrder_appListPage(params=params, headers=headers):
    """
    APP分页列表
    /appStore/store/dis/mortgage/returnOrder/appListPage

    参数说明:
    - beginTime: 申请开始日期
    - companyCode: 分公司编号
    - companyCodeList: 分公司编号列表
    - companyCodes: 分公司编号列表
    - discountType: 折扣类型 1:A->65%, 2:B->70%, 3:C->75%, 4:D->85%
    - endTime: 申请结束日期
    - finishBeginTime: 完成开始日期
    - finishEndTime: 完成结束日期
    - orderMark: 退货标识 1普通押货退货 2套装组合退货 3套装拆分退货 4押货修改退
    - orderSn: 退货单编号
    - orderSource: 押货单来源 1服务中心押货 2运营后台押货
    - orderStatus: 处理状态 1待审核 2待退回 3待验货 4已完成 5已取消
    - pageNum: 页数
    - pageSize: 页大小
    - pushStatus: 推送状态 1待推送 2推送成功
    - storeCode: 服务中心编号
    """

    url = "/appStore/store/dis/mortgage/returnOrder/appListPage"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
