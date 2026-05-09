import os

from util.client import client

params = {
    "id": "",  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_dis_mortgage_diffOrder_detail_id(params=params, headers=headers):
    """
    详情
    /appStore/store/dis/mortgage/diffOrder/detail/{id}

    参数说明:
    - id: id
    """

    url = f"/appStore/store/dis/mortgage/diffOrder/detail/{params['id']}"
    with client.get(url=url, headers=headers) as r:
        return r
