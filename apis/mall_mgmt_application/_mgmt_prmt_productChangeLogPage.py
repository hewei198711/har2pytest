import os

from util.client import client

params = {
    "createTimeMax": "",  # 创建时间末
    "createTimeMin": "",  # 创建时间始
    "pageNum": 0,  # 当前页
    "pageSize": 0,  # 每页数量
    "productName": "",  # 商品名称
    "promotionId": 0,  # 活动id
    "serialNo": "",  # 商品编码
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_productChangeLogPage(params=params, headers=headers):
    """
    分页查询活动产品编辑记录
    /mgmt/prmt/productChangeLogPage

    参数说明:
    - createTimeMax: 创建时间末
    - createTimeMin: 创建时间始
    - pageNum: 当前页
    - pageSize: 每页数量
    - productName: 商品名称
    - promotionId: 活动id
    - serialNo: 商品编码
    """

    url = "/mgmt/prmt/productChangeLogPage"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
