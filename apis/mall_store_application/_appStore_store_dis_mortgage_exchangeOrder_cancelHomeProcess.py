import os

from util.client import client

data = {
    "id": 0,  # 换货单id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_dis_mortgage_exchangeOrder_cancelHomeProcess(data=data, headers=headers):
    """
    取消上门取件退回处理
    /appStore/store/dis/mortgage/exchangeOrder/cancelHomeProcess

    参数说明:
    - id: 换货单id
    """

    url = "/appStore/store/dis/mortgage/exchangeOrder/cancelHomeProcess"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
