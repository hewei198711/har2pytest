import os

from util.client import client

params = {
    "orderCancelTimeEnd": "",  # 取消时间(结束) yyyy-MM-dd
    "orderCancelTimeStart": "",  # 取消时间(开始) yyyy-MM-dd
    "orderCreateTimeEnd": "",  # 开单时间(结束) yyyy-MM-dd
    "orderCreateTimeStart": "",  # 开单时间(开始) yyyy-MM-dd
    "orderMortgageTimeEnd": "",  # 支付时间(结束) yyyy-MM-dd
    "orderMortgageTimeStart": "",  # 支付时间(开始) yyyy-MM-dd
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 页大小
    "storeCode": "",  # 店铺编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_distributionChange_page(params=params, headers=headers):
    """
    列表查询
    /mgmt/inventory/distributionChange/page

    参数说明:
    - orderCancelTimeEnd: 取消时间(结束) yyyy-MM-dd
    - orderCancelTimeStart: 取消时间(开始) yyyy-MM-dd
    - orderCreateTimeEnd: 开单时间(结束) yyyy-MM-dd
    - orderCreateTimeStart: 开单时间(开始) yyyy-MM-dd
    - orderMortgageTimeEnd: 支付时间(结束) yyyy-MM-dd
    - orderMortgageTimeStart: 支付时间(开始) yyyy-MM-dd
    - pageNum: 页数
    - pageSize: 页大小
    - storeCode: 店铺编号
    """

    url = "/mgmt/inventory/distributionChange/page"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
