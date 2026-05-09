import os

from util.client import client

params = {
    "returnNo": "",  # returnNo
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_orderReturn_details(params=params, headers=headers):
    """
    售后详情
    /appStore/orderReturn/details

    参数说明:
    - returnNo: returnNo
    """

    url = "/appStore/orderReturn/details"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
