import os

from util.client import client

data = {
    "id": 0,  # id
    "sort": 0,  # 排序
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_cms_avatarFrame_updateSort(data=data, headers=headers):
    """
    更改头像框图片排序
    /mgmt/cms/avatarFrame/updateSort

    参数说明:
    - id: id
    - sort: 排序
    """

    url = "/mgmt/cms/avatarFrame/updateSort"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
