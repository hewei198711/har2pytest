import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_dis_mortgageOrder_getMortgageAmount(headers=headers):
    """
    查询店铺押货余额与限额
    /appStore/store/dis/mortgageOrder/getMortgageAmount
    """

    url = "/appStore/store/dis/mortgageOrder/getMortgageAmount"
    with client.get(url=url, headers=headers) as r:
        return r
