import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_getCertiTypeIdAndName(headers=headers):
    """
    查找所有的证件类型的id和名字
    /mgmt/sys/getCertiTypeIdAndName
    """

    url = "/mgmt/sys/getCertiTypeIdAndName"
    with client.get(url=url, headers=headers) as r:
        return r
