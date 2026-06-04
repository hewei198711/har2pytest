import os

from util.client import client

params = {
    "storeCode": "",  # storeCode
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_getBankAccountList(params=params, headers=headers):
    """
    通过storeCode获取银行账户资料信息
    /mgmt/store/getBankAccountList

    参数说明:
    - storeCode: storeCode
    """

    url = "/mgmt/store/getBankAccountList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
