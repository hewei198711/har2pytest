import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _appStore_store_dis_mortgageOrder_mortgageMall(headers=headers):
    """
    商城-店铺押货下单
    /appStore/store/dis/mortgageOrder/mortgageMall
    """

    url = "/appStore/store/dis/mortgageOrder/mortgageMall"
    with client.post(url=url, headers=headers) as r:
        return r
