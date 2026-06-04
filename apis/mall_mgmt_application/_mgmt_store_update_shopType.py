import os

from util.client import client

params = {
    "id": 0,  # id
    "name": "",  # name
    "remark": "",  # remark
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_update_shopType(params=params, headers=headers):
    """
    修改网点类型
    /mgmt/store/update/shopType

    参数说明:
    - id: id
    - name: name
    - remark: remark
    """

    url = "/mgmt/store/update/shopType"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
