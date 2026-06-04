import os

from util.client import client

data = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_cms_buttonColumn_delButtonColumn(data=data, headers=headers):
    """
    删除底部栏配置
    /mgmt/cms/buttonColumn/delButtonColumn

    参数说明:
    - id: id
    """

    url = "/mgmt/cms/buttonColumn/delButtonColumn"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
