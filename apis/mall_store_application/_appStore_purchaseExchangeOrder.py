import os

from util.client import client

data = {
    "orderFileName": "",  # 换货单附件名称，支持3个，用逗号隔开
    "orderFileUrl": "",  # 换货单附件，支持3个，用逗号隔开
    "productVoList": [],  # 商品列表
    "reasonFirst": "",  # 一级原因
    "reasonFirstId": 0,  # 一级原因id
    "reasonFirstRemarks": "",  # 一级原因备注
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_purchaseExchangeOrder(data=data, headers=headers):
    """
    添加换货单
    /appStore/purchaseExchangeOrder

    参数说明:
    - orderFileName: 换货单附件名称，支持3个，用逗号隔开
    - orderFileUrl: 换货单附件，支持3个，用逗号隔开
    - productVoList: 商品列表
    - reasonFirst: 一级原因
    - reasonFirstId: 一级原因id
    - reasonFirstRemarks: 一级原因备注
    """

    url = "/appStore/purchaseExchangeOrder"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
