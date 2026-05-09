import os

from util.client import client

data = {
    "orderMark": 0,  # 押货标识 1普通押货单 2仅调账不发货 3套装组合押货 4套装拆分押货 5库存转移 6签约押货单 7随心购押货单 8换购品押货 9签约购押货3.0 10商城-店铺押货 11签约购押货4.0
    "products": [],  # 商品列表
    "storeCode": "",  # 店铺编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_dis_mortgageOrder_checkMortgagePayProduct(data=data, headers=headers):
    """
    校验商品押货分配量与是否允许押货,返回不通过的商品编号
    /appStore/store/dis/mortgageOrder/checkMortgagePayProduct

    参数说明:
    - orderMark: 押货标识 1普通押货单 2仅调账不发货 3套装组合押货 4套装拆分押货 5库存转移 6签约押货单 7随心购押货单 8换购品押货 9签约购押货3.0 10商城-店铺押货 11签约购押货4.0
    - products: 商品列表
    - storeCode: 店铺编号
    """

    url = "/appStore/store/dis/mortgageOrder/checkMortgagePayProduct"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
