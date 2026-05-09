import os

from util.client import client

params = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_mobile_store_refund_cancelApply(params=params, headers=headers):
    """
    撤销申请
    /appStore/mobile/store/refund/cancelApply

    参数说明:
    - id: id
    """

    url = "/appStore/mobile/store/refund/cancelApply"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
