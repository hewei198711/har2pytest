import os

from util.client import client

data = {
    "id": 0,  # 活动id
    "importKey": "",  # 导入/新增 操作键
    "keyword": "",  # 查询关键字:根据商品编码查询
    "pageNum": 0,  # 当前页
    "pageSize": 0,  # 每页数量:-1表示全量查询
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_luckyActivity_pageProducts(data=data, headers=headers):
    """
    分页查询活动黑名单产品
    /mgmt/prmt/luckyActivity/pageProducts

    参数说明:
    - id: 活动id
    - importKey: 导入/新增 操作键
    - keyword: 查询关键字:根据商品编码查询
    - pageNum: 当前页
    - pageSize: 每页数量:-1表示全量查询
    """

    url = "/mgmt/prmt/luckyActivity/pageProducts"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
