import os

from util.client import client

params = {
    "id": "",  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_dis_mortgageOrder_detail_id(params=params, headers=headers):
    """
    押货单详情
    /appStore/store/dis/mortgageOrder/detail/{id}

    参数说明:
    - id: id
    """

    url = f"/appStore/store/dis/mortgageOrder/detail/{params['id']}"
    with client.get(url=url, headers=headers) as r:
        return r
