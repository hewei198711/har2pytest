import os

from util.client import client

params = {
    "orderId": 0,  # orderId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_dis_mortgage_diffOrder_appDetail(params=params, headers=headers):
    """
    APP详情
    /appStore/store/dis/mortgage/diffOrder/appDetail

    参数说明:
    - orderId: orderId
    """

    url = "/appStore/store/dis/mortgage/diffOrder/appDetail"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
