import os

from util.client import client

params = {
    "pageNum": 0,  # 当前页
    "pageSize": 0,  # 每页数量
    "serialNo": "",  # 单一商品编码
    "serialNos": [],  # 商品编码集合
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_state_checkProduct(params=params, headers=headers):
    """
    校验活动商品
    /mgmt/prmt/state/checkProduct

    参数说明:
    - pageNum: 当前页
    - pageSize: 每页数量
    - serialNo: 单一商品编码
    - serialNos: 商品编码集合
    """

    url = "/mgmt/prmt/state/checkProduct"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
