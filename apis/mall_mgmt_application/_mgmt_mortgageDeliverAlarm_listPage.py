import os

from util.client import client

params = {
    "bizMode": 0,  # 押货模式 1->1:3押货 2分级押货
    "deliverSn": "",  # 发货单编号
    "orderSn": "",  # 押货单号
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 页大小
    "status": 0,  # 状态 1待跟进 2已跟进
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_mortgageDeliverAlarm_listPage(params=params, headers=headers):
    """
    分页列表
    /mgmt/mortgageDeliverAlarm/listPage

    参数说明:
    - bizMode: 押货模式 1->1:3押货 2分级押货
    - deliverSn: 发货单编号
    - orderSn: 押货单号
    - pageNum: 页数
    - pageSize: 页大小
    - status: 状态 1待跟进 2已跟进
    - storeCode: 服务中心编号
    """

    url = "/mgmt/mortgageDeliverAlarm/listPage"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
