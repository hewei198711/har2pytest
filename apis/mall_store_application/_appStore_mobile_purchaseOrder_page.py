import os

from util.client import client

params = {
    "customFlag": 0,  # 是否为定制品押货单 0否 1是
    "orderStatus": 0,  # 押货单状态,1待审核 2待发货（审核通过） 3部分发货 4已完成 5已取消
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 页大小
    "searchStr": "",  # 押货单号/产品名称/产品编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_mobile_purchaseOrder_page(params=params, headers=headers):
    """
    押货单列表分页
    /appStore/mobile/purchaseOrder/page

    参数说明:
    - customFlag: 是否为定制品押货单 0否 1是
    - orderStatus: 押货单状态,1待审核 2待发货（审核通过） 3部分发货 4已完成 5已取消
    - pageNum: 页数
    - pageSize: 页大小
    - searchStr: 押货单号/产品名称/产品编号
    """

    url = "/appStore/mobile/purchaseOrder/page"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
