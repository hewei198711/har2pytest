import os

from util.client import client

data = {
    "status": 0,  # 活码状态，0-全部禁用，1-全部启用
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_qrcode_updateAllStatus(data=data, headers=headers):
    """
    修改活码状态 支持全部启用/禁用
    /mgmt/store/qrcode/updateAllStatus

    参数说明:
    - status: 活码状态，0-全部禁用，1-全部启用
    """

    url = "/mgmt/store/qrcode/updateAllStatus"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
