import os

from util.client import client

data = {
    "exchangeNo": "",  # 兑换产品编码
    "keyword": "",  # 搜索条件
    "pageNum": 0,  # 当前页
    "pageSize": 0,  # 每页数量
    "stockType": 0,  # 库存类型,0-全部,1-限量,2-非限量
    "title": "",  # 兑换产品名称
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_rights_exhangProductStock_list(data=data, headers=headers):
    """
    库存列表
    /mgmt/prmt/rights/exhangProductStock/list

    参数说明:
    - exchangeNo: 兑换产品编码
    - keyword: 搜索条件
    - pageNum: 当前页
    - pageSize: 每页数量
    - stockType: 库存类型,0-全部,1-限量,2-非限量
    - title: 兑换产品名称
    """

    url = "/mgmt/prmt/rights/exhangProductStock/list"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
