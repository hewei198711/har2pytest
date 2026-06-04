import os

from util.client import client

data = {
    "effectTime": "",  # 生效时间
    "loseEffectTime": "",  # 失效时间
    "maxNum": 0,  # 最大可销售数量
    "productId": 0,  # 产品id
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_product_quota_addProduct(data=data, headers=headers):
    """
    新增产品
    /mgmt/product/quota/addProduct

    参数说明:
    - effectTime: 生效时间
    - loseEffectTime: 失效时间
    - maxNum: 最大可销售数量
    - productId: 产品id
    - storeCode: 服务中心编号
    """

    url = "/mgmt/product/quota/addProduct"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
