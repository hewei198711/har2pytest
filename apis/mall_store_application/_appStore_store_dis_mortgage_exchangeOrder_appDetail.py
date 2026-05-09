import os

from util.client import client

params = {
    "orderId": 0,  # 换货单id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_dis_mortgage_exchangeOrder_appDetail(params=params, headers=headers):
    """
    APP详情
    /appStore/store/dis/mortgage/exchangeOrder/appDetail

    参数说明:
    - orderId: 换货单id
    """

    url = "/appStore/store/dis/mortgage/exchangeOrder/appDetail"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
