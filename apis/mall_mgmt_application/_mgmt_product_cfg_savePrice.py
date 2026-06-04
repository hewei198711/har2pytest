import os

from util.client import client

data = {
    "groupParam": 0.0,  # 团购参数
    "id": 0,  # id
    "orderParam": 0.0,  # 订货参数
    "productParam": 0.0,  # 货物参数
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_product_cfg_savePrice(data=data, headers=headers):
    """
    价格参数保存
    /mgmt/product/cfg/savePrice

    参数说明:
    - groupParam: 团购参数
    - id: id
    - orderParam: 订货参数
    - productParam: 货物参数
    """

    url = "/mgmt/product/cfg/savePrice"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
