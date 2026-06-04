import os

from util.client import client

data = {
    "keyword": "",  # 搜索条件
    "pageNum": 0,  # 当前页
    "pageSize": 0,  # 每页数量
    "stockId": 0,  # 库存id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_rights_exhangProductStock_listHistory(data=data, headers=headers):
    """
    库存历史
    /mgmt/prmt/rights/exhangProductStock/listHistory

    参数说明:
    - keyword: 搜索条件
    - pageNum: 当前页
    - pageSize: 每页数量
    - stockId: 库存id
    """

    url = "/mgmt/prmt/rights/exhangProductStock/listHistory"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
