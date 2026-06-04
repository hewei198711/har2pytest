import os

from util.client import client

params = {
    "storeCode": "",  # storeCode
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_getDepositInfo(params=params, headers=headers):
    """
    根据storeCode获取保证金信息
    /mgmt/store/getDepositInfo

    参数说明:
    - storeCode: storeCode
    """

    url = "/mgmt/store/getDepositInfo"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
