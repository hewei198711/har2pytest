import os

from util.client import client

params = {
    "storeCode": "",  # storeCode
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_getJSSignBankAccountList(params=params, headers=headers):
    """
    获取建设银行签署银行账号列表
    /mgmt/store/getJSSignBankAccountList

    参数说明:
    - storeCode: storeCode
    """

    url = "/mgmt/store/getJSSignBankAccountList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
