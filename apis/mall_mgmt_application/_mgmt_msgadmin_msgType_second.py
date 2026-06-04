import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_msgadmin_msgType_second(headers=headers):
    """
    查询所有子节点消息类型内容(包含所有状态,可用不可用都可以查询)
    /mgmt/msgadmin/msgType/second
    """

    url = "/mgmt/msgadmin/msgType/second"
    with client.get(url=url, headers=headers) as r:
        return r
