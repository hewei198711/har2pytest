import os

from util.client import client

params = {
    "id": "",  # 节点id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_product_cfg_get_type(params=params, headers=headers):
    """
    菜单查询
    /mgmt/product/cfg/get/{type}

    参数说明:
    - id: 节点id
    - type: 菜单类型
    """

    url = f"/mgmt/product/cfg/get/{params['type']}"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
