import os

from util.client import client

params = {
    "catalogId": "",  # 类型id
    "pageNum": 0,  # 页码
    "pageSize": 0,  # 页面大小
    "serialNo": "",  # 商品编码
    "showId": "",  # 前端分类
    "title": "",  # 商品名称
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_product_item_listRelShow(params=params, headers=headers):
    """
    商品展示关联列表
    /mgmt/product/item/listRelShow

    参数说明:
    - catalogId: 类型id
    - pageNum: 页码
    - pageSize: 页面大小
    - serialNo: 商品编码
    - showId: 前端分类
    - title: 商品名称
    """

    url = "/mgmt/product/item/listRelShow"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
