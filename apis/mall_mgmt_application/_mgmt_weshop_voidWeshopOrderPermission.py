import os

from util.client import client

data = {
    "id": 0,  # 主键id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_weshop_voidWeshopOrderPermission(data=data, headers=headers):
    """
    作废KOS转分权限
    /mgmt/weshop/voidWeshopOrderPermission

    参数说明:
    - id: 主键id
    """

    url = "/mgmt/weshop/voidWeshopOrderPermission"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
