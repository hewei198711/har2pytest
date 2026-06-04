import os

from util.client import client

params = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_acc_item_detail_id(params=params, headers=headers):
    """
    获取acc项目详情
    /mgmt/acc/item/detail/{id}

    参数说明:
    - id: id
    """

    url = f"/mgmt/acc/item/detail/{params['id']}"
    with client.get(url=url, headers=headers) as r:
        return r
