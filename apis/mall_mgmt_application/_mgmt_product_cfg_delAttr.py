import os

from util.client import client

params = {
    "id": "",  # 节点id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_product_cfg_delAttr(params=params, headers=headers):
    """
    产品属性删除
    /mgmt/product/cfg/delAttr

    参数说明:
    - id: 节点id
    """

    url = "/mgmt/product/cfg/delAttr"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
