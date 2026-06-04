import os

from util.client import client

params = {
    "isGift": False,  # 是否查询赠品: true-是,false-否
    "serialNo": "",  # 商品编码
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_combine_selectProduct(params=params, headers=headers):
    """
    搜索3S组合活动商品
    /mgmt/prmt/combine/selectProduct

    参数说明:
    - isGift: 是否查询赠品: true-是,false-否
    - serialNo: 商品编码
    """

    url = "/mgmt/prmt/combine/selectProduct"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
