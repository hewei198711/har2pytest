import os

from util.client import client

data = {
    "attachmentList": [],  # 附件列表(付费凭证)
    "id": 0,  # 返修单ID
    "systemCode": 0,  # 查询系统编码
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_mobile_store_factory_paymentConfirm(data=data, headers=headers):
    """
    执行付费确认
    /appStore/mobile/store/factory/paymentConfirm

    参数说明:
    - attachmentList: 附件列表(付费凭证)
    - id: 返修单ID
    - systemCode: 查询系统编码
    """

    url = "/appStore/mobile/store/factory/paymentConfirm"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
