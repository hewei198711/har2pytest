import os

from util.client import client

params = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_undoDepositApply(params=params, headers=headers):
    """
    撤销保证金申请
    /mgmt/store/undoDepositApply

    参数说明:
    - id: id
    """

    url = "/mgmt/store/undoDepositApply"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
