import os

from util.client import client

params = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_dis_mortgage_returnOrder_detail_id(params=params, headers=headers):
    """
    押货退详情
    /appStore/store/dis/mortgage/returnOrder/detail/{id}

    参数说明:
    - id: id
    """

    url = f"/appStore/store/dis/mortgage/returnOrder/detail/{params['id']}"
    with client.get(url=url, headers=headers) as r:
        return r
