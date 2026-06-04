import os

from util.client import client

data = {
    "id": 0,  # 活动id
    "importKey": "",  # 导入/新增 操作键
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_luckyActivity_clearProducts(data=data, headers=headers):
    """
    切换黑白配置清空商品
    /mgmt/prmt/luckyActivity/clearProducts

    参数说明:
    - id: 活动id
    - importKey: 导入/新增 操作键
    """

    url = "/mgmt/prmt/luckyActivity/clearProducts"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
