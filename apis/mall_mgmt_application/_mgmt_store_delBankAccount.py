import os

from util.client import client

params = {
    "accountId": 0,  # accountId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_delBankAccount(params=params, headers=headers):
    """
    银行卡作废
    /mgmt/store/delBankAccount

    参数说明:
    - accountId: accountId
    """

    url = "/mgmt/store/delBankAccount"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
