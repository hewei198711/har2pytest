import os

from util.client import client

params = {
    "id": "",  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_mobile_returnOrder_id(params=params, headers=headers):
    """
    押货退货详情
    /appStore/mobile/returnOrder/{id}

    参数说明:
    - id: id
    """

    url = f"/appStore/mobile/returnOrder/{params['id']}"
    with client.get(url=url, headers=headers) as r:
        return r
