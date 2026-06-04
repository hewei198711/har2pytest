import os

from util.client import client

data = {
    "planCode": "",  # TODO: 添加参数说明
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_msgadmin_handmade_repeal(data=data, headers=headers):
    """
    撤销发送
    /mgmt/msgadmin/handmade/repeal
    """

    url = "/mgmt/msgadmin/handmade/repeal"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
