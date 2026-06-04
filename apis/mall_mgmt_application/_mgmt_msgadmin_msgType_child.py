import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_msgadmin_msgType_child(headers=headers):
    """
    查询所有子节点消息类型内容(页面消息类型调用接口,仅查询有效)
    /mgmt/msgadmin/msgType/child
    """

    url = "/mgmt/msgadmin/msgType/child"
    with client.get(url=url, headers=headers) as r:
        return r
