import os

from util.client import client

params = {
    "pageNum": "0",  # 页码
    "pageSize": "0",  # 页面大小
}

headers = {
    "channel": "pc",
    "client": "op",
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_product_cfg_listAttr(params=params, headers=headers):
    """
    产品属性列表
    /mgmt/product/cfg/listAttr

    参数说明:
    - pageNum: 页码
    - pageSize: 页面大小
    """

    url = "/mgmt/product/cfg/listAttr"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
