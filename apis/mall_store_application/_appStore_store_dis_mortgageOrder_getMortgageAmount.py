import os

from util.client import client

headers = {
    "channel": "pc",
    "client": "store",
    "authorization": f"bearer {os.environ['access_token']}",
}


def _appStore_store_dis_mortgageOrder_getMortgageAmount(headers=headers):
    """
    TODO: 添加接口描述
    /appStore/store/dis/mortgageOrder/getMortgageAmount
    """

    url = "/appStore/store/dis/mortgageOrder/getMortgageAmount"
    with client.get(url=url, headers=headers) as r:
        return r
