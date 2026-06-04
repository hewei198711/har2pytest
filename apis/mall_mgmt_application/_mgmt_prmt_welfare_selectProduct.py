import os

from util.client import client

params = {
    "id": "",  # 活动id,新增页面不传活动id，详情页面传活动id
    "serialNo": "",  # 商品编码
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_welfare_selectProduct(params=params, headers=headers):
    """
    添加时搜索公益购活动商品
    /mgmt/prmt/welfare/selectProduct

    参数说明:
    - id: 活动id,新增页面不传活动id，详情页面传活动id
    - serialNo: 商品编码
    """

    url = "/mgmt/prmt/welfare/selectProduct"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
