import os

from util.client import client

params = {
    "serialNos": [],  # serialNos
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_ecenter_selectProduct(params=params, headers=headers):
    """
    查询商品列表 或 添加时搜索商品(需要前端判重)
    /mgmt/ecenter/selectProduct

    参数说明:
    - serialNos: serialNos
    """

    url = "/mgmt/ecenter/selectProduct"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
