import os

from util.client import client

params = {
    "id": "",  # 节点id
    "sort": "",  # 排序类型
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_product_cfg_sort_type(params=params, headers=headers):
    """
    菜单排序
    /mgmt/product/cfg/sort/{type}

    参数说明:
    - id: 节点id
    - sort: 排序类型
    - type: 菜单类型
    """

    url = f"/mgmt/product/cfg/sort/{params['type']}"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
