import os

from util.client import client

data = {
    "id": 0,  # 跳转内容配置id
    "status": 0,  # 状态:1-上架,2-下架
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_product_jump_updateState(data=data, headers=headers):
    """
    更新状态（上架、下架）
    /mgmt/product/jump/updateState

    参数说明:
    - id: 跳转内容配置id
    - status: 状态:1-上架,2-下架
    """

    url = "/mgmt/product/jump/updateState"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
