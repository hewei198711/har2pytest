import os

from util.client import client

params = {
    "beginTime": "",  # 开始时间
    "companyCode": "",  # 分公司编号
    "diffType": 0,  # 货损货差类型 1货损 2货差
    "endTime": "",  # 结束时间
    "orderSn": "",  # 货损货差单号
    "orderSource": 0,  # 申请端口 1油葱商城 2运营后台
    "orderStatus": 0,  # 状态 1待审核 2待收货 3已完成 4已取消 5待发货
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 页大小
    "storeCode": "",  # 服务中心编码
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_productDiff_orderList(params=params, headers=headers):
    """
    货损货差列表（分页）
    /appStore/productDiff/orderList

    参数说明:
    - beginTime: 开始时间
    - companyCode: 分公司编号
    - diffType: 货损货差类型 1货损 2货差
    - endTime: 结束时间
    - orderSn: 货损货差单号
    - orderSource: 申请端口 1油葱商城 2运营后台
    - orderStatus: 状态 1待审核 2待收货 3已完成 4已取消 5待发货
    - pageNum: 页数
    - pageSize: 页大小
    - storeCode: 服务中心编码
    """

    url = "/appStore/productDiff/orderList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
