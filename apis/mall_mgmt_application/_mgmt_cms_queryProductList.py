import os

from util.client import client

data = {
    "productCodeList": [],  # 商品编号列表
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_queryProductList(data=data, headers=headers):
    """
    查询获取产品列表
    /mgmt/cms/queryProductList

    参数说明:
    - productCodeList: 商品编号列表
    """

    url = "/mgmt/cms/queryProductList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
