import os

from util.client import client

data = {
    "exchangeProductId": "",  # 兑换产品id
    "keyword": "",  # 搜索条件
    "pageNum": 0,  # 当前页
    "pageSize": 0,  # 每页数量
    "versionId": "",  # 兑换产品版本id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_rights_exhangProduct_listVerLog(data=data, headers=headers):
    """
    兑换产品版本操作日志列表
    /mgmt/prmt/rights/exhangProduct/listVerLog

    参数说明:
    - exchangeProductId: 兑换产品id
    - keyword: 搜索条件
    - pageNum: 当前页
    - pageSize: 每页数量
    - versionId: 兑换产品版本id
    """

    url = "/mgmt/prmt/rights/exhangProduct/listVerLog"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
