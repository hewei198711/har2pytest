import os

from util.client import client

params = {
    "signNo": "",  # signNo
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_order_orderSign_findMortgageIdBySignNo(params=params, headers=headers):
    """
    有权限查看根据签约单查询押货单ID
    /appStore/order/orderSign/findMortgageIdBySignNo

    参数说明:
    - signNo: signNo
    """

    url = "/appStore/order/orderSign/findMortgageIdBySignNo"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
