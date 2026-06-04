import os

from util.client import client

params = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_signSale_historys(params=params, headers=headers):
    """
    获取历史版本列表
    /mgmt/prmt/signSale/historys

    参数说明:
    - id: id
    """

    url = "/mgmt/prmt/signSale/historys"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
