import os

from util.client import client

data = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_cms_buttonColumn_shelfOffButtonColumn(data=data, headers=headers):
    """
    下架底部栏配置
    /mgmt/cms/buttonColumn/shelfOffButtonColumn

    参数说明:
    - id: id
    """

    url = "/mgmt/cms/buttonColumn/shelfOffButtonColumn"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
