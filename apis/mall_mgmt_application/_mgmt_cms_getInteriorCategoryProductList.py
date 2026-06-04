import os

from util.client import client

data = {
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


def _mgmt_cms_getInteriorCategoryProductList(data=data, headers=headers):
    """
    从商品中心获取内部分类产品列表
    /mgmt/cms/getInteriorCategoryProductList

    参数说明:
    - catalogId: 商品分类Id
    - keyword: 产品名称/编码
    - pageNum: 页码
    - pageSize: 每页页数
    - serialNoList: 产品编码列表
    """

    url = "/mgmt/cms/getInteriorCategoryProductList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
