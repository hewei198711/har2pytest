import os

from util.client import client

params = {
    "month": 0,  # month
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_storeDepositMonthSettle(params=params, headers=headers):
    """
    保证金月结，测试用接口
    /mgmt/store/storeDepositMonthSettle

    参数说明:
    - month: month
    """

    url = "/mgmt/store/storeDepositMonthSettle"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
