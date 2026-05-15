import os

from util.client import client

params = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_dis_mortgageOrder_appDetail_id(params=params, headers=headers):
    """
    APP押货单详情
    /appStore/store/dis/mortgageOrder/appDetail/{id}

    参数说明:
    - id: id
    """

    url = f"/appStore/store/dis/mortgageOrder/appDetail/{params['id']}"
    with client.get(url=url, headers=headers) as r:
        return r
