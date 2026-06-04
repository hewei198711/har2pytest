import os

from util.client import client

params = {
    "catalogId": "",  # 商品分类Id
    "keyword": "",  # 产品名称/编码
    "pageNum": 0,  # 页码
    "pageSize": 0,  # 每页页数
    "serialNoList": [],  # 产品编码列表
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_getProductList(params=params, headers=headers):
    """
    获取产品列表（点击关联产品）
    /mgmt/cms/getProductList

    参数说明:
    - catalogId: 商品分类Id
    - keyword: 产品名称/编码
    - pageNum: 页码
    - pageSize: 每页页数
    - serialNoList: 产品编码列表
    """

    url = "/mgmt/cms/getProductList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
