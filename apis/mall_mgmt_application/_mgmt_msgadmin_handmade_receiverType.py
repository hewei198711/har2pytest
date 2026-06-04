import os

from util.client import client

params = {
    "pid": "",  # pid
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_msgadmin_handmade_receiverType(params=params, headers=headers):
    """
    查询发送渠道
    /mgmt/msgadmin/handmade/receiverType

    参数说明:
    - pid: pid
    """

    url = "/mgmt/msgadmin/handmade/receiverType"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
