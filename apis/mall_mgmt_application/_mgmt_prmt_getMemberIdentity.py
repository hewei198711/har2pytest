import os

from util.client import client

headers = {
    "channel": "pc",
    "client": "op",
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_prmt_getMemberIdentity(headers=headers):
    """
    获取所有顾客身份类型
    /mgmt/prmt/getMemberIdentity
    """

    url = "/mgmt/prmt/getMemberIdentity"
    with client.get(url=url, headers=headers) as r:
        return r
