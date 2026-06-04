import os

from util.client import client

data = {
    "taskDtlList": [
        {"customerCard": "", "customerId": 0, "leaderCard": "", "number": 0, "serialNo": "", "storeCode": ""}
    ],  # 确认转分参数
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_submitMgmtOrderTask(data=data, headers=headers):
    """
    分级押货模式确认转分订单接口
    /mgmt/order/submitMgmtOrderTask

    参数说明:
    - taskDtlList: 确认转分参数
    - taskDtlList.customerCard: 顾客卡号
    - taskDtlList.customerId: 顾客ID
    - taskDtlList.leaderCard: 负责人卡号
    - taskDtlList.number: 产品数量
    - taskDtlList.serialNo: 产品编码
    - taskDtlList.storeCode: 门店编码
    """

    url = "/mgmt/order/submitMgmtOrderTask"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
