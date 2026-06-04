import os

from util.client import client

data = {
    "effectTime": "",  # 生效时间
    "loseEffectTime": "",  # 失效时间
    "distId": 0,  # 分配量id
    "maxNum": 0,  # 最大可销售数量
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_product_quota_updateProduct(data=data, headers=headers):
    """
    编辑
    /mgmt/product/quota/updateProduct

    参数说明:
    - effectTime: 生效时间
    - loseEffectTime: 失效时间
    - distId: 分配量id
    - maxNum: 最大可销售数量
    """

    url = "/mgmt/product/quota/updateProduct"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
