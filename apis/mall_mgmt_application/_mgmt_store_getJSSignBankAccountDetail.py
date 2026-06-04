import os

from util.client import client

params = {
    "account": "",  # account
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_getJSSignBankAccountDetail(params=params, headers=headers):
    """
    获取建设银行签署银行账号详细信息
    /mgmt/store/getJSSignBankAccountDetail

    参数说明:
    - account: account
    """

    url = "/mgmt/store/getJSSignBankAccountDetail"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
