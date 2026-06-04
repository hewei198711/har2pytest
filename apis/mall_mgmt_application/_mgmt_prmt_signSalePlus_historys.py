import os

from util.client import client

params = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_signSalePlus_historys(params=params, headers=headers):
    """
    获取历史版本列表
    /mgmt/prmt/signSalePlus/historys

    参数说明:
    - id: id
    """

    url = "/mgmt/prmt/signSalePlus/historys"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
