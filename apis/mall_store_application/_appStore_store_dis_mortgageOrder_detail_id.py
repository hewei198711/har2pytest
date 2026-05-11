import os

from util.client import client

params = {
    "id": "96453",  # TODO: 添加参数说明
}

headers = {
    "channel": "pc",
    "client": "store",
    "authorization": f"bearer {os.environ['access_token']}",
}


def _appStore_store_dis_mortgageOrder_detail_id(params=params, headers=headers):
    """
    TODO: 添加接口描述
    /appStore/store/dis/mortgageOrder/detail/{id}
    """

    url = f"/appStore/store/dis/mortgageOrder/detail/{params['id']}"
    with client.get(url=url, headers=headers) as r:
        return r
