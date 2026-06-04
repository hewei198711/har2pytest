import os

from util.client import client

params = {
    "id": "",  # 隐藏编码列表id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_deleteDisableRegion(params=params, headers=headers):
    """
    取消隐藏的地区编码
    /mgmt/sys/deleteDisableRegion

    参数说明:
    - id: 隐藏编码列表id
    """

    url = "/mgmt/sys/deleteDisableRegion"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
