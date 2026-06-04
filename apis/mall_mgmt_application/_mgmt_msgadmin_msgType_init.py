import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_msgadmin_msgType_init(headers=headers):
    """
    消息类型初始化
    /mgmt/msgadmin/msgType/init
    """

    url = "/mgmt/msgadmin/msgType/init"
    with client.get(url=url, headers=headers) as r:
        return r
