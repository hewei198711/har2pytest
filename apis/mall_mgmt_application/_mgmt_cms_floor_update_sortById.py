import os

from util.client import client

data = {
    "id": 0,  # id
    "sort": 0,  # 排序
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_floor_update_sortById(data=data, headers=headers):
    """
    按id修改楼层页排序
    /mgmt/cms/floor/update/sortById

    参数说明:
    - id: id
    - sort: 排序
    """

    url = "/mgmt/cms/floor/update/sortById"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
