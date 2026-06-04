import os

from util.client import client

data = {
    "exacts": [],  # 精准搜索
    "from": 0,  # TODO: 添加参数说明
    "like": "",  # 模糊搜索
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 每页显示数
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_riskctrl_getAddrKeywordsList(data=data, headers=headers):
    """
    收货地址关键词列表
    /mgmt/order/riskctrl/getAddrKeywordsList

    参数说明:
    - exacts: 精准搜索
    - like: 模糊搜索
    - pageNum: 页数
    - pageSize: 每页显示数
    """

    url = "/mgmt/order/riskctrl/getAddrKeywordsList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
