import os

from util.client import client

params = {
    "code": "",  # 需隐藏的编码
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_disableRegion(params=params, headers=headers):
    """
    根据编码隐藏地区
    /mgmt/sys/disableRegion

    参数说明:
    - code: 需隐藏的编码
    """

    url = "/mgmt/sys/disableRegion"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
