import os

from util.client import client

data = {
    "list": [{"productCode": "", "productMortgagePrice": 0.0, "productNum": 0, "productRetailPrice": 0.0}],  # 押货列表
    "transId": "",  # 业务id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_purchase_commit(data=data, headers=headers):
    """
    提交押货单
    /appStore/purchase/commit

    参数说明:
    - list: 押货列表
    - list.productCode: 押货商品编码
    - list.productMortgagePrice: 商品押货价
    - list.productNum: 押货商品数量
    - list.productRetailPrice: 商品零售价
    - transId: 业务id
    """

    url = "/appStore/purchase/commit"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
