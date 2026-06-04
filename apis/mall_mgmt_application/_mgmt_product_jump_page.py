import os

from util.client import client

data = {
    "pageNum": 0,  # 页码
    "pageSize": 0,  # 页面大小
    "serialNo": "",  # 商品编码
    "status": 0,  # 状态：1-已上架，2-已下架
    "title": "",  # 商品名称
    "type": 0,  # 跳转内容类型 1-精选推文 2-温馨提示
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_product_jump_page(data=data, headers=headers):
    """
    分页查询
    /mgmt/product/jump/page

    参数说明:
    - pageNum: 页码
    - pageSize: 页面大小
    - serialNo: 商品编码
    - status: 状态：1-已上架，2-已下架
    - title: 商品名称
    - type: 跳转内容类型 1-精选推文 2-温馨提示
    """

    url = "/mgmt/product/jump/page"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
