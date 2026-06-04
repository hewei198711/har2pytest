import os

from util.client import client

params = {
    "id": 0,  # 活动id
    "keyword": "",  # 查询关键字
    "pageNum": 0,  # 当前页
    "pageSize": 0,  # 每页数量:-1表示全量查询
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_shoppedGift_exportProducts(params=params, headers=headers):
    """
    导出活动产品
    /mgmt/prmt/shoppedGift/exportProducts

    参数说明:
    - id: 活动id
    - keyword: 查询关键字
    - pageNum: 当前页
    - pageSize: 每页数量:-1表示全量查询
    """

    url = "/mgmt/prmt/shoppedGift/exportProducts"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
