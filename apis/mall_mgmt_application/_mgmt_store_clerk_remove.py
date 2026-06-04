import os

from util.client import client

data = {
    "id": 0,  # 店员ID
    "storeCode": "",  # 服务中心编码（门店系统不需要填）
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_clerk_remove(data=data, headers=headers):
    """
    删除店员账号
    /mgmt/store/clerk/remove

    参数说明:
    - id: 店员ID
    - storeCode: 服务中心编码（门店系统不需要填）
    """

    url = "/mgmt/store/clerk/remove"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
