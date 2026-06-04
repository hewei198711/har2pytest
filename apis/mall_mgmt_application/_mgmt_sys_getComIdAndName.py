import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_getComIdAndName(headers=headers):
    """
    获取所有公司的id和类型
    /mgmt/sys/getComIdAndName
    """

    url = "/mgmt/sys/getComIdAndName"
    with client.get(url=url, headers=headers) as r:
        return r
