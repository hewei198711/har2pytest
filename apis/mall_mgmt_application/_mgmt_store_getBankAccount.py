import os

from util.client import client

params = {
    "accountId": 0,  # accountId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_getBankAccount(params=params, headers=headers):
    """
    获取银行账号
    /mgmt/store/getBankAccount

    参数说明:
    - accountId: accountId
    """

    url = "/mgmt/store/getBankAccount"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
