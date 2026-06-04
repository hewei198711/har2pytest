import os

from util.client import client

params = {
    "account": "",  # OA工号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_personRegister(params=params, headers=headers):
    """
    通过OA工号获取客户编号
    /mgmt/store/personRegister

    参数说明:
    - account: OA工号
    """

    url = "/mgmt/store/personRegister"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
