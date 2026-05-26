import os

from util.client import client

headers = {
    "channel": "pc",
    "client": "op",
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_sys_lclFee_list(headers=headers):
    """
    获取拼箱费列表
    /mgmt/sys/lclFee/list
    """

    url = "/mgmt/sys/lclFee/list"
    with client.get(url=url, headers=headers) as r:
        return r
