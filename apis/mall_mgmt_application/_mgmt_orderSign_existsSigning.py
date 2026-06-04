import os

from util.client import client

params = {
    "creatorId": 0,  # creatorId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_orderSign_existsSigning(params=params, headers=headers):
    """
    查询开单人是否存在签约中的签约购
    /mgmt/orderSign/existsSigning

    参数说明:
    - creatorId: creatorId
    """

    url = "/mgmt/orderSign/existsSigning"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
