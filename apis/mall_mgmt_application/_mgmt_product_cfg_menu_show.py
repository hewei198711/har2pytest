import os

from util.client import client

headers = {
    "channel": "pc",
    "client": "op",
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_product_cfg_menu_show(headers=headers):
    """
    TODO: 添加接口描述
    /mgmt/product/cfg/menu/show
    """

    url = "/mgmt/product/cfg/menu/show"
    with client.get(url=url, headers=headers) as r:
        return r
