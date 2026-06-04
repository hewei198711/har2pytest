import os

from util.client import client

params = {
    "listId": 0,  # listId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dataAdmin_warningWhiteList_detail(params=params, headers=headers):
    """
    详情
    /mgmt/dataAdmin/warningWhiteList/detail

    参数说明:
    - listId: listId
    """

    url = "/mgmt/dataAdmin/warningWhiteList/detail"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
