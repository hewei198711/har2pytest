import os

from util.client import client

data = {
    "id": 0,  # 活动id
    "serialNo": "",  # 主产品编码
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_addMainProduct(data=data, headers=headers):
    """
    手动新增主产品
    /mgmt/prmt/addMainProduct

    参数说明:
    - id: 活动id
    - serialNo: 主产品编码
    """

    url = "/mgmt/prmt/addMainProduct"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
