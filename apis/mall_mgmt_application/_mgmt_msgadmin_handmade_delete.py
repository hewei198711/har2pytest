import os

from util.client import client

data = {
    "planCode": "",  # TODO: 添加参数说明
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_msgadmin_handmade_delete(data=data, headers=headers):
    """
    删除手工消息
    /mgmt/msgadmin/handmade/delete
    """

    url = "/mgmt/msgadmin/handmade/delete"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
