import os

from util.client import client

params = {
    "needEvaluationId": False,  # TODO: 添加参数说明
    "orderStatus": 0,  # 押货换货处理状态 1待审核 2待退回 3待验货 4待发货 5待收货 6已完成 7已取消,押货退货处理状态:1待审核 2待退回 3待验货 4已完成 5已取消,货损货差处理状态:状态 1待审核 2待发货 3待收货 4已完成 5已取消
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 页大小
    "searchStr": "",  # 押货退货/换货/货损货差单号/产品名称/产品编号
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_dis_mortgage_exchangeOrder_appListPage(params=params, headers=headers):
    """
    APP分页查询
    /appStore/store/dis/mortgage/exchangeOrder/appListPage

    参数说明:
    - orderStatus: 押货换货处理状态 1待审核 2待退回 3待验货 4待发货 5待收货 6已完成 7已取消,押货退货处理状态:1待审核 2待退回 3待验货 4已完成 5已取消,货损货差处理状态:状态 1待审核 2待发货 3待收货 4已完成 5已取消
    - pageNum: 页数
    - pageSize: 页大小
    - searchStr: 押货退货/换货/货损货差单号/产品名称/产品编号
    - storeCode: 服务中心编号
    """

    url = "/appStore/store/dis/mortgage/exchangeOrder/appListPage"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
