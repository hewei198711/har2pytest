import os

from util.client import client

data = {
    "id": 0,  # id
    "sort": 0,  # 排序
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_cms_activity_update_sortById(data=data, headers=headers):
    """
    按id修改活动专区排序
    /mgmt/cms/activity/update/sortById

    参数说明:
    - id: id
    - sort: 排序
    """

    url = "/mgmt/cms/activity/update/sortById"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
