import os

from util.client import client

params = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_city_level_detail_id(params=params, headers=headers):
    """
    根据ID查询城市等级详情
    /mgmt/sys/city-level/detail/{id}

    参数说明:
    - id: id
    """

    url = f"/mgmt/sys/city-level/detail/{params['id']}"
    with client.get(url=url, headers=headers) as r:
        return r
