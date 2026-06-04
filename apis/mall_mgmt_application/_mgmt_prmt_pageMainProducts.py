import os

from util.client import client

params = {
    "id": 0,  # 活动id
    "pageNum": 0,  # 当前页
    "pageSize": 0,  # 每页数量
    "product": "",  # 产品编号或名称
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_pageMainProducts(params=params, headers=headers):
    """
    分页查询主产品
    /mgmt/prmt/pageMainProducts

    参数说明:
    - id: 活动id
    - pageNum: 当前页
    - pageSize: 每页数量
    - product: 产品编号或名称
    """

    url = "/mgmt/prmt/pageMainProducts"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
