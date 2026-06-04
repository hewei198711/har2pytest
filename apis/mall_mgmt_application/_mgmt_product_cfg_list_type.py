import os

from util.client import client

params = {
    "type": "",  # 菜单类型
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_product_cfg_list_type(params=params, headers=headers):
    """
    配置查询
    /mgmt/product/cfg/list/{type}

    参数说明:
    - type: 菜单类型
    """

    url = f"/mgmt/product/cfg/list/{params['type']}"
    with client.get(url=url, headers=headers) as r:
        return r
