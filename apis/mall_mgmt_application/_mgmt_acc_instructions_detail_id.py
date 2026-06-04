import os

from util.client import client

params = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_acc_instructions_detail_id(params=params, headers=headers):
    """
    使用说明详情
    /mgmt/acc/instructions/detail/{id}

    参数说明:
    - id: id
    """

    url = f"/mgmt/acc/instructions/detail/{params['id']}"
    with client.get(url=url, headers=headers) as r:
        return r
