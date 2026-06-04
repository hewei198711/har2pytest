import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_getProvinceList(headers=headers):
    """
    获取省份信息
    /mgmt/sys/getProvinceList
    """

    url = "/mgmt/sys/getProvinceList"
    with client.get(url=url, headers=headers) as r:
        return r
