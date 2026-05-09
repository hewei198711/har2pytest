import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _appStore_store_dis_mortgageOrder_checkSaleStock(headers=headers):
    """
    校验商品销售库存是否足够,并返回销售库存不足的商品编码
    /appStore/store/dis/mortgageOrder/checkSaleStock
    """

    url = "/appStore/store/dis/mortgageOrder/checkSaleStock"
    with client.post(url=url, headers=headers) as r:
        return r
