import os

from util.client import client

params = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_return_register_deleteReturnRegister(params=params, headers=headers):
    """
    删除登记退货信息
    /mgmt/return/register/deleteReturnRegister

    参数说明:
    - id: id
    """

    url = "/mgmt/return/register/deleteReturnRegister"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
