import os

from util.client import client

params = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_acc_cleaner_detail_id(params=params, headers=headers):
    """
    查询清洗人员详情
    /mgmt/acc/cleaner/detail/{id}

    参数说明:
    - id: id
    """

    url = f"/mgmt/acc/cleaner/detail/{params['id']}"
    with client.get(url=url, headers=headers) as r:
        return r
