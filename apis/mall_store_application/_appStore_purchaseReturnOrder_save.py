import os

from util.client import client

data = {
    "invtMortgageReturnOrderProductVOList": [],  # 押货退货单货物列表
    "invtMortgageReturnOrderVO": "",  # 押货退货单信息
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_purchaseReturnOrder_save(data=data, headers=headers):
    """
    提交退货单
    /appStore/purchaseReturnOrder/save

    参数说明:
    - invtMortgageReturnOrderProductVOList: 押货退货单货物列表
    - invtMortgageReturnOrderVO: 押货退货单信息
    """

    url = "/appStore/purchaseReturnOrder/save"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
